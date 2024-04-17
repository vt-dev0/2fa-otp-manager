import base64
from urllib.parse import quote
import qrcode
import otpauth_migration_pb2  # Ensure this is generated from the .proto file and available


def encode_to_migration_url(otp_parameters):
    # Create a new MigrationPayload instance
    migration_payload = otpauth_migration_pb2.MigrationPayload()

    for item in otp_parameters:
        secret, name, issuer, algorithm, digits, type_, counter = item.strip().split(';')
        otp_param = migration_payload.otp_parameters.add()
        otp_param.secret = base64.b32decode(secret)
        otp_param.name = name if name else ''
        otp_param.issuer = issuer if issuer else ''
        otp_param.algorithm = int(algorithm) if algorithm else 0
        otp_param.digits = int(digits) if digits else 0
        otp_param.type = int(type_) if type_ else 0
        otp_param.counter = int(counter) if counter else 0

    migration_payload.version = int(2)
    migration_payload.batch_size = int(1)
    migration_payload.batch_index = int(0)
    migration_payload.batch_id = int(0)

    # Serialize to binary string and encode to base64
    data = migration_payload.SerializeToString()
    encoded_data = base64.b64encode(data).decode('utf-8')

    # Construct the migration URL
    return f"otpauth-migration://offline?data={quote(encoded_data)}"


def generate_qr_code(data, filename):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)


def process_batches(input_file, output_directory):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    batch_size = 10
    num_batches = len(lines) // batch_size + (1 if len(lines) % batch_size != 0 else 0)

    for i in range(num_batches):
        batch = lines[i * batch_size:(i + 1) * batch_size]
        otp_parameters = [line.strip() for line in batch if line.strip()]  # Example handling, needs specific parsing

        # Encode to migration URL
        migration_url = encode_to_migration_url(otp_parameters)

        # Generate QR code and save it to a file
        filename = f"{output_directory}/qr_{i + 1}.png"
        generate_qr_code(migration_url, filename)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Process batches of lines into QR codes.")
    parser.add_argument("input_file", type=str, help="Path to the input file with data.")
    parser.add_argument("output_directory", type=str, help="Directory to save the QR codes.")

    args = parser.parse_args()
    process_batches(args.input_file, args.output_directory)


if __name__ == "__main__":
    main()
