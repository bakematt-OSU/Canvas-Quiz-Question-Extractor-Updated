"""
Canvas:   Quiz Extractor
Author:   Matthew Baker
Brief:    Takes one or more HTML files of Quiz results from Canvas and creates
          easy to read Text, Markdown, and PDF documents for studying or flash cards.
Version:  0.8
Date:     2025-06-07
"""

import os
from datetime import datetime
import HTML_Extract
import FileProcess


def read_classes_from_file(filename):
    try:
        with open(filename, "r") as file:
            classes = [line.strip() for line in file.readlines() if line.strip()]
        return classes
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return []


def choose_class_only():
    classes = read_classes_from_file("CurrentClasses.txt")
    print("Available options:")
    print("0. Enter class info manually")

    if classes:
        for idx, class_info in enumerate(classes, 1):
            print(f"{idx}. {class_info}")

    while True:
        try:
            choice = int(input("\nSelect a class by number: "))
            if choice == 0:
                class_name = input("Enter the class name manually: ")
                break
            elif 1 <= choice <= len(classes):
                class_name = classes[choice - 1]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    return class_name


def choose_quiz_info_for_file(filename):
    print(f"\nProcessing quiz file: {os.path.basename(filename)}")
    quiz_number = input("Enter the quiz number or extra info for this quiz: ").strip()
    if not quiz_number:
        quiz_number = "UnknownQuiz"
    return quiz_number


def choose_quiz_and_class():
    classes = read_classes_from_file("CurrentClasses.txt")
    print("Available options:")
    print("0. Enter class info manually")

    if classes:
        for idx, class_info in enumerate(classes, 1):
            print(f"{idx}. {class_info}")

    while True:
        try:
            choice = int(input("\nSelect a class by number: "))
            if choice == 0:
                class_name = input("Enter the class name manually: ")
                quiz_number = input("Enter the quiz number: ")
                break
            elif 1 <= choice <= len(classes):
                class_name = classes[choice - 1]
                quiz_number = input(f"Enter the quiz number for {class_name}: ")
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        extra_info_input = input(
            "Is there any extra information for this quiz? (1/y for yes, 0/n for no): "
        ).strip().lower()
        if extra_info_input in ("1", "y"):
            extra_info = input("Please enter the extra information: ")
            quiz_number = quiz_number + " - " + extra_info
            break
        elif extra_info_input in ("0", "n"):
            break
        else:
            print("Invalid input. Please enter '1', '0', 'y', or 'n'.")

    while True:
        add_quiz_header = input(
            "Do you want to add the Quiz Number and Class to each question header? (1/y for yes, 0/n for no): "
        ).strip().lower()
        if add_quiz_header in ("1", "y", "0", "n"):
            add_quiz_header_flag = add_quiz_header in ("1", "y")
            break
        print("Please enter '1', '0', 'y', or 'n'.")

    return quiz_number, class_name, add_quiz_header_flag


def choose_extraction_method():
    while True:
        print("\nSelect the quiz extraction method:")
        print(
            "1. Taken Quiz Extraction ➡ Returns: Questions, Answers, marks Correct/Incorrect"
        )
        print("2. Untaken Quiz Extraction ➡ Returns: Questions, Possible Options")
        try:
            choice = int(input("\nEnter the number of your choice: "))
            if choice in [1, 2]:
                return choice
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def ask_only_show_correct():
    while True:
        answer = (
            input("Only show correct answer for fully correct questions? (1/y for yes, 0/n for no): ")
            .strip()
            .lower()
        )
        if answer in ["1", "y", "0", "n"]:
            return answer in ["1", "y"]
        print("Please enter '1', '0', 'y', or 'n'.")


def choose_processing_mode():
    while True:
        mode = input("\nProcess a single file or batch (multiple files/folder)? (s (1) / b (2)): ").strip().lower()
        if mode in ('s', 'single', '1'):
            return 'single'
        elif mode in ('b', 'batch', '2'):
            return 'batch'
        else:
            print("Please enter 's' or '1' for single or 'b' or '2' for batch.")


