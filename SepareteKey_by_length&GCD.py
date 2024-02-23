import os
import math
import sys
from batch_gcd import batch_gcd

# Increase the limit for integer string conversion
sys.set_int_max_str_digits(6000)

def create_files_by_length(input_file, output_folder):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Dictionary to store lines based on their length
    lines_by_length = {}

    for line in lines:
        length = len(line.strip())
        if length not in lines_by_length:
            lines_by_length[length] = []

        lines_by_length[length].append(line)

    # Create a directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Create separate files for each length within the specified folder
    for length, lines_list in lines_by_length.items():
        output_file = os.path.join(output_folder, f'output_length_{length}.txt')
        with open(output_file, 'w') as file:
            file.writelines(lines_list)

    print(f"Files created successfully in the '{output_folder}' folder!")

def gcd_test(numbers):
    # Calculate the GCD for a list of numbers
    result = numbers[0]
    for number in numbers[1:]:
        result = math.gcd(result, number)
    return result

def apply_gcd_test_to_files(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            print(f"testing for file : {filepath}")
            with open(filepath, 'r') as file:
                lines = file.readlines()

            # Convert lines to integers for GCD calculation
            numbers = [int(line.strip()) for line in lines]

            # Apply GCD test
            result = batch_gcd(*numbers)

            output_filename = f'gcd_{filename}.txt'
            with open(output_filename, 'w') as output_file:
                # Write filename as the first line
                output_file.write(f"Filename: {filename}\n")
        
                # Write the list of numbers
                output_file.write(f"{result}\n")


# Usage example
folder_name = 'Separated_key_byLength'
create_files_by_length('key_without&sorted.txt', folder_name)
apply_gcd_test_to_files(folder_name)