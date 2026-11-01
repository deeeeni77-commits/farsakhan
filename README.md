# فارساخوان | Persian Handwritten OCR

فارساخوان یک وب‌اپلیکیشن دمو با Django است که جریان تشخیص متن فارسی را از آپلود تصویر تا نمایش خروجی، کلیدواژه‌ها، تاریخچه و مقایسه‌ی مدل‌ها شبیه‌سازی می‌کند.

## اجرای پروژه در VS Code

ابتدا پروژه را در VS Code باز کن و در ترمینال آن این دستورات را اجرا کن:

```bash
python -m venv .venv
```

فعال‌سازی محیط مجازی در macOS/Linux:

```bash
source .venv/bin/activate
```

فعال‌سازی در Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

سپس وابستگی‌ها و دیتابیس را آماده کن:

```bash
pip install -r requirements.txt
copy .env.example .env  # در macOS/Linux: cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

سایت از مسیر `http://127.0.0.1:8000/` در دسترس خواهد بود.

## ساختار مهم

منطق پردازش دمو داخل `ocr/services/demo_ocr.py` قرار دارد. برای اتصال به Tesseract یا یک مدل Transformer، همین سرویس را جایگزین کن و قرارداد خروجی `text`، `confidence`، `processing_time` و `keywords` را نگه دار. نتیجه‌ها در مدل `ProcessedDocument` ذخیره می‌شوند.

## ساخت ادمین اختیاری

```bash
python manage.py createsuperuser
```

بعد از آن پنل ادمین از مسیر `/admin/` در دسترس است.

## آماده‌سازی GitHub

پس از نصب Git و ساخت یک repository خالی در GitHub، در ریشه‌ی پروژه اجرا کن:

```bash
git init
git add .
git commit -m "Initial Django OCR demo"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/farsakhan.git
git push -u origin main
```

فایل‌های محیط مجازی، دیتابیس محلی، فایل `.env` و آپلودهای توسعه در `.gitignore` قرار دارند و به GitHub ارسال نمی‌شوند.

## اجرای production با Docker

پروژه یک `Dockerfile` و مسیر health در `/health/` دارد. کانتینر با Gunicorn اجرا می‌شود و فایل‌های static با WhiteNoise سرو می‌شوند:

```bash
docker build -t farsakhan .
docker run --rm -p 3000:3000 farsakhan
```

## وضعیت فعلی OCR

خروجی OCR در این نسخه برای دمو شبیه‌سازی شده است؛ داده‌های مدل‌ها و اعداد مقایسه نیز نمونه‌ی نمایشی هستند و برای گزارش علمی نهایی باید با نتایج واقعی دیتاست‌های پروژه جایگزین شوند.
