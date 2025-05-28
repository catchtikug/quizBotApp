import csv
import re
from django.core.management.base import BaseCommand
from home.models import Categories, Books, Chapters, Verses, Questions, QuestionOptions

class Command(BaseCommand):
    help = 'Import questions for the book of Acts from CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = 'acts_questions.csv'

        category, _ = Categories.objects.get_or_create(name="Old Testament")
        book, _ = Books.objects.get_or_create(name="Acts", category=category)

        def extract_chapter_verse(text):
            match = re.search(r'\(Acts\s+(\d+):(\d+)\)', text)
            if match:
                return int(match.group(1)), int(match.group(2))
            return None, None

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                question_text = row['question'].strip()
                chapter_num, verse_num = extract_chapter_verse(question_text)
                if not chapter_num or not verse_num:
                    continue

                print(f"Question {question_text} -- {chapter_num} Has been saved")
                
                chapter, _ = Chapters.objects.get_or_create(book=book, chapter_number=chapter_num)

                verse, _ = Verses.objects.get_or_create(
                    book=book,
                    chapter=chapter,
                    verse_number=verse_num,
                    defaults={'text': 'Placeholder verse text.'}
                )

                correct_option = row['correct_option'].strip().upper()
                options = {
                    'A': row['option_a'].strip(),
                    'B': row['option_b'].strip(),
                    'C': row['option_c'].strip(),
                    'D': row['option_d'].strip()
                }
                correct_answer = options.get(correct_option, '')

                question = Questions.objects.create(
                    book=book,
                    chapter=chapter,
                    verse=verse,
                    question=question_text,
                    correct_answer=correct_answer
                )

                for text in options.values():
                    QuestionOptions.objects.create(question=question, option=text)

        self.stdout.write(self.style.SUCCESS("✅ Acts questions imported successfully."))
