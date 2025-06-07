import os
import re
import io
import requests
from datetime import datetime
from bs4 import BeautifulSoup, NavigableString, Tag
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

OPTION_SPACING = 1.0
QUESTION_HEADER_SPACING = 1.2
QUESTION_ANSWER_SPACING = 1.2


def parse_quiz_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    questions = soup.find_all("div", class_="display_question")
    return questions

def extract_question_info(question_soup):
    question_text_div = question_soup.find("div", class_="question_text")
    question_header = question_soup.find("div", class_="header")
    question_number_raw = (
        question_header.find("span", class_="name question_name").get_text(strip=True)
        if question_header
        else "Question"
    )
    question_number_cleaned = re.sub(
        r"(Partial|IncorrectQuestion|CorrectQuestion)", "", question_number_raw
    ).strip()
    if not question_number_cleaned.lower().startswith("question"):
        question_number_cleaned = "Question " + question_number_cleaned
    question_number = question_number_cleaned

    points_awarded, points_possible = 0.0, 0.0
    user_points_elem = question_soup.find("div", class_="user_points")
    possible_points_elem = question_soup.find("span", class_="points question_points")

    if user_points_elem:
        match = re.search(r"([\d.]+)", user_points_elem.get_text(strip=True))
        points_awarded = float(match.group(1)) if match else 0.0
    if possible_points_elem:
        match = re.search(r"([\d.]+)", possible_points_elem.get_text(strip=True))
        points_possible = float(match.group(1)) if match else 0.0

    is_correct = points_possible > 0 and points_awarded >= points_possible

    return {
        "number": question_number,
        "points_awarded": points_awarded,
        "points_possible": points_possible,
        "is_correct": is_correct,
        "question_text_div": question_text_div,
        "question_soup": question_soup,
    }

def extract_answers_info(question_soup, question_is_correct):
    answers = []
    answer_divs = question_soup.find_all("div", class_="answer")

    any_answer_correct_marked = any(
        answer.find("span", class_="answer_arrow correct") for answer in answer_divs
    )

    for answer in answer_divs:
        answer_text_div = answer.find("div", class_="answer_text") or answer.find(
            "div", class_="answer_label"
        )
        text = (
            answer_text_div.get_text(strip=True).replace("\u00a0", " ")
            if answer_text_div
            else "No answer text found."
        )
        is_selected = "selected_answer" in answer.get("class", [])
        if any_answer_correct_marked:
            is_correct = bool(answer.find("span", class_="answer_arrow correct"))
        else:
            if is_selected:
                is_correct = question_is_correct
            else:
                is_correct = False
        answers.append({"text": text, "selected": is_selected, "correct": is_correct})

    return answers

def write_pdf_text(
    c,
    text,
    left_margin,
    right_margin,
    current_y,
    line_height,
    font_name="Courier",
    font_size=12,
):
    max_width = right_margin - left_margin
    words = text.split()
    line = ""
    for word in words:
        test_line = line + word + " "
        if c.stringWidth(test_line, font_name, font_size) > max_width:
            c.drawString(left_margin, current_y, line.strip())
            current_y -= line_height
            line = word + " "
            if current_y < 1 * inch:
                c.showPage()
                current_y = letter[1] - 1 * inch
        else:
            line = test_line
    if line:
        c.drawString(left_margin, current_y, line.strip())
        current_y -= line_height
        if current_y < 1 * inch:
            c.showPage()
            current_y = letter[1] - 1 * inch
    return current_y

