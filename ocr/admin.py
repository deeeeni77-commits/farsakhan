from django.contrib import admin

from .models import ProcessedDocument


@admin.register(ProcessedDocument)
class ProcessedDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "model_name",
        "confidence",
        "processing_time",
        "created_at",
    )
    list_filter = ("model_name", "created_at")
    search_fields = ("extracted_text",)
    readonly_fields = ("created_at",)
