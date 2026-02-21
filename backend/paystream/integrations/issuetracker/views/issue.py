"""
Integrated Issue ViewSet
========================

Extends GenericIssueTracker IssueCRUDViewSet to emit
enterprise integration signals.

Responsibilities
----------------
- Emit issue_created signal
- Emit issue_status_changed signal
- Preserve atomic consistency
- Maintain schema determinism
"""

from django.db import transaction

from genericissuetracker.views.v1.crud.issue import IssueCRUDViewSet
from genericissuetracker.signals import (
    issue_created,
    issue_status_changed,
)
from genericissuetracker.services.identity import get_identity_resolver


class IntegratedIssueCRUDViewSet(IssueCRUDViewSet):
    """
    DjangoPlay-integrated Issue ViewSet.
    """

    def perform_create(self, serializer):
        identity = get_identity_resolver().resolve(self.request)

        with transaction.atomic():
            issue = serializer.save()

            issue_created.send(
                sender=self.__class__,
                issue=issue,
                identity=identity,
            )

    # DO NOT override perform_update.
    # Status transitions are handled via lifecycle service.
    
