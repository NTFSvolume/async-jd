from __future__ import annotations

import dataclasses
import json
import logging
from typing import Any

import requests

from pyjd.common import Params, make_request, prepare_api_json
from pyjd.jd_types import JDDevice

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
        except requests.exceptions.RequestException:
            return False
        else:
            return True

    def request_json(self, path: str, params: Params | None = None) -> Any:
        content = self.request_bytes(path, params)
        return _parse_resp(content)

    def request_bytes(self, path: str, params: Params | None = None) -> bytes:
        return self.request(path, params).content

    def request(self, path: str, params: Params | None = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        return make_request(url, data=prepare_api_json(path, params))


def _parse_resp(content: bytes | str) -> Any:
    resp = json.loads(content)
    data = resp.get("data", resp)
    if resp.get("type") == "BAD_PARAMETERS":
        msg = f"BAD_PARAMETERS ({str(data)[:40]})"
        raise RuntimeError(msg)
    return data
