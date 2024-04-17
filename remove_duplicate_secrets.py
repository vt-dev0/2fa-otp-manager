def remove_duplicates_and_filter_secrets(input_file, output_file):
    seen_secrets = set()
    filtered_lines = []

    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) < 7:
                continue  # Skip lines that do not have enough data

            secret = parts[0]
            # Check if the secret is long enough and not a duplicate
            if len(secret) > 4 and secret not in seen_secrets:
                seen_secrets.add(secret)
                filtered_lines.append(line)

    # Write the filtered lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(filtered_lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Remove duplicate lines based on the secret and filter out secrets shorter than 5 characters.")
    parser.add_argument("input_file", type=str, help="Path to the input file containing the data.")
    parser.add_argument("output_file", type=str, help="Path to the output file to save the filtered data.")

    args = parser.parse_args()

    remove_duplicates_and_filter_secrets(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
