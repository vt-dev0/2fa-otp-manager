
import sys
import qrcode

def generate_qr_code(url, output_file):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an Image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    img.save(output_file)

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_qr.py <input_file_with_url> <output_file_for_qr.png>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read the URL from the file
    with open(input_file, 'r') as file:
        url = file.read().strip()

    # Generate the QR code
    generate_qr_code(url, output_file)

if __name__ == "__main__":
    main()
