
from django.db.models import Count, QuerySet
from genericissuetracker.models import Issue, IssueStatus
from genericissuetracker.services.pagination import resolve_page_size

from helpdesk.adapters.bug_issue_projection import project_bug_to_issue
from helpdesk.adapters.generic_issue_projection import project_generic_issue

from helpdesk.models import BugReport

from paystream.integrations.issuetracker.services.visibility import (
    IssueVisibilityService,
)


class IssueQueryService:

    """
    Service responsible for constructing Issue list querysets
    for UI consumption.

    Responsibilities:
        - Base queryset construction
        - Visibility filtering
        - Enum-driven status filtering
        - Deterministic ordering

    No business logic.
    No permission logic duplication.
    """
    # ---------------------------------------------------------
    # Generic Issues
    # ---------------------------------------------------------
    @staticmethod
    def _fetch_issues(user, status):

        queryset = Issue.objects.all().annotate(
            comment_count=Count("comments", distinct=True)
        )

        identity = {
            "is_authenticated": user.is_authenticated,
            "is_superuser": getattr(user, "is_superuser", False),
            "role_code": getattr(user, "role_code", None),
        }

        visibility_service = IssueVisibilityService(identity=identity)

        queryset = visibility_service.filter_issue_queryset(queryset)

        if status and status != "ALL":
            valid = {choice[0] for choice in IssueStatus.choices}

            if status in valid:
                queryset = queryset.filter(status=status)

        issues = []

        for issue in queryset:
            issues.append(project_generic_issue(issue))

        return issues

    # ---------------------------------------------------------
    # Bug projections
    # ---------------------------------------------------------
    @staticmethod
    def _fetch_bugs(status):

        bugs = BugReport.objects.filter(deleted_at__isnull=True)

        projections = []

        for bug in bugs:

            p = project_bug_to_issue(bug)

            projections.append(p)

        if status and status != "ALL":
            projections = [
                p for p in projections if p.status == status
            ]

        return projections


    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    @staticmethod
    def get_issues_for_list(user, status: str | None = None):
        """
        Returns issues visible to the given user,
        optionally filtered by status.

        Combines:
            - GenericIssueTracker issues
            - Helpdesk BugReport projections
        """

        # Reuse existing logic
        issues = IssueQueryService._fetch_issues(user, status)

        # Fetch bug projections
        bugs = IssueQueryService._fetch_bugs(status)

        # Merge results
        combined = issues + bugs

        # Deterministic ordering
        combined.sort(
            key=lambda x: x.created_at if hasattr(x, "created_at") else x["created_at"],
            reverse=True,
        )

        return combined

    # ---------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------
    @staticmethod
    def get_page_size() -> int:
        """
        Resolve page size from genericissuetracker settings.
        """
        return resolve_page_size()

    # ---------------------------------------------------------
    # Detail fetch
    # ---------------------------------------------------------
    @staticmethod
    def get_issue_for_detail(user, issue_number: int):
        from django.http import Http404

        queryset = (
            Issue.objects.all()
            .prefetch_related("comments", "attachments")
        )

        identity = {
            "is_authenticated": user.is_authenticated,
            "is_superuser": getattr(user, "is_superuser", False),
            "role_code": getattr(user, "role_code", None),
        }

        visibility_service = IssueVisibilityService(identity=identity)
        queryset = visibility_service.filter_issue_queryset(queryset)

        try:
            return queryset.get(issue_number=issue_number)
        except Issue.DoesNotExist:
            raise Http404("Issue not found")
