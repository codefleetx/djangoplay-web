"""
Integrated Attachment ViewSet
=============================

Extends GenericIssueTracker AttachmentCRUDViewSet.

Future Responsibilities
-----------------------
- Physical file deletion
- Attachment audit logging
- Permission enforcement
"""

from genericissuetracker.views.v1.crud.attachment import (
    AttachmentCRUDViewSet,
)


class IntegratedAttachmentCRUDViewSet(AttachmentCRUDViewSet):
    """
    DjangoPlay-integrated Attachment ViewSet.

    Currently identical to base implementation.
    Physical deletion logic will be added in Phase 3.
    """
    pass
