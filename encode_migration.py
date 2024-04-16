import sys
import base64
from urllib.parse import urlparse, parse_qs, quote_plus, quote
import otpauth_migration_pb2  # Import the generated protobuf module

def read_otpauth_urls(input_file):
    # Read all otpauth URLs from the input file
    with open(input_file, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls if url.strip()]

def encode_to_migration_url(otpauth_urls):
    # Create a new MigrationPayload instance
    migration_payload = otpauth_migration_pb2.MigrationPayload()

    for url in otpauth_urls:
        print(f"Processing URL: {url}")
        if 'otpauth://totp/' not in url and 'otpauth://hotp/' not in url:
            print(f"Skipping URL due to missing 'totp' or 'hotp': {url}")
            continue

        # Extracting parts after 'totp/' or 'hotp/'
        token_type = 'totp' if 'totp' in url else 'hotp'
        part_after_token = url.split(f'otpauth://{token_type}/')[1].split('?')[0]
        account_info = part_after_token.split(':')
        if len(account_info) != 2:
            print(f"Skipping URL due to incorrect account information format: {url}")
            continue

        issuer, account_name = account_info
        params = parse_qs(urlparse(url).query)
        print(f"Parsed parameters: {params}")

        # Create and configure a new OtpParameters instance
        otp_param = migration_payload.otp_parameters.add()
        otp_param.secret = base64.b32decode(params['secret'][0].encode('utf-8'))
        otp_param.name = account_name
        otp_param.issuer = issuer if issuer else ""

        # Set default values for algorithm, digits, type, and counter if applicable
        otp_param.algorithm = getattr(otpauth_migration_pb2.MigrationPayload.Algorithm, f'ALGORITHM_{params.get("algorithm", ["SHA1"])[0].upper()}')
        otp_param.digits = getattr(otpauth_migration_pb2.MigrationPayload.DigitCount, f'DIGIT_COUNT_{params.get("digits", ["SIX"])[0]}')
        otp_param.type = otpauth_migration_pb2.MigrationPayload.OtpType.OTP_TYPE_TOTP
        otp_param.counter = 0

        print(f"Algorithm: {otp_param.algorithm}")
        print(f"Digits: {otp_param.digits}")
        print(f"Type: {otp_param.type}")
        print(f"Counter: {otp_param.counter}")

# Assuming you have set up your protobuf object (new_data) correctly
    binary_original = base64.urlsafe_b64decode("Ch4KD81C4UFLuhk+OO98exHZtBIFdGVzdDEgASgBMAIQAhgBIAA=")

    migration_payload.version = 2
    migration_payload.batch_size = 1
    migration_payload.batch_index = 0

    print("migration_payload: ", migration_payload)
    print("migration_payload.version: ", migration_payload.version)
    print("migration_payload.batch_size: ", migration_payload.batch_size)
    print("migration_payload.otp_parameters: ", migration_payload.otp_parameters)

    binary_new = migration_payload.SerializeToString()

    if not hasattr(migration_payload, 'batch_index') or migration_payload.batch_index == 0:
        binary_new += b'\x20\x00'

    print("binary_original: ", binary_original)
    print("binary_new:      ", binary_new)

    # Convert both to hexadecimal for comparison
    hex_original = binary_original.hex()
    hex_new = binary_new.hex()

    print("Original Hex:    ", hex_original)
    print("New Hex:         ", hex_new)

    # Check if they match
    print("Data Matches:", hex_original == hex_new)

    # Serialize to binary string
    data = migration_payload.SerializeToString()
    if not hasattr(migration_payload, 'batch_index') or migration_payload.batch_index == 0:
        data += b'\x20\x00'
    encoded_data = base64.b64encode(data).decode('utf-8')

    print("encoded: ", encoded_data)

    # Construct the migration URL
    return f'otpauth-migration://offline?data={quote(encoded_data)}'

def write_migration_url_to_file(migration_url, output_file):
    # Write the migration URL to the specified output file
    with open(output_file, 'w') as file:
        file.write(migration_url + '\n')

def main():
    if len(sys.argv) < 3:
        print("Usage: python encode_script.py <input_file_with_urls> <output_file_for_migration_url>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    otpauth_urls = read_otpauth_urls(input_file)
    migration_url = encode_to_migration_url(otpauth_urls)
    write_migration_url_to_file(migration_url, output_file)

if __name__ == "__main__":
    main()