def main():
    extraction_method = choose_extraction_method()

    processing_mode = choose_processing_mode()

    files = FileProcess.list_files()
    if not files:
        print("No input files found.")
        return

    if processing_mode == 'single':
        input_file = FileProcess.choose_input_file(files)
        if not input_file:
            print("No file selected.")
            return
        input_files = [input_file]

        quiz_number, class_name, add_quiz_header_flag = choose_quiz_and_class()

    else:  # batch mode
        input_files = FileProcess.choose_input_files_with_folders()
        if not input_files:
            print("No files selected.")
            return

        class_name = choose_class_only()
        add_quiz_header_flag = True  # force in batch mode

        quiz_numbers_per_file = {}
        for file in input_files:
            quiz_num = choose_quiz_info_for_file(file)
            quiz_numbers_per_file[file] = quiz_num

    only_show_correct = False
    if extraction_method == 1:
        only_show_correct = ask_only_show_correct()

    combine_output = input("Combine all quizzes into a single output file? (y/n): ").strip().lower() in ("y", "1", "yes")

    if combine_output:
        if processing_mode == 'batch':
            # Prompt user explicitly for output base filename in batch mode
            user_base_name = input("Enter base name for combined output files (no extension): ").strip()
            if not user_base_name:
                user_base_name = "Batch_Quiz_Output"
            output_file_base = os.path.join(FileProcess.OUTPUT_FOLDER, user_base_name)
        else:
            output_file_base = FileProcess.choose_output_file(quiz_number, class_name)
            if output_file_base is None:
                print("Output file creation cancelled.")
                return

        if processing_mode == 'batch':
            all_questions = []
            for file in input_files:
                questions = HTML_Extract.parse_quiz_html(file)
                quiz_num = quiz_numbers_per_file.get(file, "UnknownQuiz")
                all_questions.extend([(file, q, quiz_num) for q in questions])

            if extraction_method == 1:
                HTML_Extract.process_taken_quiz_multiple_files_with_quiznum(
                    all_questions,
                    output_file_base,
                    class_name,
                    only_show_correct,
                    add_quiz_header_flag,
                )
            else:
                HTML_Extract.process_untaken_quiz_multiple_files_with_quiznum(
                    all_questions,
                    output_file_base,
                    class_name,
                    add_quiz_header_flag,
                )

            print(
                f"\nCombined results saved to:\n - {output_file_base}.txt\n - {output_file_base}.md\n - {output_file_base}.pdf"
            )
        else:
            # Single mode combined (rare)
            questions = HTML_Extract.parse_quiz_html(input_files[0])
            if extraction_method == 1:
                HTML_Extract.process_taken_quiz(
                    input_files[0],
                    output_file_base,
                    quiz_number,
                    class_name,
                    only_show_correct,
                    add_quiz_header_flag,
                )
            else:
                HTML_Extract.process_untaken_quiz(
                    input_files[0],
                    output_file_base,
                    quiz_number,
                    class_name,
                    add_quiz_header_flag,
                )
            print(
                f"\nResults saved to:\n - {output_file_base}.txt\n - {output_file_base}.md\n - {output_file_base}.pdf"
            )
    else:
        if processing_mode == 'batch':
            for file in input_files:
                quiz_num = quiz_numbers_per_file.get(file, "UnknownQuiz")
                output_file_base = FileProcess.choose_output_file(quiz_num, class_name)
                if output_file_base is None:
                    print(f"Skipping output for {file} due to user choice.")
                    continue

                if extraction_method == 1:
                    HTML_Extract.process_taken_quiz(
                        file,
                        output_file_base,
                        quiz_num,
                        class_name,
                        only_show_correct,
                        add_quiz_header_flag,
                    )
                else:
                    HTML_Extract.process_untaken_quiz(
                        file,
                        output_file_base,
                        quiz_num,
                        class_name,
                        add_quiz_header_flag,
                    )
                print(
                    f"\nResults saved for {file} to:\n - {output_file_base}.txt\n - {output_file_base}.md\n - {output_file_base}.pdf"
                )
        else:
            output_file_base = FileProcess.choose_output_file(quiz_number, class_name)
            if output_file_base is None:
                print("Output file creation cancelled.")
                return

            if extraction_method == 1:
                HTML_Extract.process_taken_quiz(
                    input_files[0],
                    output_file_base,
                    quiz_number,
                    class_name,
                    only_show_correct,
                    add_quiz_header_flag,
                )
            else:
                HTML_Extract.process_untaken_quiz(
                    input_files[0],
                    output_file_base,
                    quiz_number,
                    class_name,
                    add_quiz_header_flag,
                )
            print(
                f"\nResults saved to:\n - {output_file_base}.txt\n - {output_file_base}.md\n - {output_file_base}.pdf"
            )


if __name__ == "__main__":
    main()
