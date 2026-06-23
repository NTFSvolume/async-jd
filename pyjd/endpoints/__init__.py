from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Protocol

if TYPE_CHECKING:
    import requests

    from pyjd.common import Params
    from pyjd.jd_types import JDDevice


class Connection(Protocol):
    device: JDDevice

    def request(
        self,
        path: str,
        params: Params | None = None,
    ) -> requests.Response: ...

    def request_bytes(
        self,
        path: str,
        params: Params | None = None,
    ) -> bytes: ...

    def request_json(
        self,
        path: str,
        params: Params | None = None,
    ) -> Any: ...


class Action:
    __slots__ = ("conn",)
    endpoint: ClassVar[str]
    conn: Connection

    def __init__(self, connection: Connection) -> None:
        self.conn = connection

    def __repr__(self) -> str:
        return f"<{type(self).__name__}(endpoint={self.endpoint!r})>"

    def __init_subclass__(cls, *, endpoint: str | None = None, **kwargs) -> None:
        if endpoint:
            cls.endpoint = endpoint
        super().__init_subclass__(**kwargs)

    def action(self, route: str, params: Params | None = None) -> Any:
        route = f"/{self.endpoint}{route}"
        return self.conn.request_json(route, params)

    def request_bytes(self, route: str, params: Params | None = None) -> bytes:
        route = f"/{self.endpoint}{route}"
        return self.conn.request_bytes(route, params)
