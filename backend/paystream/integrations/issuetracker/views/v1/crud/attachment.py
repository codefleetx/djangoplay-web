"""
Integrated Attachment ViewSet
=============================

- Enforces RBAC visibility governance
- Uses secure serializer override
"""

from genericissuetracker.views.v1.crud.attachment import (
    AttachmentCRUDViewSet,
)

from genericissuetracker.services.identity import get_identity_resolver

from paystream.integrations.issuetracker.services.visibility import (
    IssueVisibilityService,
)
from paystream.integrations.issuetracker.serializers.v1.read.attachment import (
    IntegratedAttachmentReadSerializer,
)


class IntegratedAttachmentCRUDViewSet(AttachmentCRUDViewSet):
    """
    DjangoPlay-integrated Attachment ViewSet.
    """

    read_serializer_class = IntegratedAttachmentReadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        identity = get_identity_resolver().resolve(self.request)
        visibility = IssueVisibilityService(identity)

        return visibility.filter_attachment_queryset(queryset)