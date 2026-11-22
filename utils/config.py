"""Load settings from environment / .env (no secrets in repo)."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str
    test_user_id: str
    browser: str
    headless: bool
    request_timeout: float


def get_settings() -> Settings:
    return Settings(
        base_url=os.getenv("BASE_URL", "http://localhost:3000").rstrip("/"),
        test_user_id=os.getenv("TEST_USER_ID", "web_aqa_portfolio_001"),
        browser=os.getenv("BROWSER", "chromium").lower(),
        headless=os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"},
        request_timeout=float(os.getenv("REQUEST_TIMEOUT", "15")),
    )
