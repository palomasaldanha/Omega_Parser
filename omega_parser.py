import re
import csv
import os
import hashlib
import argparse

# Define a function to detect patterns and return (url, user, pass)
def extract_credentials(line):
    # Skip lines that are likely to be malformed
    if line.startswith(":") or "javascript:" in line:
        return None
    
    # Add http to URLs that don't have a scheme
    if not line.startswith("http"):
        line = re.sub(r'(?P<url>([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})([^\s:]*))', r'http://\g<url>', line)

    # Common patterns with or without URL schemes
    patterns = [
        r'(?P<url>https?://[^\s|:]+)[|:](?P<user>[^\s|:]+)[|:](?P<pass>[^\s|:]+)',  # URL:USER:PASS
        r'(?P<user>[^\s|:]+)[|:](?P<pass>[^\s|:]+)[|:](?P<url>https?://[^\s|:]+)',  # USER:PASS:URL
        r'(?P<url>https?://[^\s|:]+)[|:](?P<user>[^\s|:]+)',                        # URL:USER (no PASS)
        r'(?P<url>https?://[^\s|:]+)',                                              # URL only
        r'(?P<url>http://[^\s|/]+/?[^\s|:]+)[|:](?P<user>[^\s|:]+)[|:](?P<pass>[^\s|:#]+)',  # URL (no scheme):USER:PASS
        r'(?P<user>[^\s|:]+)[|:](?P<pass>[^\s|:]+)',                                # USER:PASS (no URL)
        r'(?P<url>android://[^\s|:]+)[|:](?P<user>[^\s|:]+)[|:](?P<pass>[^\s|:#]+)' # android:// scheme
    ]
    
    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            return match.groupdict()

    return None

# Function to calculate the hash of a file
def calculate_hash(filepath):
    hash_sha256 = hashlib.sha256()
    with open(filepath, 'rb') as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            hash_sha256.update(byte_block)
    return hash_sha256.hexdigest()

# Function to load existing hashes from the CSV file
def load_existing_hashes(output_file):
    if not os.path.exists(output_file):
        return set()

    existing_hashes = set()
    with open(output_file, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        if 'HASH' not in reader.fieldnames:
            return existing_hashes

        for row in reader:
            existing_hashes.add(row['HASH'])
    return existing_hashes

# Function to process a single file and append to CSV if hash is new
def process_file(filename, output_file, mode, existing_hashes, warnings):
    file_hash = calculate_hash(filename)

    if file_hash in existing_hashes:
        print(f"Skipping {filename} (already processed)")
        return

    with open(output_file, mode, newline='', encoding='utf-8') as csv_file:
        fieldnames = ['FILE', 'HASH', 'URL', 'USER', 'PASS']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if mode == 'w':
            writer.writeheader()

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        credentials = extract_credentials(line)
                        if credentials:
                            writer.writerow({
                                'FILE': os.path.basename(filename),
                                'HASH': file_hash,
                                'URL': credentials.get('url', ''),
                                'USER': credentials.get('user', ''),
                                'PASS': credentials.get('pass', '')
                            })
                        else:
                            warnings.append(f"Could not parse line in {filename}: {line}")
        except UnicodeDecodeError:
            warnings.append(f"UnicodeDecodeError in {filename}. Skipping problematic lines.")

# Main function to process all files in the folder
def process_files(input_folder, output_file):
    existing_hashes = load_existing_hashes(output_file)
    warnings = []

    if os.path.exists(output_file):
        mode = 'a'
    else:
        mode = 'w'

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if filename.endswith('.txt'):
            print(f"Processing {filename}...")
            process_file(file_path, output_file, mode, existing_hashes, warnings)
            mode = 'a'

    # Print warnings summary at the end
    if warnings:
        print("\nWarnings Summary:")
        for warning in warnings:
            print(warning)

# Main function with argparse
def main():
    logo = """
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
    """

    print(logo)
    print("A parser tool for treating Combo files for OMEGA Group")

    parser = argparse.ArgumentParser(description="A parser tool for treating Combo files for OMEGA Group")
    parser.add_argument('-i', '--input', required=True, help="Input folder containing the .txt files")
    parser.add_argument('-o', '--output', required=True, help="Output CSV file")

    args = parser.parse_args()

    process_files(args.input, args.output)

if __name__ == '__main__':
    main()
