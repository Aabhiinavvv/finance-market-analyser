"""Market news provider.

API credentials are supplied through environment variables; never hard-code
provider credentials in source code.
"""

import logging
import os
from typing import Any

from newsapi import NewsApiClient

logger = logging.getLogger(__name__)


class NewsProviderError(RuntimeError):
    """Raised when the configured news provider cannot be used."""


def get_news(limit: int = 5) -> list[dict[str, Any]]:
    """Return business headlines from NewsAPI.

    The UI can treat an empty list as a degraded-but-available state. Missing
    credentials are logged without exposing their value.
    """
    api_key = os.getenv("NEWSAPI_KEY", "").strip()
    if not api_key:
        logger.warning("NEWSAPI_KEY is not configured; news is unavailable")
        return []

    try:
        client = NewsApiClient(api_key=api_key)
        response = client.get_top_headlines(category="business", language="en")
        articles = response.get("articles", [])
        return articles[: max(0, limit)]
    except Exception:
        logger.exception("News provider request failed")
        return []
