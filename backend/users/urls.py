# users/urls.py

from django.urls import include, path
from utilities.views.health_check import HealthCheckView

app_name = "users"

urlpatterns = [
    # ------------------------------------------------------------------
    # Canonical versioned API
    # ------------------------------------------------------------------
    path(
        "",
        include("users.views.v1"),
    ),

    # ------------------------------------------------------------------
    # Health check (non-versioned by design)
    # ------------------------------------------------------------------
    path(
        "health/",
        HealthCheckView.as_view(),
        name="health-check",
    ),
]
