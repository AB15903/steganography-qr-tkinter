import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import  ImageTk, Image
import os
# import base64

from src.qr_utils import generate_qr, hide_image, extract_qr_from_image, decode_qr_image


EOF_MARKER = "ÿÿÿÿ"

def to_bin(data):
    return ''.join(format(ord(char), '08b') for char in data)

def from_bin(bin_data):
    chars = [chr(int(bin_data[i:i+8], 2)) for i in range(0, len(bin_data), 8)]
    return ''.join(chars)

def xor_encrypt(text, key='mykey'):
    # encrypted_bytes = bytes([ord(c) ^ ord(key[i % len(key)])for i, c in enumerate(text)])
    # return base64.b64encode(encrypted_bytes).decode()
   
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))


# def xor_decrypt(encoded_text, key='mykey'):
    # encrypted_bytes = base64.b64encode(encoded_text)
    # return ''.join(chr(b ^ ord(key[i % len(key)])) for i,b in enumerate(encrypted_bytes))


def hide_text(img_path, message, out_path, key='mykey'):
    encrypted_msg = xor_encrypt(message + EOF_MARKER, key)
    binary_msg = to_bin(encrypted_msg)
    img = Image.open(img_path).convert('RGB')
    pixels = list(img.getdata())

    # ✅ Add this warning check here
    if len(binary_msg) > len(pixels) * 3:
        raise ValueError("Message too long to hide in the selected image.")

    new_pixels = []
    idx = 0
    for pixel in pixels:
        r, g, b = pixel
        if idx < len(binary_msg):
            r = (r & ~1) | int(binary_msg[idx])
            idx += 1
        if idx < len(binary_msg):
            g = (g & ~1) | int(binary_msg[idx])
            idx += 1
        if idx < len(binary_msg):
            b = (b & ~1) | int(binary_msg[idx])
            idx += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(out_path)
    return True

def extract_text(img_path, key='mykey'):
    img = Image.open(img_path).convert('RGB')
    pixels = img.getdata()

    binary_data = ""
    for pixel in pixels:
        for color in pixel:
            binary_data += str(color & 1)

    extracted = from_bin(binary_data)
    decrypted = xor_encrypt(extracted, key)

    eof_index = decrypted.find(EOF_MARKER)
    if eof_index != -1:
        decrypted = decrypted[:eof_index]

    return decrypted

# GUI Code
class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.image_path = ""
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=5)
        self.qr_label = tk.Label(root)
        self.qr_label.pack(pady=5)

        tk.Button(root, text="Choose Image", command=self.load_image).pack(pady=5)
        
        tk.Label(root, text="Encryption Key:").pack()
        self.key_entry = tk.Entry(root, show="*")
        self.key_entry.pack(pady=5)
        
        self.text_entry = tk.Text(root, height=10, width=60)
        self.text_entry.pack(pady=5)

        tk.Button(root, text="Hide Message", command=self.hide_message).pack(pady=5)
        tk.Button(root, text="Extract Message", command=self.extract_message).pack(pady=5)
        tk.Button(root, text="Clear All", command=self.clear_all).pack(pady=5)

        # New buttons for QR
        tk.Button(root, text="Generate QR + Hide in Image", command=self.qr_hide).pack(pady=5)
        tk.Button(root, text="Extract QR + Decode message", command=self.qr_extract).pack(pady=5)


    def load_image(self):
        self.image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png *.bmp")])
        if self.image_path:
            messagebox.showinfo("Loaded", f"Image loaded:\n{self.image_path}")

            # ✅ Load and display image
            img = Image.open(self.image_path)
            img = img.resize((300, 300))        # Resize for display purpose
            img_tk  = ImageTk.PhotoImage(img)

            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk     # Keep a refrence to avoid garbage collection


    def hide_message(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image selected.")
            return
        
        message = self.text_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "No message to hide.")
            return
        
        key = self.key_entry.get() or 'mykey'      # 🔐 Use entered key or default
        

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            try:
                hide_text(self.image_path, message, output_path, key=key)       # ✅ Key passed
                messagebox.showinfo("Success", f"Message hidden in {output_path}")
            except ValueError as ve:
                messagebox.showerror("Too long", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error:\n{str(e)}")

    def extract_message(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image selected.")
            return
        
        key = self.key_entry.get() or 'mykey'     # 🔐 Use entered key or default
        try:
            message = extract_text(self.image_path, key=key)        # ✅ Key passed 
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert(tk.END, message)
            messagebox.showinfo("Success", "Message extracted.")
        except Exception as e:
            messagebox.showerror("Error", f"Extraction failed:\n{str(e)}")

    def qr_hide(self):
        if not self.image_path:
            messagebox.showerror("Error", "No cover image selected.")
            return
        
        message = self.text_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "No message to hide.")
            return
        
        try:
            # Step 1 : Generate QR code from message
            qr_path = generate_qr(message)

            # ✅ Show QR before hiding 
            qr_img = Image.open(qr_path).resize((200, 200))
            qr_img_tk = ImageTk.PhotoImage(qr_img)
            self.qr_label.configure(image=qr_img_tk)
            self.qr_label.image = qr_img_tk         # Hold reference

            # Step 2 : Save stego image
            output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if output_path:
                hide_image(self.image_path, qr_path, output_path)

                if os.path.exists(qr_path):
                    os.remove(qr_path)      # 🧹 Optional cleanup

                messagebox.showinfo("Success", f"QR hiding in image:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"QR hiding failed:\n{str(e)}")


    def qr_extract(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image is selected.")
            return
        
        try:
            # Step 1 : Extract QR from stego image
            extracted_qr = extract_qr_from_image(self.image_path)

            # ✅ Step 2 : Display extracted QR
            qr_img = Image.open(extracted_qr)
            qr_img = qr_img.resize((200,200))   # Resize for display
            qr_img_tk = ImageTk.PhotoImage(qr_img)

            self.qr_label.configure(image=qr_img_tk)
            self.qr_label.image = qr_img_tk     # Keep refrence 


            # Step 3 : Decode message from QR 
            message = decode_qr_image(extracted_qr)

            if message:
                self.text_entry.delete("1.0",tk.END)
                self.text_entry.insert(tk.END, message)
                messagebox.showinfo("Success", "Message decode from QR.")
            else:
                messagebox.showwarning("Warning", "No QR code found or decoding failed.")
        except Exception as e:
            messagebox.showerror("Error", f"QR extraction failed:\n{str(e)}")



    def clear_all(self):
        self.image_path = ""
        self.key_entry.delete(0, tk.END)
        self.text_entry.delete("1.0", tk.END)
        self.image_label.configure(image='')    # Clear selected image
        self.image_label.image = None
        self.qr_label.configure(image='')       # Clear QR image
        self.qr_label.image = None


        
# Run GUI
# if __name__ == "__main__":
    # root = tk.Tk()
    # app = StegoApp(root)
    # root.mainloop()
