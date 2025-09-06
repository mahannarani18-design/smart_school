import google.generativeai as genai
from openai import OpenAI
from django.core.management.base import BaseCommand
from decouple import config
import json

class Command(BaseCommand):
    help = 'Generates sample questions using a specified AI model (gemini or chatgpt)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Specifies the AI model to use: "gemini" or "chatgpt"',
            default='gemini' # مدل پیش‌فرض
        )

    def _generate_with_gemini(self, text, subject_name):
        self.stdout.write("Connecting to Google AI (Gemini)...")
        GOOGLE_API_KEY = config('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        شما یک طراح سوال حرفه‌ای برای درس '{subject_name}' هستی.
        بر اساس متن زیر، 3 سوال چهارگزینه‌ای استاندارد طراحی کن.
        خروجی را فقط و فقط در فرمت JSON به صورت لیستی از آبجکت‌ها ارائه بده.
        هر آبجکت باید شامل کلیدهای "question_text", "answers" باشد.
        کلید "answers" باید لیستی از آبجکت‌ها باشد که هر کدام شامل "answer_text" و "is_correct" (boolean) است.
        متن: --- {text} ---
        """
        response = model.generate_content(prompt)
        return response.text

    def _generate_with_chatgpt(self, text, subject_name):
        self.stdout.write("Connecting to OpenAI (ChatGPT)...")
        OPENAI_API_KEY = config('OPENAI_API_KEY')
        client = OpenAI(api_key=OPENAI_API_KEY)

        prompt = f"""
        You are a professional question designer for the '{subject_name}' subject.
        Based on the following text, design 3 standard multiple-choice questions.
        Provide the output only and exclusively in JSON format as a list of objects.
        Each object must contain the keys "question_text" and "answers".
        The "answers" key must be a list of objects, each containing "answer_text" and "is_correct" (boolean).
        Text: --- {text} ---
        """ # ChatGPT با prompt انگلیسی بهتر کار می‌کند

        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # یا gpt-4
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content

    def handle(self, *args, **options):
        model_choice = options['model'].lower()

        sample_text = """
        قانون دوم نیوتن بیان می‌کند که نرخ تغییر تکانه خطی یک جسم برابر با نیروی خالص وارد بر آن جسم است. 
        این قانون به صورت فرمول F=ma نمایش داده می‌شود که در آن F نیروی خالص، m جرم جسم و a شتاب آن است.
        """
        subject_name = "فیزیک"

        try:
            if model_choice == 'gemini':
                raw_response = self._generate_with_gemini(sample_text, subject_name)
            elif model_choice == 'chatgpt':
                raw_response = self._generate_with_chatgpt(sample_text, subject_name)
            else:
                self.stderr.write(self.style.ERROR(f"Model '{model_choice}' is not supported. Use 'gemini' or 'chatgpt'."))
                return

            self.stdout.write("Generating questions...")
            cleaned_response = raw_response.strip().replace('`', '').replace('json', '')
            questions_data = json.loads(cleaned_response)

            self.stdout.write(self.style.SUCCESS(f"Successfully generated questions using {model_choice}:"))

            for i, q in enumerate(questions_data, 1):
                self.stdout.write(self.style.HTTP_INFO(f"\nسوال {i}: {q['question_text']}"))
                for j, ans in enumerate(q['answers']):
                    prefix = "[صحیح] " if ans['is_correct'] else "[غلط]   "
                    self.stdout.write(f"{prefix}گزینه {j+1}: {ans['answer_text']}")

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))