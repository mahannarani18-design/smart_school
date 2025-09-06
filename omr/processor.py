# مسیر: omr/processor.py

import cv2
import numpy as np

def process_omr_sheet(image_path):
    """
    این تابع یک مسیر عکس پاسخنامه را گرفته و پاسخ‌های دانش‌آموز را استخراج می‌کند.
    فرض بر این است که پاسخنامه دارای ستون‌های منظم و دایره‌های توپر است.
    """
    # این مقادیر باید بر اساس فرم پاسخنامه شما تنظیم شوند
    QUESTIONS_COUNT = 25  # تعداد کل سوالات در یک ستون
    OPTIONS_COUNT = 4     # تعداد گزینه‌ها برای هر سوال

    # ۱. خواندن و پیش‌پردازش تصویر
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # ۲. پیدا کردن کانتورها (اشکال)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    question_contours = []
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        aspect_ratio = w / float(h)

        # ۳. فیلتر کردن کانتورها برای پیدا کردن دایره‌های گزینه‌ها
        if w >= 15 and h >= 15 and 0.9 <= aspect_ratio <= 1.1:
            question_contours.append(c)

    # اگر تعداد کانتورهای پیدا شده درست نباشد، خطا برگردان
    if len(question_contours) != QUESTIONS_COUNT * OPTIONS_COUNT:
        print(f"Warning: Found {len(question_contours)} contours, expected {QUESTIONS_COUNT * OPTIONS_COUNT}")
        # در یک پروژه واقعی اینجا باید یک خطا مدیریت شود
        return None

    # ۴. مرتب‌سازی کانتورها از بالا به پایین
    question_contours = sorted(question_contours, key=lambda c: cv2.boundingRect(c)[1])

    answers = {}
    # ۵. گروه‌بندی کانتورها برای هر سوال
    for i in range(0, len(question_contours), OPTIONS_COUNT):
        question_num = (i // OPTIONS_COUNT) + 1

        # گزینه‌های یک سوال را بر اساس موقعیت افقی (از چپ به راست) مرتب کن
        options = sorted(question_contours[i:i+OPTIONS_COUNT], key=lambda c: cv2.boundingRect(c)[0])

        bubbled_index = -1  # -1 یعنی هیچ گزینه‌ای انتخاب نشده

        # ۶. پیدا کردن گزینه پر شده
        max_filled = 0
        for j, option_contour in enumerate(options):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [option_contour], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total_pixels = cv2.countNonZero(mask)

            if total_pixels > max_filled:
                max_filled = total_pixels
                bubbled_index = j

        # ثبت پاسخ دانش‌آموز (0=الف, 1=ب, 2=ج, 3=د)
        answers[question_num] = bubbled_index

    return answers