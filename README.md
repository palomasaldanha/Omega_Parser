# OMEGA Combo Parser Tool

```
░░      ░░░  ░░░░  ░░        ░░░      ░░░░      ░░░░░░░░    
▒  ▒▒▒▒  ▒▒   ▒▒   ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒▒▒▒▒▒    
▓  ▓▓▓▓  ▓▓        ▓▓      ▓▓▓▓  ▓▓▓   ▓▓  ▓▓▓▓  ▓▓▓▓▓▓▓    
█  ████  ██  █  █  ██  ████████  ████  ██        ███████    
██      ███  ████  ██        ███      ███  ████  ███████    
                                                            
░       ░░░░      ░░░       ░░░░      ░░░        ░░       ░░
▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒
▓       ▓▓▓  ▓▓▓▓  ▓▓       ▓▓▓▓      ▓▓▓      ▓▓▓▓       ▓▓
█  ████████        ██  ███  █████████  ██  ████████  ███  ██
█  ████████  ████  ██  ████  ███      ███        ██  ████  █
```

This **OMEGA Combo Parser Tool** is designed to parse text files containing leaked credentials with the format `URL:USER:PASS` (or variations). The tool processes large datasets containing such credentials, identifies patterns, and writes the extracted data to a CSV file with columns for file name, hash, URL, username, and password. It also skips already processed files using a hash check to avoid redundant processing.

## Features

- **Pattern Matching**: Extracts credentials from various formats, including `URL:USER:PASS`, `USER:PASS:URL`, and other variations.
- **Hashing**: Generates a SHA-256 hash for each file to prevent reprocessing of previously parsed files.
- **Error Handling**: Skips over lines with encoding issues or malformed data.
- **Warning Summary**: Instead of printing a flood of warnings during execution, it logs any parsing issues and provides a summary at the end of execution.

## Usage

### Requirements

- **Python 3.x**: Make sure you have Python 3 installed on your system.
- Required packages:
  - `csv`
  - `re`
  - `os`
  - `hashlib`
  - `argparse`

You can install dependencies (if any additional packages are needed) with:

```bash
pip install -r requirements.txt
```

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/omega_combo_parser.git
   ```

2. Navigate into the project directory:

   ```bash
   cd omega_combo_parser
   ```

3. Make sure the Python script is executable:

   ```bash
   chmod +x combo_parser.py
   ```

### Running the Tool

The tool requires two arguments:
- **`-i`**: Input folder containing `.txt` files with credentials.
- **`-o`**: Output CSV file that will contain the extracted data.

Example command:

```bash
python combo_parser.py -i /path/to/input/folder -o output.csv
```

### Command-line Arguments

- **`-i / --input`**: Path to the input folder containing `.txt` files with the credentials.
- **`-o / --output`**: Path to the output CSV file where parsed credentials will be saved.

### Example

```bash
python combo_parser.py -i /Users/your_user/Documents/Telegram_Credentials -o Omega_DB.csv
```

### CSV Output

The tool will generate a CSV file with the following columns:
- `FILE`: The name of the file where the credentials were found.
- `HASH`: The SHA-256 hash of the file, used for detecting duplicates.
- `URL`: The extracted URL (if present).
- `USER`: The extracted username (if present).
- `PASS`: The extracted password (if present).

### Error Handling

The tool can handle common issues like:
- **Malformed lines**: If a line does not follow the expected format, it will be skipped, and a warning will be logged.
- **Encoding errors**: Lines with encoding issues will be skipped, and a warning will be logged.

### Example of Warnings

The tool provides a summary of warnings for any lines that couldn't be parsed, printed at the end of execution. These warnings can help identify files or lines that need manual intervention.

```plaintext
Warnings Summary:
Warning: Could not parse line in /path/to/input/file.txt: android //qbMQCZh-CU_SBn04UFat_bLMSicoFKWYI0...
Warning: Could not parse line in /path/to/input/file.txt: javascript: victor.rocchi@gmail.com:bikmop2020...
```

## Contribution

Feel free to contribute by opening issues, submitting pull requests, or suggesting improvements!

### How to Contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push your changes and create a pull request.

