from __future__ import annotations

from typing import Any


MODEL_CATALOG: list[dict[str, Any]] = [
    {
        "key": "crnn",
        "name": "CRNN + Attention",
        "short_name": "CRNN",
        "accuracy": "91.8٪",
        "parameters": "12.4M",
        "gflops": "1.6",
        "fit": "موبایل و پردازش سریع",
        "description": "سبک، سریع و مناسب برای شروع پردازش روی منابع محدود.",
        "accent": "teal",
    },
    {
        "key": "vit",
        "name": "Vision Transformer (ViT)",
        "short_name": "ViT",
        "accuracy": "95.1٪",
        "parameters": "86.7M",
        "gflops": "17.2",
        "fit": "دقت بالا و اسناد پیچیده",
        "description": "مدل دقیق‌تر برای متن‌های متنوع و تصاویر با پیچیدگی بیشتر.",
        "accent": "purple",
    },
    {
        "key": "svtr",
        "name": "SVTR",
        "short_name": "SVTR",
        "accuracy": "94.3٪",
        "parameters": "28.6M",
        "gflops": "6.8",
        "fit": "سامانه‌های عملیاتی",
        "description": "تعادل قابل اتکا بین دقت، سرعت و هزینه‌ی محاسباتی.",
        "accent": "orange",
    },
]


_DEMO_OUTPUTS = {
    "crnn": {
        "text": "نام شهر: شیراز\nنوع نمونه: دست‌نویس فارسی\nوضعیت: قابل پردازش",
        "confidence": 91.8,
        "processing_time": 0.84,
        "keywords": ["شیراز", "دست‌نویس", "فارسی", "پردازش"],
    },
    "vit": {
        "text": "نام شهر: شیراز\nاین نمونه برای ارزیابی تشخیص متن فارسی آماده شده است.",
        "confidence": 95.1,
        "processing_time": 1.47,
        "keywords": ["شیراز", "ارزیابی", "تشخیص متن", "فارسی"],
    },
    "svtr": {
        "text": "نام شهر: شیراز\nنمونه‌ی آزمایشی با مدل SVTR تحلیل شد.",
        "confidence": 94.3,
        "processing_time": 1.08,
        "keywords": ["شیراز", "SVTR", "آزمایشی", "تحلیل"],
    },
}


def get_model_catalog() -> list[dict[str, Any]]:
    return MODEL_CATALOG


def run_demo_ocr(model_key: str, image_name: str = "") -> dict[str, Any]:
    """دموی قابل جایگزینی با موتور واقعی OCR.

    در نسخه‌ی بعدی، همین قرارداد می‌تواند به Tesseract، PaddleOCR یا Transformer متصل شود.
    """
    result = _DEMO_OUTPUTS.get(model_key, _DEMO_OUTPUTS["crnn"]).copy()
    result["model_key"] = model_key
    result["source_name"] = image_name
    result["pipeline"] = [
        {"label": "حذف نویز و نرمال‌سازی", "status": "done"},
        {"label": "استخراج ویژگی‌های بصری", "status": "done"},
        {"label": "تشخیص توالی متن فارسی", "status": "done"},
    ]
    return result
