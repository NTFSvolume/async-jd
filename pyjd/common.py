from __future__ import annotations

import dataclasses
import json
import logging
import time
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, ClassVar, Self

import requests

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from collections.abc import Generator, Mapping

REQUEST_ID: ContextVar[int] = ContextVar("REQUEST_ID")

_MISSING = object()

type Params = list[Any]


def next_request_id() -> int:
    return time.time_ns()


class DictDataClass:
    __dataclass_fields__: ClassVar[dict[str, dataclasses.Field[Any]]]

    # dict protocol ->  dict(self)
    def __iter__(self) -> Generator[tuple[str, Any]]:
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)

    # recursive dict conversion
    def __json__(self) -> dict[str, Any]:
        return dict(self)

    @classmethod
    def filter_dict(cls, data: Mapping[str, Any]) -> dict[str, Any]:
        return {
            field.name: value
            for field in dataclasses.fields(cls)
            if field.init and (value := data.get(field.name, _MISSING)) is not _MISSING
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        return cls(**cls.filter_dict(data))


def make_request(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: str | None = None,
    timeout: int = 60,
    method: str = "POST",
) -> requests.Response:
    logger.debug(f"Request to {url}")
    headers = headers or {}
    if method == "POST":
        headers.setdefault("Content-Type", "application/json; charset=utf-8")
    return requests.request(method, url, headers=headers, timeout=timeout, data=data)


def _parse_param(params: Params | None):
    if not params:
        return
    for param in params:
        if type(param) is dict:
            yield {k: v for k, v in param.items() if v is not None}
        else:
            yield params


def prepare_api_json(path: str, params: Params | None) -> str:

    data = {
        "apiVer": 1,
        "url": path.partition("?")[0],
        "params": list(_parse_param(params)),
        "rid": REQUEST_ID.get(),
    }
    return json.dumps(data)
