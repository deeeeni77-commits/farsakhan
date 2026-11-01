from io import BytesIO

from django import forms
from PIL import Image, UnidentifiedImageError

from .models import ProcessedDocument


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = ProcessedDocument
        fields = ["original_image", "model_name"]
        widgets = {
            "original_image": forms.ClearableFileInput(
                attrs={"accept": "image/png,image/jpeg,image/webp"}
            ),
            "model_name": forms.Select(),
        }

    def clean_original_image(self):
        image_file = self.cleaned_data["original_image"]
        if image_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("حجم تصویر باید کمتر از ۵ مگابایت باشد.")

        try:
            image = Image.open(BytesIO(image_file.read()))
            image.verify()
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise forms.ValidationError("فایل انتخاب‌شده یک تصویر معتبر نیست.") from exc
        finally:
            image_file.seek(0)

        if image.format not in {"PNG", "JPEG", "WEBP"}:
            raise forms.ValidationError("فرمت مجاز تصویر PNG، JPG یا WEBP است.")
        return image_file
