from __future__ import annotations

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


def make_request(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: Any = None,
    timeout: int = 60,
) -> requests.Response:
    logger.debug(f"Request to {url}")
    return requests.get(url, headers=headers, timeout=timeout, data=data)
