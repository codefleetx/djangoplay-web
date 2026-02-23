"""
Attachment Serializer Override
===============================

Removes public MEDIA exposure.
Provides secure download endpoint only.
"""

from django.urls import reverse
from rest_framework import serializers

from genericissuetracker.serializers.v1.read.attachment import (
    IssueAttachmentReadSerializer,
)


class IntegratedAttachmentReadSerializer(IssueAttachmentReadSerializer):
    """
    Secure attachment serializer.
    """

    download_url = serializers.SerializerMethodField()

    class Meta(IssueAttachmentReadSerializer.Meta):
        # Remove "file" field completely
        fields = [
            "id",
            "issue",
            "original_name",
            "size",
            "created_at",
            "updated_at",
            "download_url",
        ]

    def get_download_url(self, obj):
        request = self.context.get("request")

        url = reverse(
            "issuetracker-attachment-download",
            kwargs={"pk": obj.pk},
        )

        if request:
            return request.build_absolute_uri(url)

        return url