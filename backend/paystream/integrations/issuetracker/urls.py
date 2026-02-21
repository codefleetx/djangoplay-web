"""
Issue Tracker Integration URL Configuration
===========================================

Replaces default GenericIssueTracker routing
with integrated ViewSets.

Mount Path:
    /api/v1/issuetracker/
"""

from rest_framework.routers import DefaultRouter

from .views import (
    IntegratedIssueCRUDViewSet,
    IntegratedCommentCRUDViewSet,
    IntegratedAttachmentCRUDViewSet,
)

from genericissuetracker.views.v1.read.issue import IssueReadViewSet
from genericissuetracker.views.v1.read.comment import CommentReadViewSet
from genericissuetracker.views.v1.read.attachment import AttachmentReadViewSet
from genericissuetracker.views.v1.read.label import LabelReadViewSet
from genericissuetracker.views.v1.crud.label import LabelCRUDViewSet

router = DefaultRouter()

# ----------------------------------------------------------------------
# ISSUE ENDPOINTS
# ----------------------------------------------------------------------
router.register(r"issues", IntegratedIssueCRUDViewSet, basename="issue")
router.register(r"issues-read", IssueReadViewSet, basename="issue-read")

# ----------------------------------------------------------------------
# COMMENT ENDPOINTS
# ----------------------------------------------------------------------
router.register(r"comments", IntegratedCommentCRUDViewSet, basename="comment")
router.register(r"comments-read", CommentReadViewSet, basename="comment-read")

# ----------------------------------------------------------------------
# ATTACHMENT ENDPOINTS
# ----------------------------------------------------------------------
router.register(r"attachments", IntegratedAttachmentCRUDViewSet, basename="attachment")
router.register(r"attachments-read", AttachmentReadViewSet, basename="attachment-read")

# ----------------------------------------------------------------------
# LABEL ENDPOINTS (unchanged)
# ----------------------------------------------------------------------
router.register(r"labels", LabelCRUDViewSet, basename="label")
router.register(r"labels-read", LabelReadViewSet, basename="label-read")

urlpatterns = router.urls
