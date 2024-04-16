
import sys
import base64
from urllib.parse import urlparse, parse_qs
import otpauth_migration_pb2  # Import the generated protobuf module

def decode_migration_url_from_file(input_file):
    # Read the migration URL from the input file
    with open(input_file, 'r') as file:
        migration_url = file.read().strip()
    
    # Parse the URL and extract the base64 encoded data
    parsed_url = urlparse(migration_url)
    query_params = parse_qs(parsed_url.query)
    encoded_data = query_params['data'][0]
    data = base64.urlsafe_b64decode(encoded_data + '===')  # Ensure padding is correct for base64 decoding

    print("parsed_url: ", parsed_url)
    print("query_params: ", query_params)
    print("encoded_data: ", encoded_data)
    print("data: ", data)

    # Decode using the protobuf definition
    migration_payload = otpauth_migration_pb2.MigrationPayload()
    migration_payload.ParseFromString(data)

    print("migration_payload: ", migration_payload)
    print("migration_payload.version: ", migration_payload.version)
    print("migration_payload.batch_size: ", migration_payload.batch_size)
    print("migration_payload.otp_parameters: ", migration_payload.otp_parameters)

    # Generate otpauth URLs from the decoded data
    otpauth_urls = []
    for param in migration_payload.otp_parameters:
        secret = base64.b32encode(param.secret).decode('utf-8').rstrip('=')
        issuer = param.issuer
        name = param.name
        url = f"otpauth://totp/{issuer}:{name}?secret={secret}&issuer={issuer}"
        otpauth_urls.append(url)

    return otpauth_urls

def write_urls_to_file(urls, output_file):
    # Write each URL to the specified output file
    with open(output_file, 'w') as file:
        for url in urls:
            file.write(url + '\n')

def main():
    if len(sys.argv) < 3:
        print("Usage: python decode_script.py <input_file_with_url> <output_file_for_urls>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    otpauth_urls = decode_migration_url_from_file(input_file)
    write_urls_to_file(otpauth_urls, output_file)

if __name__ == "__main__":
    main()
