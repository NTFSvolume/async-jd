from __future__ import annotations

import dataclasses
import logging
import time
from typing import TYPE_CHECKING, Any, Literal

from pyjd.jd_types import Connection

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pyjd.jd_types import JDDevice
    from pyjd.myjd.api import MyJDAPI

logger = logging.getLogger(__name__)

type CoolDown = float


@dataclasses.dataclass(slots=True, frozen=True)
class _DirectConnection:
    ip: str
    port: int


@dataclasses.dataclass(slots=True)
class _DirectConnectionContext:
    enabled: bool = True
    info: dict[_DirectConnection, CoolDown] = dataclasses.field(default_factory=dict)
    min_cooldown: int = 0
    consecutive_errors: int = 0

    @property
    def should_use(self) -> bool:
        return self.enabled and bool(self.info) and not self.is_cooling_down

    @property
    def is_cooling_down(self) -> bool:
        return time.time() < self.min_cooldown

    def refresh(self, valid_connections: set[_DirectConnection]) -> None:
        info = dict.fromkeys(valid_connections.difference(self.info), 0)
        # put pre-existing connections last to give them priority
        info |= {
            conn: cooldown for conn, cooldown in self.info.items() if conn in valid_connections
        }
        self.info = info


class MyJDConnection(Connection):
    def __init__(
        self,
        api: MyJDAPI,
        device: JDDevice,
        *,
        refresh_direct_connections: bool = True,
    ) -> None:
        self.api: MyJDAPI = api
        self.device: JDDevice = device
        self._direct_ctx: _DirectConnectionContext = _DirectConnectionContext()
        if refresh_direct_connections:
            self.__refresh_direct_connections()

    def refresh_direct_connections(self) -> None:
        self.__refresh_direct_connections()

    def __refresh_direct_connections(self) -> None:
        if not self._direct_ctx.enabled or self._direct_ctx.is_cooling_down:
            return

        logger.info("refreshing direct connections")
        response = self.api.request(
            "/device/getDirectConnectionInfos",
            "POST",
            None,
            self.__action_url(),
        )

        try:
            connections: list[dict[str, Any]] = response["data"]["infos"]
        except LookupError:
            return

        if len(connections) > 0:
            self._direct_ctx.refresh({_DirectConnection(**info) for info in connections})

    def enable_direct_connection(self) -> None:
        self._direct_ctx.enabled = True
        self.__refresh_direct_connections()

    def disable_direct_connect(self) -> None:
        self._direct_ctx.enabled = False
        self._direct_ctx.info.clear()

    def action(
        self,
        path: str,
        params: Sequence[tuple[str, str | int]] | None = (),
        http_action: Literal["GET", "POST"] = "POST",
        *,
        binary: bool = False,
    ) -> dict[str, Any] | None:

        if not self._direct_ctx.should_use:
            return self._myjd_request(path, params, http_action, binary=binary)

        action_url = self.__action_url()
        now = time.time()
        for connection, cooldown in reversed(self._direct_ctx.info.items()):
            if now < cooldown:
                continue

            response = self.api.request(
                path,
                http_action,
                params,
                action_url,
                api=f"http://{connection.ip}:{connection.port}",
                binary=binary,
            )
            if response is None:
                self._direct_ctx.info[connection] = now + 60
                continue

            # This connection worked, remove and re add it to give it priority on the next request
            cooldown = self._direct_ctx.info.pop(connection)
            self._direct_ctx.info[connection] = cooldown
            self._direct_ctx.consecutive_errors = 0
            if binary:
                return response
            return response.get("data", response)

        # Fallback to MyJD API
        self._direct_ctx.consecutive_errors += 1
        self._direct_ctx.min_cooldown = int(now + (60 * self._direct_ctx.consecutive_errors))
        return self._myjd_request(path, params, http_action, binary=binary)

    def _myjd_request(
        self,
        path: str,
        params: Any | None = (),
        http_action: Literal["GET", "POST"] = "POST",
        *,
        binary: bool = False,
    ):
        response = self.api.request(path, http_action, params, self.__action_url(), binary=binary)
        if response is None or binary:
            return response

        self.__refresh_direct_connections()
        return response.get("data", response)

    def __action_url(self) -> str:
        return "/t_" + self.api.session_token + "_" + self.device.id
