import os
import shutil

def separate_folder(source_folder, target_folder_base, num_parts):
    # Create target folders
    for i in range(1, num_parts + 1):
        target_folder = os.path.join(target_folder_base, f"Cer_part_{i}")
        os.makedirs(target_folder, exist_ok=True)

    # Get the list of files in the source folder
    files = os.listdir(source_folder)

    # Calculate the number of files per part
    files_per_part = len(files) // num_parts
    remainder = len(files) % num_parts

    # Distribute files into target folders
    current_part = 1
    current_file_index = 0

    for i in range(num_parts):
        part_size = files_per_part + (1 if i < remainder else 0)
        target_folder = os.path.join(target_folder_base, f"Cer_part_{current_part}")

        for j in range(part_size):
            source_file = os.path.join(source_folder, files[current_file_index])
            target_file = os.path.join(target_folder, files[current_file_index])

            # Move the file to the target folder
            shutil.move(source_file, target_file)

            current_file_index += 1

        current_part += 1

if __name__ == "__main__":
    source_folder = "Certificates"  # Replace with the path to your source folder
    target_folder_base = "Cert_Part"  # Replace with the path to your target folder base
    num_parts = 13  # Change the number of parts to 10

    separate_folder(source_folder, target_folder_base, num_parts)
    print(f"Folder '{source_folder}' separated into {num_parts} parts (Cer_part_1, Cer_part_2, ..., Cer_part_10) in '{target_folder_base}'.")
