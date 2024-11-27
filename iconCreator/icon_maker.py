import os
import subprocess
import argparse
from PIL import Image

"""
Author: Aleph
Description: This script obtains an image in 512x512 resolution to create and resize the images needed to form the icon. 
Wait before “assembling” all the images in the ICO format for the information to be hidden.

You can start from this function to change the waiting method to the function that hides the information in the file,
as can be seen in <example_auto_hide_dll.py>.

The script uses ImageMagick to manipulate the images and does not remove the information hidden 
by compression algorithms and so on.
"""

def create_icon(input_image_path, output_icon_path):
    
    # Defines the resolution of the images for the icon
    icon_sizes = [16, 32, 48, 64, 128, 256]
    
    # Creates a list of temporary files with the resized images
    temp_files = []
    for size in icon_sizes:
        temp_file = f"temp_{size}.png"
        temp_files.append(temp_file)
        
        # Uses ImageMagick to resize the image
        subprocess.run(["magick", input_image_path, "-resize", f"{size}x{size}", temp_file])

    print("[!] The images have been resized. Modify the 256x256 image before continuing.")
    print("[!] Make sure that the 256x256 image contains the steganographic information.")
    print("[!] Press any key to continue once the image has been modified...")

    input()  # This is where you wait for the user to modify the image and press a key.

    # Now, after the modification, create the .ico file with the resized images
    subprocess.run(["magick"] + temp_files + [output_icon_path])

    # Delete temporary files
    for temp_file in temp_files:
        os.remove(temp_file)

    print(f"Icon saved in {output_icon_path}")


def main():

    parser = argparse.ArgumentParser(description="Create an icon (.ico) file from a 512x512 image.")

    parser.add_argument('input_image', type=str, help="Path to the input image (e.g., input_image.png)")
    parser.add_argument('output_icon', type=str, help="Path to the output .ico file (e.g., output_icon.ico)")
    
    args = parser.parse_args()

    create_icon(args.input_image, args.output_icon)

if __name__ == "__main__":
    main()

