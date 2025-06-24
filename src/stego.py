from PIL import Image

# Rare EOF marker to signal end of message
EOF_MARKER = "ÿÿÿÿ"

def to_bin(data: str) -> str:
    """Convert string to binary."""
    return ''.join(format(ord(char), '08b') for char in data)

def from_bin(bin_data: str) -> str:
    """Convert binary to string."""
    chars = [chr(int(bin_data[i:i+8], 2)) for i in range(0, len(bin_data), 8)]
    return ''.join(chars)

def xor_encrypt(text: str, key: str = 'mykey') -> str:
# def xor_cipher(text: str, key: str = 'mykey') -> str:
    """Encrypt or decrypt text using XOR with key."""
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

def hide_text_in_image(img_path: str, message: str, out_path: str, key: str = 'mykey') -> bool:
    """Hide a message inside an image and save it."""
    encrypted_msg = xor_encrypt(message + EOF_MARKER, key)
    binary_msg = to_bin(encrypted_msg)

    img = Image.open(img_path).convert('RGB')
    pixels = list(img.getdata())

    # ✅ Check if message fits in image
    # if len(binary_msg) > len(pixels) * 3:
    #     raise ValueError("Message is too long to fit in this image.")
    

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

    if idx > len(binary_msg):
        raise ValueError("Message is too long to fit in this image.")

    img.putdata(new_pixels)
    img.save(out_path)
    return True

def extract_text_from_image(img_path: str, key: str = 'mykey') -> str:
    """Extract and decrypt message from image."""
    img = Image.open(img_path).convert('RGB')
    pixels = list(img.getdata())

    binary_data = ""
    for pixel in pixels:
        for color in pixel:
            binary_data += str(color & 1)

    extracted = from_bin(binary_data)
    decrypted = xor_encrypt(extracted, key)

    eof_index = decrypted.find(EOF_MARKER)
    if eof_index != -1:
        return decrypted[:eof_index]
    return decrypted
