from __future__ import annotations

import dataclasses
import json
import logging
from typing import TYPE_CHECKING, Any

from pyjd.common import make_request
from pyjd.jd_types import JDDevice

if TYPE_CHECKING:
    from collections.abc import Sequence

    import requests

logger = logging.getLogger(__name__)


@dataclasses.dataclass(slots=True)
class DirectConnection:
    base_url: str = "http://localhost:3128"
    headers: dict[str, str] | None = None
    device: JDDevice = dataclasses.field(
        init=False,
        default=JDDevice(
            id="local",
            name="Local JDownloader",
            type="jd",
        ),
    )

    def is_connected(self) -> bool:
        try:
            make_request(self.base_url + "/jd/version", headers=self.headers)
        except Exception:  # noqa: BLE001
            return False
        else:
            return True

    def action(
        self,
        path: str,
        params: Sequence[tuple[str, Any]] | None = None,
        http_action: str = "POST",
        *,
        binary: bool = False,
    ) -> Any:
        """Make the request to the JDownloader"""
        content = self.request(path, params, http_action).content
        if binary:
            return content

        data = json.loads(content)
        return data.get("data", data)

    def request(
        self,
        path: str,
        params: Sequence[tuple[str, Any]] | None = None,
        http_action: str = "POST",
    ) -> requests.Response:
        assert http_action == "POST"
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?" + "&".join(map(json.dumps, params))
        return make_request(url, headers=self.headers)
