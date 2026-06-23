from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Protocol

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pyjd.jd_types import JDDevice


class Connection(Protocol):
    device: JDDevice

    def action(
        self,
        path: str,
        params: Sequence[tuple[str, Any]] | None = None,
        *,
        binary: bool = False,
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

    def action(self, route: str, params: Any | None = None, *, binary: bool = False) -> Any:
        route = f"/{self.endpoint}{route}"
        return self.conn.action(route, params, binary=binary)
