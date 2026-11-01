import json
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from .forms import DocumentUploadForm
from .models import ProcessedDocument
from .services.demo_ocr import get_model_catalog, run_demo_ocr


def routes_manifest(request):
    manifest_path = Path(settings.BASE_DIR) / "manus-routes.json"
    return JsonResponse(json.loads(manifest_path.read_text(encoding="utf-8")))


def health(request):
    return HttpResponse("ok", content_type="text/plain")


def home(request):
    context = {
        "documents_count": ProcessedDocument.objects.count(),
        "models": get_model_catalog(),
        "latest_document": ProcessedDocument.objects.first(),
    }
    return render(request, "ocr/home.html", context)


def ocr_demo(request):
    return render(
        request,
        "ocr/demo.html",
        {"form": DocumentUploadForm(), "models": get_model_catalog()},
    )


@require_POST
def run_ocr(request):
    form = DocumentUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        errors = {
            field: [str(error) for error in field_errors]
            for field, field_errors in form.errors.items()
        }
        return JsonResponse({"success": False, "errors": errors}, status=400)

    model_key = form.cleaned_data["model_name"]
    image = form.cleaned_data["original_image"]
    result = run_demo_ocr(model_key, image.name)

    document = form.save(commit=False)
    document.extracted_text = result["text"]
    document.confidence = result["confidence"]
    document.processing_time = result["processing_time"]
    document.keywords = result["keywords"]
    document.save()

    return JsonResponse(
        {
            "success": True,
            "id": document.pk,
            "text": document.extracted_text,
            "confidence": float(document.confidence),
            "processing_time": document.processing_time,
            "keywords": document.keywords,
            "model": document.get_model_name_display(),
            "image_url": document.original_image.url if document.original_image else "",
            "detail_url": f"/history/{document.pk}/",
            "analysis_url": f"/analysis/?id={document.pk}",
            "pipeline": result["pipeline"],
        }
    )


def analysis(request):
    document_id = request.GET.get("id")
    if document_id:
        document = get_object_or_404(ProcessedDocument, pk=document_id)
    else:
        document = ProcessedDocument.objects.first()
    return render(request, "ocr/analysis.html", {"document": document})


def history(request):
    documents = ProcessedDocument.objects.all()
    return render(request, "ocr/history.html", {"documents": documents})


def history_detail(request, pk):
    document = get_object_or_404(ProcessedDocument, pk=pk)
    return render(request, "ocr/detail.html", {"document": document})


def models_compare(request):
    return render(request, "ocr/models.html", {"models": get_model_catalog()})


@require_GET
def models_api(request):
    return JsonResponse({"models": get_model_catalog()})
