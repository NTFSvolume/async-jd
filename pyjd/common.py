from __future__ import annotations

import dataclasses
import logging
from collections.abc import Collection
from typing import TYPE_CHECKING, Any, ClassVar, Self

import requests

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from collections.abc import Generator, Mapping


_MISSING = object()

type Params = Collection[tuple[str, Any] | str | int | list[int] | list[str]]


class DictDataClass:
    __dataclass_fields__: ClassVar[dict[str, dataclasses.Field[Any]]]

    # dict protocol ->  dict(self)
    def __iter__(self) -> Generator[tuple[str, Any]]:
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)

    # recursive dict conversion
    def __json__(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

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
    data: Any = None,
    timeout: int = 60,
) -> requests.Response:
    logger.debug(f"Request to {url}")
    return requests.get(url, headers=headers, timeout=timeout, data=data)
