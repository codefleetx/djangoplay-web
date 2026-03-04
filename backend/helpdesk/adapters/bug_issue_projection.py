"""
Bug → Issue projection adapter.

This module converts Helpdesk BugReport objects into
Issue-like dictionaries so they can be displayed inside
the Generic Issue Tracker UI.

This adapter is READ-ONLY and does not mutate BugReport.
"""
from dataclasses import dataclass, field

from helpdesk.models import BugReport


# ---------------------------------------------------------
# Status / priority mapping
# ---------------------------------------------------------

BUG_STATUS_TO_ISSUE_STATUS = {
    "NEW": "OPEN",
    "TRIAGED": "OPEN",
    "IN_PROGRESS": "IN_PROGRESS",
    "FIXED": "RESOLVED",
    "VERIFIED": "RESOLVED",
    "CLOSED": "CLOSED",
}

BUG_SEVERITY_TO_PRIORITY = {
    "LOW": "LOW",
    "MEDIUM": "MEDIUM",
    "HIGH": "HIGH",
    "CRITICAL": "CRITICAL",
}


# ---------------------------------------------------------
# Lightweight comment manager
# ---------------------------------------------------------
class EmptyCommentQuerySet:
    def all(self):
        return self

    def filter(self, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def count(self):
        return 0

    def __iter__(self):
        return iter([])  # so for x in ... works

# ---------------------------------------------------------
# Projection Object
# ---------------------------------------------------------

@dataclass
class UnifiedIssueProjection:
    id: str
    issue_number: str
    title: str
    description: str
    status: str
    priority: str
    reporter_email: str | None
    created_at: object
    updated_at: object
    source: str
    is_public: bool = True
    comments: object = field(default_factory=EmptyCommentQuerySet)
    attachments: object = field(default_factory=EmptyCommentQuerySet)


# ---------------------------------------------------------
# Projection function
# ---------------------------------------------------------

def project_bug_to_issue(bug: BugReport) -> UnifiedIssueProjection:

    reporter_email = None

    if bug.reporter:
        reporter_email = getattr(bug.reporter, "email", None)

    return UnifiedIssueProjection(
        id=f"bug-{bug.id}",
        issue_number=bug.bug_number,
        title=bug.summary,
        description=bug.steps_to_reproduce,
        status=BUG_STATUS_TO_ISSUE_STATUS.get(bug.status, "OPEN"),
        priority=BUG_SEVERITY_TO_PRIORITY.get(bug.severity, "MEDIUM"),
        reporter_email=reporter_email,
        created_at=bug.created_at,
        updated_at=bug.updated_at,
        source="bug",
    )