"""
Unified Issue List View.

This view exposes a unified issue list combining:

- Generic Issue Tracker issues
- Helpdesk BugReports (via projection adapter)

The result is consumed by the Issue UI.

This view is READ-ONLY and does not mutate any models.
"""

from django.views.generic import TemplateView

from helpdesk.services.unified_issue_query_service import (
    UnifiedIssueQueryService,
)


class UnifiedIssueListView(TemplateView):
    """
    Display unified issue list.

    Combines:
        - Generic Issues
        - Helpdesk Bugs (projected)

    Sorted by created_at DESC.
    """

    template_name = "issues/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        issues = UnifiedIssueQueryService.get_unified_issues()

        context["issues"] = issues

        return context