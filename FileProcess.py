import os
from datetime import datetime

# Define global variables for the input and output directories
INPUT_FOLDER = "Input"
OUTPUT_FOLDER = "Output"

def list_files():
    """
    Lists all files in the 'Input' directory.

    This function prints all the files available in the 'Input' directory
    and returns them as a list of file names.

    Returns:
        list: A list of filenames in the 'Input' directory.
    """
    if not os.path.exists(INPUT_FOLDER):
        print(f"The directory {INPUT_FOLDER} does not exist.")
        return []

    files = [f for f in os.listdir(INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, f))]
    if not files:
        print(f"There are no files in the {INPUT_FOLDER} directory.")
        return []

    print(f"\nAvailable files in the '{INPUT_FOLDER}' directory:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")

    return files


def choose_input_file(files):
    """
    Prompt user to select a single file from the 'Input' folder.

    Returns:
        str: Selected file path (including Input folder).
    """
    while True:
        try:
            choice = int(input("\nEnter the number of the file to process: "))
            if 1 <= choice <= len(files):
                return os.path.join(INPUT_FOLDER, files[choice - 1])
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_input_files_simple(files):
    """
    Prompt user to select multiple files (no folders).

    User inputs numbers separated by commas or 'all'.

    Returns:
        list of selected file paths.
    """
    print("\nAvailable files in the 'Input' directory:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")

    while True:
        choice = input("\nEnter numbers of files separated by commas, or 'all' for all files: ").strip().lower()
        if choice == 'all':
            return [os.path.join(INPUT_FOLDER, f) for f in files]

        indices = choice.split(',')
        try:
            selected = []
            for idx_str in indices:
                idx = int(idx_str.strip()) - 1
                if 0 <= idx < len(files):
                    selected.append(os.path.join(INPUT_FOLDER, files[idx]))
                else:
                    raise ValueError
            if selected:
                return selected
            else:
                print("No valid files selected. Please try again.")
        except ValueError:
            print("Invalid input. Enter valid numbers separated by commas or 'all'.")


def choose_input_files_with_folders():
    """
    Prompt user to select files and/or folders from the 'Input' directory.

    Lists files and folders with distinct numbering.

    Returns:
        list of selected file paths.
    """
    files = [f for f in os.listdir(INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, f))]
    folders = [d for d in os.listdir(INPUT_FOLDER) if os.path.isdir(os.path.join(INPUT_FOLDER, d))]

    print("\nAvailable files in the 'Input' directory:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. [FILE] {file}")

    folder_start_idx = len(files) + 1
    if folders:
        print("\nAvailable folders in the 'Input' directory:")
        for idx, folder in enumerate(folders, folder_start_idx):
            print(f"{idx}. [FOLDER] {folder}")

    total_options = len(files) + len(folders)

    while True:
        choice = input("\nEnter numbers of files/folders separated by commas, or 'all' for all files: ").strip().lower()
        if choice == 'all':
            return [os.path.join(INPUT_FOLDER, f) for f in files]

        indices = choice.split(',')
        try:
            selected_paths = []
            for idx_str in indices:
                idx = int(idx_str.strip())
                if 1 <= idx <= len(files):
                    selected_paths.append(os.path.join(INPUT_FOLDER, files[idx - 1]))
                elif len(files) < idx <= total_options:
                    folder_idx = idx - len(files) - 1
                    folder_name = folders[folder_idx]
                    folder_path = os.path.join(INPUT_FOLDER, folder_name)
                    folder_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                    if folder_files:
                        print(f"Adding {len(folder_files)} files from folder '{folder_name}'.")
                        selected_paths.extend(folder_files)
                    else:
                        print(f"Folder '{folder_name}' is empty, skipping.")
                else:
                    raise ValueError("Selection out of range.")
            if selected_paths:
                return selected_paths
            else:
                print("No valid files or folders selected. Please try again.")
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter valid numbers or 'all'.")


def choose_output_file(quiz_number, class_name):
    """
    Generate a base output file path based on quiz number, class name, and current date,
    in the Output folder. Does not add extension, so .txt, .md, .pdf can be appended.

    Args:
        quiz_number (str): The quiz number.
        class_name (str): The class name.

    Returns:
        str: The base path for output files WITHOUT extension.
    """
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    current_date = datetime.now().strftime('%Y-%m-%d')

    base_file_name = f"Quiz {quiz_number} - {class_name} - {current_date}"
    base_path = os.path.join(OUTPUT_FOLDER, base_file_name)

    def file_exists_with_ext(ext):
        return os.path.exists(base_path + ext)

    if any(file_exists_with_ext(ext) for ext in ['.txt', '.md', '.pdf']):
        while True:
            user_choice = input(
                f"Output files for '{base_file_name}' already exist. Overwrite? (y/n/1/0) or rename with attempt (a): "
            ).strip().lower()

            if user_choice in ('y', '1'):
                break
            elif user_choice in ('n', '0'):
                print("Choose a different quiz number or class name.")
                return None
            elif user_choice == 'a':
                attempt = 1
                while any(file_exists_with_ext(ext) for ext in ['.txt', '.md', '.pdf']):
                    base_file_name = f"Quiz {quiz_number} - {class_name} - {current_date} - Attempt {attempt}"
                    base_path = os.path.join(OUTPUT_FOLDER, base_file_name)
                    attempt += 1
                print(f"Renamed output base to '{base_file_name}'.")
                break
            else:
                print("Please enter 'y', 'n', '1', '0', or 'a'.")
    return base_path
