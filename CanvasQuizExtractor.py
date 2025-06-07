"""
Canvas:   Quiz Extractor
Author:   Matthew Baker
Brief:    Takes HTML file of Quiz results from Canvas and creates
          easy to read Text, Markdown, and PDF documents for studying or flash cards.
Version:  0.3
Date:     2025-06-06
"""

import os
from datetime import datetime
from bs4 import BeautifulSoup
import HTML_Extract
import FileProcess


# Function to read class info from CurrentClasses.txt
def read_classes_from_file(filename):
    try:
        with open(filename, "r") as file:
            classes = [line.strip() for line in file.readlines() if line.strip()]
        return classes
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return []


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

    # Extra info option
    while True:
        extra_info_input = input(
            "Is there any extra information for this quiz? (1 for yes, 0 for no): "
        ).strip()
        if extra_info_input == "1":
            extra_info = input("Please enter the extra information: ")
            quiz_number = quiz_number + " - " + extra_info
            break
        elif extra_info_input == "0":
            break
        else:
            print("Invalid input. Please enter '1' or '0'.")

    # NEW PROMPT: Ask if quiz number and class should be added to question headers
    while True:
        add_quiz_header = input(
            "Do you want to add the Quiz Number and Class to each question header? (y/n): "
        ).strip().lower()
        if add_quiz_header in ("y", "n"):
            add_quiz_header_flag = add_quiz_header == "y"
            break
        print("Please enter 'y' or 'n'.")

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
            input("Only show correct answer for fully correct questions? (y/n): ")
            .strip()
            .lower()
        )
        if answer in ["y", "n"]:
            return answer == "y"
        print("Please enter 'y' or 'n'.")


def main():
    extraction_method = choose_extraction_method()

    only_show_correct = False
    if extraction_method == 1:
        only_show_correct = ask_only_show_correct()

    files = FileProcess.list_files()
    if not files:
        print("No input files found.")
        return

    input_file = FileProcess.choose_input_file(files)
    if not input_file:
        print("No file selected.")
        return

    quiz_number, class_name, add_quiz_header_flag = choose_quiz_and_class()

    output_file_base = FileProcess.choose_output_file(quiz_number, class_name)
    if output_file_base is None:
        print("Output file creation cancelled.")
        return

    if extraction_method == 1:
        # Pass only_show_correct and add_quiz_header_flag to process_taken_quiz
        HTML_Extract.process_taken_quiz(
            input_file,
            output_file_base,
            quiz_number,
            class_name,
            only_show_correct,
            add_quiz_header_flag,
        )
        print(
            f"\nResults saved to:\n - {output_file_base}.txt\n - {output_file_base}.md\n - {output_file_base}.pdf"
        )
    elif extraction_method == 2:
        # Pass add_quiz_header_flag to untaken quiz processing as well (optional)
        HTML_Extract.process_untaken_quiz(
            input_file,
            output_file_base,
            quiz_number,
            class_name,
            add_quiz_header_flag,
        )
        print(
            f"\nResults saved to:\n - {output_file_base}.txt\n - {output_file_base}.md\n - {output_file_base}.pdf"
        )
    else:
        print("ERROR - No matching Extraction Method")


if __name__ == "__main__":
    main()
