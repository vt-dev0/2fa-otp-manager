import sys
import base64
from urllib.parse import quote_plus, quote
import otpauth_migration_pb2  # Import the generated protobuf module

def encode_migration_url(input_file, output_file):
    migration_payload = otpauth_migration_pb2.MigrationPayload()

    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Process all lines except the last one for otp_parameters
    for line in lines[:-1]:
        secret, name, issuer, algorithm, digits, type_, counter = line.strip().split(';')
        otp_param = migration_payload.otp_parameters.add()
        otp_param.secret = base64.b32decode(secret)
        otp_param.name = name if name else ''
        otp_param.issuer = issuer if issuer else ''
        otp_param.algorithm = int(algorithm) if algorithm else 0
        otp_param.digits = int(digits) if digits else 0
        otp_param.type = int(type_) if type_ else 0
        otp_param.counter = int(counter) if counter else 0

    # Process the last line for other attributes
    version, batch_size, batch_index, batch_id = lines[-1].strip().split(';')
    migration_payload.version = int(version)
    migration_payload.batch_size = int(batch_size)
    migration_payload.batch_index = int(batch_index)
    migration_payload.batch_id = int(batch_id)

    # Serialize to binary string and encode to base64
    data = migration_payload.SerializeToString()
    encoded_data = base64.b64encode(data).decode('utf-8')

    # Construct the migration URL
    migration_url = f"otpauth-migration://offline?data={quote(encoded_data)}"

    # Write the migration URL to the specified output file
    with open(output_file, 'w') as file:
        file.write(migration_url)

def main():
    if len(sys.argv) < 3:
        print("Usage: python encode_script.py <input_file_with_formatted_data> <output_file_for_migration_url>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    encode_migration_url(input_file, output_file)

if __name__ == "__main__":
    main()
