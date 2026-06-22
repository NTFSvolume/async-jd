from __future__ import annotations

import dataclasses
import json
import logging
from typing import Any

from pyjd.http_client import make_request
from pyjd.jd_device import JDDevice

logger = logging.getLogger(__name__)


@dataclasses.dataclass(slots=True)
class DirectConnector:
    base_url: str = "http://localhost:3128"
    headers: dict[str, str] | None = None

    def is_connected(self) -> bool:
        """Check if the JDownloader is reachable.

        This makes a dummy request to the JDownloader and returns True if it
        was successful

        :returns: Connection status
        :rtype: bool
        """
        try:
            make_request(self.base_url + "/jd/version", headers=self.headers)
        except Exception:  # noqa: BLE001
            return False
        else:
            return True

    def get_device(self) -> JDDevice:
        return JDDevice(
            self,
            DirectConnectionHelper,
            {
                "id": "local",
                "name": "Local JDownloader",
                "type": "jd",
            },
        )


@dataclasses.dataclass(slots=True)
class DirectConnectionHelper:
    device: JDDevice

    def action(
        self,
        path: str,
        params: list[Any] | tuple[Any, ...] = (),
        http_action: str = "POST",
        *,
        binary: bool = False,
    ) -> Any:
        """Make the request to the JDownloader"""
        assert http_action == "POST"
        url = f"{self.device.connector.base_url}{path}"
        if params:
            url = f"{url}?" + "&".join(map(json.dumps, params))
        content = make_request(url, headers=self.device.connector.headers).content
        if binary:
            return content

        data = json.loads(content)
        return data.get("data", data)
