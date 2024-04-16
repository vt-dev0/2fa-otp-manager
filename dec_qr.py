
import argparse
from PIL import Image
from pyzbar.pyzbar import decode
import base64

def decode_qr_to_file(image_path, output_file):
    # Load the image
    image = Image.open(image_path)
    
    # Decode the QR code
    decoded_objects = decode(image)
    if not decoded_objects:
        raise ValueError("No QR Code found in the image.")
    
    # Extract data from the first QR code
    qr_data = decoded_objects[0].data.decode('utf-8')
    
    # Write data to a file
    with open(output_file, 'w') as file:
        file.write(qr_data)

def main():
    parser = argparse.ArgumentParser(description="Decode a QR code from an image and output the data to a text file.")
    parser.add_argument("image_path", type=str, help="Path to the image file containing the QR code.")
    parser.add_argument("output_file", type=str, help="Path to the output text file where the QR data will be saved.")
    args = parser.parse_args()
    
    decode_qr_to_file(args.image_path, args.output_file)

if __name__ == "__main__":
    main()