def write_question_text_and_images(
    question_text_div,
    txt_file,
    md_file,
    c,
    current_y,
    left_margin,
    right_margin,
    line_height,
    file_path,
):
    input_folder = os.path.dirname(file_path)
    for child in question_text_div.children:
        if isinstance(child, NavigableString):
            text = str(child).strip()
            if text:
                txt_file.write(text + "\n")
                md_file.write(text + "\n\n")
                c.setFont("Courier", 10)
                current_y = write_pdf_text(
                    c, text, left_margin, right_margin, current_y, line_height
                )
        elif isinstance(child, Tag):
            if child.name == "p":
                para_text = child.get_text(" ", strip=True).replace("\xa0", " ")
                txt_file.write(para_text + "\n\n")
                md_file.write(para_text + "\n\n")
                c.setFont("Courier", 10)
                current_y = write_pdf_text(
                    c, para_text, left_margin, right_margin, current_y, line_height
                )

                images = child.find_all("img")
                for img in images:
                    img_src = img.get("src")
                    if img_src:
                        md_file.write(f"![Image]({img_src})\n\n")
                        txt_file.write(f"[Image: {img_src}]\n\n")
                        try:
                            if img_src.startswith(("http://", "https://")):
                                response = requests.get(img_src)
                                img_data = io.BytesIO(response.content)
                            else:
                                img_data = os.path.join(input_folder, img_src)
                            img_reader = ImageReader(img_data)
                            iw, ih = img_reader.getSize()
                            max_img_width = right_margin - left_margin
                            max_img_height = current_y - 1 * inch
                            scale = min(max_img_width / iw, max_img_height / ih, 1.0)
                            iw_scaled = iw * scale
                            ih_scaled = ih * scale
                            c.drawImage(
                                img_reader,
                                left_margin,
                                current_y - ih_scaled,
                                width=iw_scaled,
                                height=ih_scaled,
                            )
                            current_y -= ih_scaled + 10
                        except Exception as e:
                            print(f"Could not add image {img_src} to PDF: {e}")

            elif child.name == "img":
                img_src = child.get("src")
                if img_src:
                    md_file.write(f"![Image]({img_src})\n\n")
                    txt_file.write(f"[Image: {img_src}]\n\n")
                    try:
                        if img_src.startswith(("http://", "https://")):
                            response = requests.get(img_src)
                            img_data = io.BytesIO(response.content)
                        else:
                            img_data = os.path.join(input_folder, img_src)
                        img_reader = ImageReader(img_data)
                        iw, ih = img_reader.getSize()
                        max_img_width = right_margin - left_margin
                        max_img_height = current_y - 1 * inch
                        scale = min(max_img_width / iw, max_img_height / ih, 1.0)
                        iw_scaled = iw * scale
                        ih_scaled = ih * scale
                        c.drawImage(
                            img_reader,
                            left_margin,
                            current_y - ih_scaled,
                            width=iw_scaled,
                            height=ih_scaled,
                        )
                        current_y -= ih_scaled + 10
                    except Exception as e:
                        print(f"Could not add image {img_src} to PDF: {e}")

            else:
                current_y = write_question_text_and_images(
                    child,
                    txt_file,
                    md_file,
                    c,
                    current_y,
                    left_margin,
                    right_margin,
                    line_height,
                    file_path,
                )
    return current_y

def draw_page_header_footer(
    c, class_name, quiz_number, total_points_earned, total_points_possible, page_num
):
    page_width = letter[0]
    y_header = letter[1] - 0.25 * inch
    header_text = f"{class_name} - Quiz {quiz_number} - Score: {total_points_earned}/{total_points_possible}"
    text_width = c.stringWidth(header_text, "Courier-Bold", 10)
    x_header = (page_width - text_width) / 2
    c.setFont("Courier-Bold", 10)
    c.drawString(x_header, y_header, header_text)
    footer_text = f"Page {page_num}"
    footer_y = 0.5 * inch
    text_width = c.stringWidth(footer_text, "Courier", 8)
    c.setFont("Courier", 8)
    c.drawString((page_width - text_width) / 2, footer_y, footer_text)

