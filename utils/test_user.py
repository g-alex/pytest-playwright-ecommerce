"""Helpers to keep UI checkout identity aligned with TEST_USER_ID."""

from __future__ import annotations


def telegram_username_for(test_user_id: str) -> str:
    """Browser checkout builds id as web_tg_<username> from Telegram field."""
    prefix = "web_tg_"
    if not test_user_id.startswith(prefix):
        raise ValueError(
            f"TEST_USER_ID must start with '{prefix}' for UI checkout sync, "
            f"got: {test_user_id}"
        )
    return test_user_id[len(prefix) :]
