from django.conf import settings
from django.shortcuts import render
from django.views import View
from paystream.integrations.issuetracker.ui.services.issue_query_service import (
    IssueQueryService,
)
from utilities.constants.template_registry import TemplateRegistry as T


class IssueDetailView(View):

    """
    Read-only Issue detail view.

    Responsibilities:
        - Resolve issue via service
        - Render template
    """

    template_name = T.ISSUES_DETAIL

    def get(self, request, issue_number):
        issue = IssueQueryService.get_issue_for_detail(
            user=request.user,
            issue_number=issue_number,
        )

        context = {
            "issue": issue,
            "site_name": settings.SITE_NAME,
            "site_url": settings.SITE_URL,
        }

        return render(request, self.template_name, context)
