# invoices/urls.py

from django.urls import include, path

urlpatterns = [
    # Canonical versioned API
    path("",include("invoices.views.v1")),
]
