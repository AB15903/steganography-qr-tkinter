from PIL import Image
import qrcode
import cv2

# --- Encryption Helpers ---
# def xor_encrypt(text, key='mykey'):
    # return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
# 
# def xor_decrypt(text, key='mykey'):
    # return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
# 
# --- QR Code Generation ---
def generate_qr(message, qr_path='qr_temp.png', key='mykey'):
    """Generate a QR code from the given message."""
    qr = qrcode.make(message)
    qr.save(qr_path)
    return qr_path

# ---QR Steganography ---
def hide_image(cover_img_path, secret_img_path, output_path):
    """Hide one image (QR) inside another (cover) using LSB steganography."""
    cover = Image.open(cover_img_path).convert('RGB')
    secret = Image.open(secret_img_path).convert('1')       # Convert to 1-bit mode (black and white)
    secret = secret.resize(cover.size)

    # Resize secret image to match cover image
    width, height = cover.size                 #✅
    secret = secret.resize((width, height))    #✅

    cover = cover.copy()
    cover_pixels = cover.load()
    secret_pixels = secret.load()
    
    

    for y in range(height):
        for x in range(width):
            r, g, b = cover_pixels[x, y]
            bit = 0 if secret_pixels[x, y] == 255 else 1    # white:0, black:1
            r = (r & ~1) | bit        # set LSB of red
            cover_pixels[x, y] = (r, g, b)

    cover.save(output_path)
    return True


def extract_qr_from_image(stego_img_path, output_qr_path='extracted_qr.png'):
    """Extract the hidden QR image from the stego image."""
    stego = Image.open(stego_img_path).convert('RGB')
    stego_pixels = stego.load()
    width, height = stego.size      #✅

    qr_img = Image.new('1', (width, height))        # black and white image
    qr_pixels = qr_img.load()

    for y in range(height):
        for x in range(width):
            r, _, _ = stego_pixels[x, y]
            bit = r & 1
            qr_pixels[x, y] = 0 if bit else 255


    qr_img.save(output_qr_path)
    return output_qr_path

# ---QR Decode + Decrypt ---
def decode_qr_image(qr_image_path, key='mykey'):
    """Decode a QR code image and return the embedded message."""
    img = cv2.imread(qr_image_path)
    qr_decoder = cv2.QRCodeDetector()
    data, bbox, _ = qr_decoder.detectAndDecode(img)

    if data:
        # try:
            # return xor_decrypt(data, key)
        # except Exception:
            # return"[Decryption failed: Incorrect Key or corrupted QR]"
    # else:
        # return 
    

        return data
    else:
         return None

# --- Test Script (optional) ---
if __name__ == "__main__":

    # Step 1 : Generate  QR code from message
    msg = "This is the secret message!"
    key = "securekey"
    qr_path = generate_qr(msg, key=key)


    # Step 2 : Hide the QR code inside a cover image
    cover_image = 'cover.png'   # Use any clear RGB image you have
    stego_image = 'stego_output.png'
    hide_image(cover_image, qr_path, stego_image)

    # Step 3 : Extract QR from the stego image
    extract_qr = extract_qr_from_image(stego_image)


    # Step 4 : Decode the QR image to get the message
    decode_msg = decode_qr_image(extract_qr, key=key)

    print("Decoded Message:", decode_msg)
