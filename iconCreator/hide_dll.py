import argparse
from PIL import Image
import os

# Function to read the DLL file and convert it to a bitstream

def read_dll_as_bits(dll_path):
    with open(dll_path, "rb") as file:
        byte_data = file.read()
        bits = ''.join(f'{byte:08b}' for byte in byte_data)
    return bits

# Function for inserting information in the last bits (LSB) of the image

"""
@Aleph: It should be optimized, it can be solved more efficiently. In addition, support for transparency must be added.
"""

def embed_lsb_in_image(image_path, dll_bits, output_image_path):
    # Load the Image using Pillow
    image = Image.open(image_path)
    image = image.convert("RGB")  # We convert to RGB if it is not
    pixels = image.load()

    width, height = image.size
    total_pixels = width * height

    # We ensure that there is enough space in the image.

    if len(dll_bits) > total_pixels * 3:
        raise ValueError("The image is too small to store all the information.")

    bit_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Modify the last bits of each RGB component
            if bit_index < len(dll_bits):
                # Modify the last bit of the red component
                r = (r & 0xFE) | int(dll_bits[bit_index])
                bit_index += 1
            if bit_index < len(dll_bits):
                # Modify the last bit of the green component
                g = (g & 0xFE) | int(dll_bits[bit_index])
                bit_index += 1
            if bit_index < len(dll_bits):
                # Modify the last bit of the blue component
                b = (b & 0xFE) | int(dll_bits[bit_index])
                bit_index += 1

            # Save the modified pixel
            pixels[x, y] = (r, g, b)

    image.save(output_image_path)
    print(f"Image stored in {output_image_path}")

def main():

    parser = argparse.ArgumentParser(description="Inserts information in the last significant bits (LSB) of an image.")
    parser.add_argument("image_path", help="Image path 256x256")
    parser.add_argument("dll_path", help="DLL file path")
    parser.add_argument("output_image_path", help="Path where the modified image will be saved")
    
    args = parser.parse_args()

    dll_bits = read_dll_as_bits(args.dll_path)

    embed_lsb_in_image(args.image_path, dll_bits, args.output_image_path)
    
if __name__ == "__main__":
    main()
