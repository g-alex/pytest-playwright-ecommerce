"""Build a stable search token from product fields (RU locale)."""

from __future__ import annotations

import re


def search_token(product: dict) -> str:
    title = product.get("title_ru") or product.get("title") or ""
    words = re.findall(r"[A-Za-zА-Яа-яЁёІіЇїЄєҐґ0-9]+", title)
    assert words, f"No searchable token in title: {title!r}"
    return words[0]
