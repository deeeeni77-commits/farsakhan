from django.db import models


class ProcessedDocument(models.Model):
    MODEL_CHOICES = [
        ("crnn", "CRNN + Attention"),
        ("vit", "Vision Transformer (ViT)"),
        ("svtr", "SVTR"),
    ]

    original_image = models.ImageField(
        "تصویر ورودی", upload_to="uploads/", blank=True, null=True
    )
    model_name = models.CharField("مدل انتخابی", max_length=24, choices=MODEL_CHOICES)
    extracted_text = models.TextField("متن استخراج‌شده")
    confidence = models.DecimalField("میزان اطمینان", max_digits=5, decimal_places=2)
    processing_time = models.FloatField("زمان پردازش (ثانیه)", default=0.0)
    keywords = models.JSONField("کلیدواژه‌ها", default=list, blank=True)
    created_at = models.DateTimeField("زمان ثبت", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "نتیجه OCR"
        verbose_name_plural = "نتایج OCR"

    def __str__(self):
        return f"{self.get_model_name_display()} — {self.created_at:%Y/%m/%d %H:%M}"
