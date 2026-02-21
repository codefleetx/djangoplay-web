import logging
from django.dispatch import receiver

from genericissuetracker.signals import (
    issue_created,
    issue_commented,
    issue_status_changed,
)

logger = logging.getLogger(__name__)


@receiver(issue_created)
def handle_issue_created(sender, issue, identity, **kwargs):
    logger.info(
        "[IssueTrackerIntegration] issue_created | "
        "issue_number=%s reporter=%s identity=%s",
        issue.issue_number,
        issue.reporter_email,
        identity,
    )


@receiver(issue_commented)
def handle_issue_commented(sender, issue, comment, identity, **kwargs):
    logger.info(
        "[IssueTrackerIntegration] issue_commented | "
        "issue_number=%s commenter=%s identity=%s",
        issue.issue_number,
        comment.commenter_email,
        identity,
    )


@receiver(issue_status_changed)
def handle_issue_status_changed(
    sender,
    issue,
    old_status,
    new_status,
    identity,
    **kwargs,
):
    logger.info(
        "[IssueTrackerIntegration] issue_status_changed | "
        "issue_number=%s %s → %s identity=%s",
        issue.issue_number,
        old_status,
        new_status,
        identity,
    )
