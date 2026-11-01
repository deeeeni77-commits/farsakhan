from django.urls import path

from . import views

app_name = "ocr"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("manus-routes.json", views.routes_manifest, name="routes_manifest"),
    path("", views.home, name="home"),
    path("ocr/", views.ocr_demo, name="demo"),
    path("api/ocr/", views.run_ocr, name="run_ocr"),
    path("api/models/", views.models_api, name="models_api"),
    path("analysis/", views.analysis, name="analysis"),
    path("history/", views.history, name="history"),
    path("history/<int:pk>/", views.history_detail, name="history_detail"),
    path("models/", views.models_compare, name="models"),
]
