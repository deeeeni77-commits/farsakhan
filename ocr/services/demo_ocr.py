from __future__ import annotations

import re
import time
from typing import Any

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


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


def get_model_catalog() -> list[dict[str, Any]]:
    return MODEL_CATALOG


def _keywords(text: str) -> list[str]:
    words = re.findall(
        r"[\u0600-\u06FF\u200cA-Za-z][\u0600-\u06FF\u200cA-Za-z0-9-]{2,}",
        text,
    )
    ignored = {"برای", "است", "این", "های", "با", "از", "the", "and"}
    unique: list[str] = []
    for word in words:
        normalized = word.strip("،؛,.!:؟")
        if normalized and normalized.lower() not in ignored and normalized not in unique:
            unique.append(normalized)
    return unique[:8]


def run_demo_ocr(model_key: str, image_file: Any, image_name: str = "") -> dict[str, Any]:
    """Extract text from the uploaded image using real Persian/English OCR.

    The model selector remains part of the demo UI, but the current deployable
    engine is Tesseract. It is isolated here so a trained handwritten model can
    replace it later without changing the views.
    """
    started_at = time.perf_counter()
    image_file.seek(0)
    image = Image.open(image_file).convert("RGB")
    image = ImageOps.exif_transpose(image)
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    image = image.filter(ImageFilter.SHARPEN)
    image = ImageEnhance.Contrast(image).enhance(1.25)
    if max(image.size) < 1800:
        scale = 1800 / max(image.size)
        image = image.resize((int(image.width * scale), int(image.height * scale)))

    config = "--oem 1 --psm 6"
    data = pytesseract.image_to_data(
        image,
        lang="fas+eng",
        config=config,
        output_type=pytesseract.Output.DICT,
    )
    lines = [
        part.strip()
        for part in pytesseract.image_to_string(image, lang="fas+eng", config=config).splitlines()
        if part.strip()
    ]
    text = "\n".join(lines).strip()
    scores = [
        float(value)
        for value in data["conf"]
        if str(value).strip() not in {"", "-1"}
    ]
    confidence = round(max(0.0, min(99.9, sum(scores) / len(scores))) if scores else 0.0, 2)
    if not text:
        text = "متنی از این تصویر شناسایی نشد. لطفاً تصویر واضح‌تر و با نور مناسب‌تری بارگذاری کنید."

    return {
        "text": text,
        "confidence": confidence,
        "processing_time": round(time.perf_counter() - started_at, 2),
        "keywords": _keywords(text),
        "model_key": model_key,
        "source_name": image_name,
        "pipeline": [
            {"label": "چرخش، حذف نویز و افزایش کنتراست", "status": "done"},
            {"label": "تشخیص متن فارسی و انگلیسی با Tesseract", "status": "done"},
            {"label": "تجمیع خطوط و استخراج کلیدواژه‌ها", "status": "done"},
        ],
    }
