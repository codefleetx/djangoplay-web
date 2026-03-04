"""
Unified Issue Query Service.

Provides a read-only unified issue list combining:

- Generic Issue Tracker issues
- Helpdesk BugReports (projected as issues)

Used by the Console Issue UI.
"""

from typing import List

from genericissuetracker.models import Issue

from helpdesk.models import BugReport
from helpdesk.adapters.bug_issue_projection import project_bug_to_issue


class UnifiedIssueQueryService:
    """
    Service responsible for fetching a unified issue list.
    """

    @staticmethod
    def fetch_generic_issues():
        """
        Fetch Generic Issue Tracker issues.

        Returns list of dictionaries compatible with projection schema.
        """

        issues = Issue.objects.filter(deleted_at__isnull=True)

        result = []

        for issue in issues:
            result.append(
                {
                    "id": str(issue.id),
                    "issue_number": issue.issue_number,
                    "title": issue.title,
                    "description": issue.description,
                    "status": issue.status,
                    "priority": issue.priority,
                    "reporter_email": issue.reporter_email,
                    "created_at": issue.created_at,
                    "updated_at": issue.updated_at,
                    "source": "issue",
                    "source_id": issue.id,
                }
            )

        return result

    @staticmethod
    def fetch_bug_reports():
        """
        Fetch Helpdesk BugReports and convert them into issue projections.
        """

        bugs = BugReport.objects.filter(deleted_at__isnull=True)

        return [project_bug_to_issue(bug) for bug in bugs]

    @classmethod
    def get_unified_issues(cls) -> List[dict]:
        """
        Return merged list of issues and bugs.
        """

        issues = cls.fetch_generic_issues()
        bugs = cls.fetch_bug_reports()

        combined = issues + bugs

        combined.sort(
            key=lambda x: x.get("created_at"),
            reverse=True,
        )

        return combined