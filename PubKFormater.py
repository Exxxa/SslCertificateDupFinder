from cryptography import x509
from cryptography.hazmat.backends import default_backend
import threading
import sys
import os
# Create a lock for thread safety
file_write_lock = threading.Lock()
sys.set_int_max_str_digits(6000)

def get_public_key_formats_from_crt(crt_file_path):
    try:
        # Open the CRT file in binary mode and read its contents
        with open(crt_file_path, "rb") as crt_file:
            crt_data = crt_file.read()

        # Parse the CRT file using the cryptography library
        cert = x509.load_pem_x509_certificate(crt_data, default_backend())

        # Extract the public key components
        public_key = cert.public_key()
        public_numbers = public_key.public_numbers()

        # Get modulus in decimal format
        modulus_decimal = public_numbers.n

        return modulus_decimal
    except Exception as e:
        # If an exception occurs (e.g., parsing error), return None
        # Uncomment the next line if you want to print the exception message
        # print(f"No number {crt_file_path}")
        return None
def process_certificate_files(start_index, end_index, modulus_output_file):
    try:
        # Open the modulus output file in append mode
        with open(modulus_output_file, "a") as modulus_file:
            # Iterate through the specified range of certificate indices
            for i in range(start_index, end_index + 1):
                # Construct the file path for the certificate
                crt_file_path = f"Certificates/{i}.crt"

                # Get the public key modulus from the certificate
                modulus_decimal = get_public_key_formats_from_crt(crt_file_path)

                # Check if the modulus is not None (indicating successful extraction)
                if modulus_decimal is not None:
                    # Acquire the lock before writing to the output file
                    with file_write_lock:
                        modulus_file.write(f"{modulus_decimal}\n")
                        #print(f"Writing {crt_file_path}")
                        
    except Exception as e:
        # If an exception occurs (e.g., parsing error), return None
        return None
        
def sort_lines_by_length(input_file, output_file):
    # Read lines from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Sort lines by length
    sorted_lines = sorted(lines, key=len)

    # Write sorted lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(sorted_lines)

def find_duplicate_lines(input_file, output_file):
    # Read lines from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Dictionary to store lines and their corresponding line numbers
    line_dict = {}

    # Iterate through lines
    for i, line in enumerate(lines, start=1):
        # Remove leading and trailing whitespaces
        clean_line = line.strip()

        # Check if the line is already in the dictionary
        if clean_line in line_dict:
            # If yes, append the current line number to the existing entry
            line_dict[clean_line].append(i)
        else:
            # If no, create a new entry with the current line number
            line_dict[clean_line] = [i]

    # Filter entries with more than one line number (i.e., duplicates)
    duplicate_entries = {line: line_numbers for line, line_numbers in line_dict.items() if len(line_numbers) > 1}

    # Write the duplicate lines and their line numbers to the output file
    with open(output_file, 'w') as file:
        for line, line_numbers in duplicate_entries.items():
            file.write(f"Line Content: {line}\nLine Numbers: {', '.join(map(str, line_numbers))}\n\n")

        # Add total count of duplicate lines at the end of the file
        total_count = sum(len(line_numbers) - 1 for line_numbers in duplicate_entries.values())
        file.write(f"Total Duplicate Lines: {total_count}")
    print("Finished finding Duplicates -> Stored in duplicates.txt")

def remove_duplicate_lines(input_file, output_file):
    # Read lines from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Remove duplicates while maintaining the order
    unique_lines = list(dict.fromkeys(lines))

    # Write unique lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(unique_lines)

def get_public_key_formats_from_crt(crt_file_path):
    try:
        with open(crt_file_path, "rb") as crt_file:
            crt_data = crt_file.read()

        # Parse the CRT file using cryptography library
        cert = x509.load_pem_x509_certificate(crt_data, default_backend())

        # Extract the public key components
        public_key = cert.public_key()
        public_numbers = public_key.public_numbers()

        # Get modulus in decimal format
        modulus_decimal = public_numbers.n

        return modulus_decimal
    except Exception as e:
        #print(f"No number {crt_file_path}")
        return None

def process_certificate_files(folder_path, modulus_output_file):
    try:
        with open(modulus_output_file, "a") as modulus_file:
            for filename in os.listdir(folder_path):
                if filename.endswith(".crt"):
                    crt_file_path = os.path.join(folder_path, filename)
                    modulus_decimal = get_public_key_formats_from_crt(crt_file_path)

                    if modulus_decimal is not None:
                        # Acquire the lock before writing to the files
                        with file_write_lock:
                            modulus_file.write(f"{modulus_decimal}\n")
    except Exception as e:
        print(f"Error: {e}")
        pass

if __name__ == '__main__':
    # Parameters for public key collection
    folder_path = "Certificates"  # Update this to the path of your folder
    modulus_output_file = "Key_with_duplicates_unsorted.txt"
    print("Putting all public keys in a text file")
    process_certificate_files(folder_path, modulus_output_file)

    # Finding and counting duplicates
    input_find_dub = modulus_output_file
    output_dup = 'Key_duplicates.txt'
    print(f"Finding all duplicates and putting them in file {output_dup}")
    find_duplicate_lines(input_find_dub, output_dup)
    
    # Sorting keys by length
    input_to_sort = modulus_output_file
    output_sorting_key = 'Key_with_duplicates_sorted.txt'
    print(f"Sorting the keys and putting them in {output_sorting_key}")
    sort_lines_by_length(input_to_sort, output_sorting_key)

    # Creating a new file without duplicates
    input_file_removing_dup = output_sorting_key
    output_file_path = 'Key_without&sorted.txt'
    print(f"Creating a new file without duplicates\nOutput folder -> {output_file_path}")
    remove_duplicate_lines(input_file_removing_dup, output_file_path)
        
