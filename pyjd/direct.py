from __future__ import annotations

import dataclasses
import json
import logging
from typing import TYPE_CHECKING, Any

import requests

from pyjd.common import Params, make_request
from pyjd.jd_types import JDDevice

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping

logger = logging.getLogger(__name__)


@dataclasses.dataclass(slots=True)
class DirectConnection:
    base_url: str = "http://localhost:3128"
    headers: Mapping[str, str] | None = None
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
        resp = json.loads(content)
        data = resp.get("data", resp)
        if resp.get("type") == "BAD_PARAMETERS":
            msg = f"BAD_PARAMETERS ({data})"
            raise RuntimeError(msg)
        return data

    def request_bytes(self, path: str, params: Params | None = None) -> bytes:
        return self.request(path, params).content

    def request(
        self,
        path: str,
        params: Params | None = None,
    ) -> requests.Response:

        url = f"{self.base_url}{path}"
        data = {
            "apiVer": 1,
            "url": path,
            "params": list(_adapt_params(params)),
            "rid": 12345,
        }

        return make_request(
            url, data=json.dumps(data), headers={"Content-Type": "application/json; charset=utf-8"}
        )


def _adapt_params(params: list[Any] | None) -> Generator[Any]:
    if params is None:
        return

    for param in params:
        if isinstance(param, str):
            yield param
        elif isinstance(param, list):
            yield list(_adapt_params(param))
        else:
            yield json.dumps(param)
