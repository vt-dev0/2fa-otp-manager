

# Usage

## Pre-requisite:
> #### This list of scripts, whether it's *decoding* or *encoding* uses standard format
> `secret;name;issuer;algorithm;digits;type;counter`<br>
> `version;batch_size;batch_index;batch_id`

<br>

### `decode_single_qr.py <image_path> <file_output>` 
> - `<image_path>` - path to an image containing QR code.
> - `<file_output>` - path to a file that will contain decoded data.
> - Decodes QR code from an image and saves the output to the specified file.
> - Expected result is file with `otpauth-migration://` URL

<br>

### `decode_batch_qr.py <directory> <output>`
> - `<directory>` - path to a directory that contains multiple QR images.
> - `<output>` -  path to a file that will contain decoded data.
> - Decodes all QR codes in given directory and saves the output to the specified file.
> - Expected result is list of otp-parameters in accordance with standard format.
> - Last line for each batch will always contain `version;batch_size;batch_index;batch_id`

<br>

### `decode_migration_url.py <input_file> <output_file>`
> - `<input_file>` - path to a file that contains `otpauth-migration://` URL
> - `<output_file>` - path to a file where decoded data will be stored.
> - Expected result is list of otp-parameters in accordance with standard format.
> - Last line for each batch will always contain `version;batch_size;batch_index;batch_id`

<br>

### `encode_migration_url.py <input_file> <output_file>`
> - `<input_file>` - path to a file that contains list of otp-parameters in accordance with standard format.
> - `<output_file>` - path to a file where `otpauth-migration://` URL will be stored.
> - Expected result is `otpauth-migration://` URL.

<br>

### `encode_single_qr.py <input_file> <output_image>`
> - `<input_file>` - path to a file that contains `otpauth-migration://` URL.
> - `<output_image>` - path to a file where QR image will be stored.
> - Expected result is QR image.

<br>

### `encode_batch_qr.py <input_file> <output_directory>`
> - `<input_file>` - path to a file that contains list of otp-parameters in accordance with standard format.
> - `<output_directory>` - path to a file where QR image will be stored.
> - Expected result is list of QR images.
> - Input file should not contain lines with `version;batch_size;batch_index;batch_id`

<br>

### `remove_duplicate_secrets.py <input_file> <output_file>`
> - `<input_file>` - path to a file that contains list of otp-parameters in accordance with standard format.
> - `<output_file>` - path to a file where filtered unique list of otp-parameters will be stored.
> - Expected result is file that contains list of unique otp-parameters.