def estimate_question_height(question_info, answers_info, line_height):
    question_lines = (
        len(question_info["question_text_div"].get_text(" ", strip=True)) // 80 + 1
        if question_info["question_text_div"]
        else 1
    )
    answer_lines = sum(len(ans["text"]) // 80 + 1 for ans in answers_info)
    image_height = 0
    if question_info["question_text_div"]:
        images = question_info["question_text_div"].find_all("img")
        image_height = min(len(images), 2) * 100
    padding_lines = 6
    total_lines = question_lines + answer_lines + padding_lines
    total_height = total_lines * line_height + image_height
    return total_height

def draw_question_header(c, x, y, full_heading):
    c.setFont("Courier-Bold", 12)
    c.drawString(x, y, full_heading)

def draw_answer_line(c, x, y, prefix, answer_text):
    unicode_symbols = {"✓", "✕", "◯", "⌕"}
    if prefix and prefix[0] in unicode_symbols:
        symbol = prefix[0]
        rest = prefix[1:].strip()
    else:
        symbol = ""
        rest = prefix

    if symbol:
        c.setFont("Courier-Bold", 10)
        c.drawString(x, y, symbol)
        symbol_width = c.stringWidth(symbol, "Courier-Bold", 10)
    else:
        symbol_width = 0

    c.setFont("Courier-Bold", 10)
    c.drawString(x + symbol_width + 2, y, rest)
    rest_width = c.stringWidth(rest, "Courier-Bold", 10)

    c.setFont("Courier", 10)
    c.drawString(x + symbol_width + rest_width + 8, y, answer_text)

def write_question_to_files(
    question_info,
    answers_info,
    txt_file,
    md_file,
    c,
    current_y,
    left_margin,
    right_margin,
    line_height,
    question_index,
    file_path,
    class_name,
    quiz_number,
    total_points_earned,
    total_points_possible,
    page_num,
    only_show_correct=False,
    add_quiz_header=False,
):
    separator = "-" * 40
    page_bottom_margin = 1 * inch
    estimated_height = estimate_question_height(
        question_info, answers_info, line_height
    )
    if current_y - estimated_height < page_bottom_margin:
        c.showPage()
        page_num += 1
        draw_page_header_footer(
            c,
            class_name,
            quiz_number,
            total_points_earned,
            total_points_possible,
            page_num,
        )
        current_y = letter[1] - 1 * inch

    partial_credit = (
        0 < question_info["points_awarded"] < question_info["points_possible"]
    )
    if question_info["is_correct"]:
        status_text = "✓ CORRECT"
    elif partial_credit:
        status_text = "◯ PARTIAL CREDIT"
    else:
        status_text = "✕ INCORRECT"

    points_str = (
        f"{question_info['points_awarded']}/{question_info['points_possible']} pts"
    )
    full_heading = f"{question_info['number']}: {status_text} - {points_str}"

    if add_quiz_header:
        short_class_name = class_name.split()[0].upper() if class_name else ""
        full_heading += f" - QUIZ {quiz_number.upper()} - {short_class_name}"

    for f in [txt_file, md_file]:
        f.write(separator + "\n")

    txt_file.write(f"{full_heading.upper()}\n\n")
    md_file.write(f"**{full_heading}**\n\n")

    draw_question_header(c, left_margin, current_y, full_heading)
    current_y -= line_height * QUESTION_HEADER_SPACING

    c.setFont("Courier", 10)

    has_images = bool(question_info["question_text_div"].find_all("img"))
    if has_images:
        current_y = write_question_text_and_images(
            question_info["question_text_div"],
            txt_file,
            md_file,
            c,
            current_y,
            left_margin,
            right_margin,
            line_height,
            file_path,
        )
    else:
        question_text = (
            question_info["question_text_div"]
            .get_text(" ", strip=True)
            .replace("\xa0", " ")
        )
        txt_file.write(question_text + "\n\n")
        md_file.write(question_text + "\n\n")
        current_y = write_pdf_text(
            c, question_text, left_margin, right_margin, current_y, line_height
        )

    md_file.write("\n\n")

    txt_file.write("\n")

    current_y -= line_height * QUESTION_ANSWER_SPACING

    if only_show_correct and question_info["is_correct"]:
        answers_to_show = [
            ans for ans in answers_info if ans["selected"] and ans["correct"]
        ]
    else:
        answers_to_show = answers_info

    for idx, answer in enumerate(answers_to_show, 1):
        option_number = f"Option {idx}:"
        if answer["selected"]:
            if answer["correct"]:
                prefix_text = "✓ Selected Correct: "
            else:
                prefix_text = (
                    "⌕ Selected Possibly: "
                    if partial_credit
                    else "✕ Selected Incorrect: "
                )
            prefix = prefix_text + option_number
        else:
            prefix = option_number

        txt_file.write(f"   {prefix} {answer['text']}\n")
        md_file.write(f"- {prefix} {answer['text']}\n\n")
        draw_answer_line(
            c, left_margin + 10, current_y, prefix, answer["text"]
        )
        current_y -= line_height * OPTION_SPACING

    c.setLineWidth(1.2)
    c.line(left_margin, current_y - 5, right_margin, current_y - 5)
    current_y -= 20

    for f in [txt_file, md_file]:
        f.write("\n")
    md_file.write("\n---\n\n")

    return current_y, page_num

def process_taken_quiz(
    file_path,
    output_file_base,
    quiz_number,
    class_name,
    only_show_correct=False,
    add_quiz_header=False,
):
    questions = parse_quiz_html(file_path)
    txt_path = output_file_base + ".txt"
    md_path = output_file_base + ".md"
    pdf_path = output_file_base + ".pdf"
    txt_file = open(txt_path, "w", encoding="utf-8")
    md_file = open(md_path, "w", encoding="utf-8")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    left_margin = 0.25 * inch
    right_margin = letter[0] - 0.25 * inch
    line_height = 14
    current_y = letter[1] - 1 * inch
    date_str = datetime.now().strftime("%Y-%m-%d")
    header = f"Quiz {quiz_number} - {class_name} - {date_str}"
    separator = "-" * 40
    for f in [txt_file, md_file]:
        f.write(header + "\n")
        f.write(separator + "\n")
    total_points_earned = 0.0
    total_points_possible = 0.0
    for question in questions:
        user_points_elem = question.find("div", class_="user_points")
        possible_points_elem = question.find("span", class_="points question_points")
        points_awarded = 0.0
        points_possible = 0.0
        if user_points_elem:
            m = re.search(r"([\d.]+)", user_points_elem.get_text(strip=True))
            points_awarded = float(m.group(1)) if m else 0.0
        if possible_points_elem:
            m = re.search(r"([\d.]+)", possible_points_elem.get_text(strip=True))
            points_possible = float(m.group(1)) if m else 0.0
        total_points_earned += points_awarded
        total_points_possible += points_possible
    md_file.write(f"# Quiz {quiz_number} - {class_name} - {date_str}\n\n")
    md_file.write(
        f"**Total Score:** {total_points_earned}/{total_points_possible} pts\n\n"
    )
    page_num = 1
    draw_page_header_footer(
        c, class_name, quiz_number, total_points_earned, total_points_possible, page_num
    )
    for i, question in enumerate(questions, 1):
        question_info = extract_question_info(question)
        answers_info = extract_answers_info(question, question_info["is_correct"])
        current_y, page_num = write_question_to_files(
            question_info,
            answers_info,
            txt_file,
            md_file,
            c,
            current_y,
            left_margin,
            right_margin,
            line_height,
            i,
            file_path,
            class_name,
            quiz_number,
            total_points_earned,
            total_points_possible,
            page_num,
            only_show_correct=only_show_correct,
            add_quiz_header=add_quiz_header,
        )
    txt_file.close()
    md_file.close()
    c.save()


def process_taken_quiz_multiple_files_with_quiznum(
    all_questions,  # list of tuples (file_path, question_soup, quiz_number)
    output_file_base,
    class_name,
    only_show_correct=False,
    add_quiz_header=False,
):
    """
    Batch process multiple taken quizzes with per-question quiz_number,
    preserving your existing formatting exactly.
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch

    txt_path = output_file_base + ".txt"
    md_path = output_file_base + ".md"
    pdf_path = output_file_base + ".pdf"

    txt_file = open(txt_path, "w", encoding="utf-8")
    md_file = open(md_path, "w", encoding="utf-8")
    c = canvas.Canvas(pdf_path, pagesize=letter)

    left_margin = 0.25 * inch
    right_margin = letter[0] - 0.25 * inch
    line_height = 14
    current_y = letter[1] - 1 * inch
    page_num = 1

    total_points_earned = 0.0
    total_points_possible = 0.0

    # Draw header for batch with generic "Batch" quiz label
    def draw_header():
        page_width = letter[0]
        y_header = letter[1] - 0.25 * inch
        header_text = f"{class_name} - Batch - Score: {total_points_earned}/{total_points_possible}"
        text_width = c.stringWidth(header_text, "Courier-Bold", 10)
        x_header = (page_width - text_width) / 2
        c.setFont("Courier-Bold", 10)
        c.drawString(x_header, y_header, header_text)
        footer_text = f"Page {page_num}"
        footer_y = 0.5 * inch
        text_width = c.stringWidth(footer_text, "Courier", 8)
        c.setFont("Courier", 8)
        c.drawString((page_width - text_width) / 2, footer_y, footer_text)

    draw_header()

    question_counter = 1

    for file_path, question, quiz_number in all_questions:
        # Extract info with your existing extractor
        question_info = extract_question_info(question)
        answers_info = extract_answers_info(question, question_info["is_correct"])

        total_points_earned += question_info["points_awarded"]
        total_points_possible += question_info["points_possible"]

        # Override question number to include quiz number and class
        # if add_quiz_header:
        #     question_info["number"] = f"{quiz_number} - {question_info['number']}"

        current_y, page_num = write_question_to_files(
            question_info,
            answers_info,
            txt_file,
            md_file,
            c,
            current_y,
            left_margin,
            right_margin,
            line_height,
            question_counter,
            file_path,
            class_name,
            quiz_number,
            total_points_earned,
            total_points_possible,
            page_num,
            only_show_correct,
            add_quiz_header,
        )
        question_counter += 1

    txt_file.close()
    md_file.close()
    c.save()


def process_untaken_quiz_multiple_files_with_quiznum(
    all_questions,  # list of tuples (file_path, question_soup, quiz_number)
    output_file_base,
    class_name,
    add_quiz_header=False,
):
    """
    Batch process multiple untaken quizzes with per-question quiz_number,
    preserving your existing formatting exactly.
    """
    txt_path = output_file_base + ".txt"
    md_path = output_file_base + ".md"
    pdf_path = output_file_base + ".pdf"

    txt_file = open(txt_path, "w", encoding="utf-8")
    md_file = open(md_path, "w", encoding="utf-8")
    c = canvas.Canvas(pdf_path, pagesize=letter)

    left_margin = 0.25 * inch
    right_margin = letter[0] - 0.25 * inch
    line_height = 14
    current_y = letter[1] - 1 * inch
    page_num = 1

    def draw_header():
        page_width = letter[0]
        y_header = letter[1] - 0.25 * inch
        header_text = f"{class_name} - Batch"
        text_width = c.stringWidth(header_text, "Courier-Bold", 10)
        x_header = (page_width - text_width) / 2
        c.setFont("Courier-Bold", 10)
        c.drawString(x_header, y_header, header_text)
        footer_text = f"Page {page_num}"
        footer_y = 0.5 * inch
        text_width = c.stringWidth(footer_text, "Courier", 8)
        c.setFont("Courier", 8)
        c.drawString((page_width - text_width) / 2, footer_y, footer_text)

    draw_header()

    question_counter = 1

    for file_path, question, quiz_number in all_questions:
        question_header = question.find("div", class_="header")
        question_number_raw = (
            question_header.find("span", class_="name question_name").get_text(strip=True)
            if question_header else "Question"
        )
        question_number_cleaned = re.sub(
            r"(Partial|IncorrectQuestion|CorrectQuestion)", "", question_number_raw
        ).strip()
        if not question_number_cleaned.lower().startswith("question"):
            question_number_cleaned = "Question " + question_number_cleaned

        # if add_quiz_header:
        #     question_number_cleaned = f"{quiz_number} - {class_name} - {question_number_cleaned}"

        question_text_div = question.find("div", class_="question_text")
        question_text = (
            question_text_div.get_text(" ", strip=True).replace("\xa0", " ")
            if question_text_div
            else ""
        )

        txt_file.write(f"{question_number_cleaned.upper()}\n\n")
        txt_file.write(question_text + "\n\n")
        md_file.write(f"**{question_number_cleaned}**\n\n")
        md_file.write(question_text + "\n\n")

        answers = question.find_all("div", class_="answer")
        for idx_ans, answer in enumerate(answers, 1):
            answer_text_div = answer.find("div", class_="answer_text") or answer.find("div", class_="answer_label")
            answer_text = (
                answer_text_div.get_text(strip=True).replace("\xa0", " ")
                if answer_text_div
                else "No answer text found."
            )
            txt_file.write(f"Option {idx_ans}: {answer_text}\n")
            md_file.write(f"- Option {idx_ans}: {answer_text}\n\n")

        txt_file.write("\n")
        md_file.write("\n---\n\n")

        question_counter += 1

    txt_file.close()
    md_file.close()
    c.save()
