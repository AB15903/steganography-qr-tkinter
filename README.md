#  🔐 Steanography + QR Code Encryption Tool (GUI-Based)

This project is a Python-based steganography tool with a graphical user interface (GUI) that allows users to:

- Hide a secret text message inside an image using XOR encryption.
- Generate a QR code from a secret message and hide the QR inside the image.
- Extract and decrypt hidden message or QR codes from the stego image.


> Supports both plaintext and QR-based double obfuscation for enhanced data privacy.


---


## 🖥️ Features

- 🧩 **XOR Encryption** of message before hiding.
- 🏞️ **Image Steganography** using Least Significant Bit (LSB).
- 📷 **QR Code generation and extraction** for double-layered security.
- 🔐 **Decryption with custom key** for added safety.
- 💡 **User-friendly GUI** built with Tkinter.
- 🧪 Built-in error handling and message size validation.

---


## 🚀 How It Works

1. **Plain Message Mode:**
   - Enter a secret message and a key.
   - The message is XOR encrypted and hidden in the image.
   - Later, use the same key to extract and decrypt the message.

2. **QR Mode:**
   - A QR code is generated from the message.
   - The QR image is then hidden inside a cover image using LSB.
   - The QR can be extracted and scanned to retrieve the original encrypted message.

3. **Tools and Libraries Used :**
   - **python 3.10 or 3.10+**
   - Tkinter - GUI framework
   - pillow (PIL) - Image processing
   - OpenCV - QR decoding
   - qrcode - QR code generation
   - pyzbar - QR decoding from images
 
Make sure to install the required dependencies:

``` bash
pip install -r requirements.txt
python app.py

