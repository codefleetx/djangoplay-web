from django.conf import settings


class IssueStateTransitionOwnerPolicy:
    """
    Allows status transition only for configured roles.

    Roles are defined in settings:
        ISSUE_STATUS_ALLOWED_ROLES = ["CEO", "DJGO", "SSO"]
    """

    def can_transition(self, issue, old_status, new_status, identity):
        if not identity.get("is_authenticated"):
            return False

        user_id = identity.get("id")
        if not user_id:
            return False

        # Resolve Employee
        from users.models import Employee

        try:
            employee = Employee.objects.get(id=user_id, deleted_at__isnull=True)
        except Employee.DoesNotExist:
            return False

        allowed_roles = getattr(
            settings,
            "ISSUE_STATUS_ALLOWED_ROLES",
            [],
        )

        return employee.role.code in allowed_roles