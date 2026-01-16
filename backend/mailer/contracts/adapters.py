from typing import Optional
from mailer.contracts.user import EmailUser


def to_email_user(user) -> Optional[EmailUser]:
    """
    Convert a Django user-like object to EmailUser.

    This is intentionally best-effort and unused in Phase 1.2.
    """
    if user is None:
        return None

    return EmailUser(
        id=getattr(user, "id", None),
        email=getattr(user, "email", None),
        full_name=(
            user.get_full_name()
            if hasattr(user, "get_full_name")
            else None
        ),
        is_active=getattr(user, "is_active", True),
    )
