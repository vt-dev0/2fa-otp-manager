import sys
import base64
from urllib.parse import urlparse, parse_qs
import otpauth_migration_pb2  # Import the generated protobuf module


def decode_migration_url(input_file, output_file):
    # Read the migration URL from the input file
    with open(input_file, 'r') as file:
        migration_url = file.read().strip()

    # Parse the URL and extract the base64 encoded data
    parsed_url = urlparse(migration_url)
    query_params = parse_qs(parsed_url.query)
    encoded_data = query_params['data'][0]
    data = base64.urlsafe_b64decode(encoded_data + '===')  # Ensure padding is correct for base64 decoding

    # Decode using the protobuf definition
    migration_payload = otpauth_migration_pb2.MigrationPayload()
    migration_payload.ParseFromString(data)

    # Process each parameter into the specified format and write to a file
    with open(output_file, 'w') as file:
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


def main():
    if len(sys.argv) < 3:
        print("Usage: python decode_script.py <input_file_with_url> <output_file_for_formatted_data>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    decode_migration_url(input_file, output_file)


if __name__ == "__main__":
    main()
