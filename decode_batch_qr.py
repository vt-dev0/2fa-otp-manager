import argparse
import base64
import os
from urllib.parse import urlparse, parse_qs

import otpauth_migration_pb2  # Import the generated protobuf module
from PIL import Image
from pyzbar.pyzbar import decode


def decode_batch_qr(directory, output):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            try:
                decode_qr_to_file(file_path, output)
            except Exception as exception:
                print(f"Error with file: {file_path}")
                print(f"Exception: {exception}")


def decode_qr_to_file(image_path, output_file):
    # Load the image
    image = Image.open(image_path)

    # Decode the QR code
    decoded_objects = decode(image)
    if not decoded_objects:
        raise ValueError("No QR Code found in the image.")

    # Extract data from the first QR code
    qr_data = decoded_objects[0].data.decode('utf-8')

    decode_migration_url(qr_data, output_file)


def decode_migration_url(migration_url_data, output_file):
    migration_url = migration_url_data

    # Parse the URL and extract the base64 encoded data
    parsed_url = urlparse(migration_url)
    query_params = parse_qs(parsed_url.query)
    encoded_data = query_params['data'][0]
    data = base64.urlsafe_b64decode(encoded_data + '===')  # Ensure padding is correct for base64 decoding

    # Decode using the protobuf definition
    migration_payload = otpauth_migration_pb2.MigrationPayload()
    migration_payload.ParseFromString(data)

    # Process each parameter into the specified format and write to a file
    with open(output_file, 'a') as file:
        for param in migration_payload.otp_parameters:
            secret = base64.b32encode(param.secret).decode('utf-8')
            name = param.name if param.name else ''
            issuer = param.issuer if param.issuer else ''
            algorithm = str(param.algorithm) if param.algorithm else '0'
            digits = str(param.digits) if param.digits else '0'
            type_ = str(param.type) if param.type else '0'
            counter = str(param.counter) if param.counter else '0'

            line = f"{secret};{name};{issuer};{algorithm};{digits};{type_};{counter}\n"
            file.write(line)

        # After all URLs, insert additional data
        version = str(migration_payload.version) if hasattr(migration_payload, 'version') else '0'
        batch_size = str(migration_payload.batch_size) if hasattr(migration_payload, 'batch_size') else '0'
        batch_index = str(migration_payload.batch_index) if hasattr(migration_payload, 'batch_index') else '0'
        batch_id = str(migration_payload.batch_id) if hasattr(migration_payload, 'batch_id') else '0'

        additional_data = f"{version};{batch_size};{batch_index};{batch_id}"
        file.write(additional_data)
        file.write("\n\n")


def main():
    parser = argparse.ArgumentParser(description="Decode a QR code from an image and output the data to a text file.")
    parser.add_argument("directory", type=str, help="Path to the directory that contains all the QR codes.")
    parser.add_argument("output", type=str, help="Path to the output file that will contain all the decoded data.")
    args = parser.parse_args()

    try:
        decode_batch_qr(args.directory, args.output)
    except Exception as e:
        print(f"Exception occurred: {e}")


if __name__ == "__main__":
    main()
