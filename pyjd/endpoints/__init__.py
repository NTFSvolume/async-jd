from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from pyjd.jd_types import Connection


class Action:
    __slots__ = ("connection",)
    endpoint: ClassVar[str]
    connection: Connection

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def __repr__(self) -> str:
        return f"<{type(self).__name__}(endpoint={self.endpoint!r})>"

    def __init_subclass__(cls, *, endpoint: str | None = None, **kwargs) -> None:
        if endpoint:
            cls.endpoint = endpoint
        super().__init_subclass__(**kwargs)

    def action(self, route: str, params: Any | None = None, binary: bool = False) -> Any:
        route = f"/{self.endpoint}{route}"
        return self.connection.action(route, params, binary=binary)
