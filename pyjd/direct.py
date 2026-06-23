from __future__ import annotations

import dataclasses
import json
import logging
from typing import TYPE_CHECKING, Any, Literal

from pyjd.common import Params, make_request
from pyjd.jd_types import JDDevice

if TYPE_CHECKING:
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

    def request_json(
        self,
        path: str,
        params: Params | None = None,
        http_action: Literal["GET", "POST"] = "GET",
    ) -> Any:
        content = self.request_bytes(path, params, http_action)
        data = json.loads(content)
        return data.get("data", data)

    def request_bytes(
        self,
        path: str,
        params: Params | None = None,
        http_action: Literal["GET", "POST"] = "GET",
    ) -> bytes:
        return self.request(path, params, http_action).content

    def request(
        self,
        path: str,
        params: Params | None = None,
        http_action: Literal["GET", "POST"] = "GET",
    ) -> requests.Response:
        assert http_action == "GET"
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?" + "&".join(map(json.dumps, params))
        return make_request(url, headers=self.headers)
