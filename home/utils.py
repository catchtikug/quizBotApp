import re
import csv
from PyPDF2 import PdfReader
import os

def extract_mc_questions(pdf_file):
    filename = os.path.basename(pdf_file)
    book_name = filename.split("_")[1] if "_" in filename else filename.split(".")[0]

    # Read text from PDF
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # Adjust regex pattern to your question format
    pattern = re.compile(
        r"(\d+)\.\s+(.*?)\n\s*A\.\s+(.*?)\n\s*B\.\s+(.*?)\n\s*C\.\s+(.*?)\n\s*D\.\s+(.*?)\n([A-D]):([A-Z]):(\w+):(\d+)",
        re.DOTALL
    )

    questions = []

    for match in pattern.finditer(text):
        questions.append([
            book_name,
            match.group(9),                      # book_code
            int(match.group(10)),                # chapter
            int(match.group(1)),                 # question_number
            match.group(2).strip(),              # question
            match.group(3).strip(),              # option A
            match.group(4).strip(),              # option B
            match.group(5).strip(),              # option C
            match.group(6).strip(),              # option D
            match.group(7).strip(),              # correct_option
            match.group(8).strip(),              # difficulty
        ])

    return questions

# ===== Run the script directly =====
pdf_file = "16_Nehemiah_MCQuestions.pdf"
output_csv = "nehemiah_questions.csv"

print(f"📄 Reading: {pdf_file}")
data = extract_mc_questions(pdf_file)

if data:
    headers = [
        "book_name", "book_code", "chapter", "question_number",
        "question", "option_a", "option_b", "option_c", "option_d",
        "correct_option", "difficulty"
    ]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"✅ Saved {len(data)} questions to {output_csv}")
else:
    print("⚠ No questions found. Check PDF formatting or regex.")
