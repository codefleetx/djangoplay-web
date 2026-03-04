"""
Unified Issue Tracker endpoints (read-only).

Provides UI access to unified issue list combining:
    - Generic issues
    - Helpdesk bugs
"""

from django.urls import path

from helpdesk.views.v1.read.issuetracker.unified_issues import (
    UnifiedIssueListView,
)

urlpatterns = [
    path(
        "issues/",
        UnifiedIssueListView.as_view(),
        name="issues-list",
    ),
]