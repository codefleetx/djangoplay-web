from genericissuetracker.models import Issue
from helpdesk.adapters.bug_issue_projection import UnifiedIssueProjection


def project_generic_issue(issue: Issue) -> UnifiedIssueProjection:
    """
    Project GenericIssueTracker Issue
    into unified Issue representation for UI.
    """

    return UnifiedIssueProjection(
        id=str(issue.id),
        issue_number=issue.issue_number,
        title=issue.title,
        description=issue.description,
        status=issue.status,
        priority=issue.priority,
        reporter_email=issue.reporter_email,
        created_at=issue.created_at,
        updated_at=issue.updated_at,
        source="issue",
    )