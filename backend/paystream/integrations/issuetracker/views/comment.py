"""
Integrated Comment ViewSet
==========================

Extends GenericIssueTracker CommentCRUDViewSet to emit
enterprise integration signals.
"""

from django.db import transaction

from genericissuetracker.views.v1.crud.comment import CommentCRUDViewSet
from genericissuetracker.signals import issue_commented
from genericissuetracker.services.identity import get_identity_resolver


class IntegratedCommentCRUDViewSet(CommentCRUDViewSet):
    """
    DjangoPlay-integrated Comment ViewSet.
    """

    def perform_create(self, serializer):
        identity = get_identity_resolver().resolve(self.request)

        with transaction.atomic():
            comment = serializer.save()

            issue_commented.send(
                sender=self.__class__,
                issue=comment.issue,
                comment=comment,
                identity=identity,
            )
