"""
Issue Tracker Integration View Layer
=====================================

This module exposes DjangoPlay-integrated ViewSets that extend
GenericIssueTracker core ViewSets.

Purpose
-------
- Emit integration signals
- Preserve schema determinism
- Avoid modifying third-party package
- Maintain upgrade safety
"""

from .issue import IntegratedIssueCRUDViewSet
from .comment import IntegratedCommentCRUDViewSet
from .attachment import IntegratedAttachmentCRUDViewSet

__all__ = [
    "IntegratedIssueCRUDViewSet",
    "IntegratedCommentCRUDViewSet",
    "IntegratedAttachmentCRUDViewSet",
]
