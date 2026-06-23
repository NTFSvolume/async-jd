from __future__ import annotations

import dataclasses
import logging
import time
from typing import TYPE_CHECKING, Any, Literal

from pyjd.jd_types import Address, Connection, DirectConnectionInfos

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence

    from pyjd.jd_types import JDDevice
    from pyjd.myjd.api import MyJDAPI

logger = logging.getLogger(__name__)

type CoolDown = float


@dataclasses.dataclass(slots=True)
class DirectConnections:
    _enabled: bool = True
    _address_map: dict[Address, CoolDown] = dataclasses.field(default_factory=dict)
    min_cooldown: int = 0
    consecutive_errors: int = 0

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self) -> None:
        self._enabled = False
        self._address_map.clear()

    def __getitem__(self, address: Address) -> CoolDown:
        return self._address_map[address]

    def __setitem__(self, address: Address, cooldown: CoolDown) -> None:
        self._address_map[address] = cooldown

    def __iter__(self) -> Generator[tuple[Address, CoolDown]]:
        yield from reversed(tuple(self._address_map.items()))

    def __bool__(self) -> bool:
        return self._enabled and bool(self._address_map) and time.time() > self.min_cooldown

    def push(self, address: Address) -> None:
        self._address_map[address] = self._address_map.pop(address, 0)

    def update(self, valid_addresses: set[Address]) -> None:
        unavaiable = self._address_map.keys() - valid_addresses
        new = valid_addresses - self._address_map.keys()
        for address in unavaiable:
            del self._address_map[address]

        # Push existing ones last to give them priority
        for address in (*new, *tuple(self._address_map)):
            self.push(address)


class MyJDConnection(Connection):
    def __init__(
        self,
        api: MyJDAPI,
        device: JDDevice,
    ) -> None:
        self.api: MyJDAPI = api
        self.device: JDDevice = device
        self._direct_connections: DirectConnections = DirectConnections()
        self._ready: bool = False

    def refresh_direct_connections(self) -> None:
        if (
            not self._direct_connections.enabled
            or time.time() < self._direct_connections.min_cooldown
        ):
            return

        logger.info("refreshing direct connections")
        resp = self.api.request(
            "/device/getDirectConnectionInfos",
            "POST",
            action=self.__action_url(),
        )
        resp = DirectConnectionInfos(**resp.get("data", resp))

        if not resp.infos:
            return

        self._direct_connections.update(set(resp.infos))

    def enable_direct_connection(self) -> None:
        self._direct_connections.enabled = True
        self.refresh_direct_connections()

    def disable_direct_connect(self) -> None:
        self._direct_connections.enabled = False

    def action(
        self,
        path: str,
        params: Sequence[tuple[str, str | int]] | None = (),
        http_action: Literal["GET", "POST"] = "POST",
        *,
        binary: bool = False,
    ) -> dict[str, Any] | None:
        if not self._ready:
            try:
                self.refresh_direct_connections()
            finally:
                self._ready = True

        if self._direct_connections:
            return self._myjd_request(path, params, http_action, binary=binary)

        action_url = self.__action_url()
        now = time.time()
        for address, cooldown in self._direct_connections:
            if now < cooldown:
                continue

            response = self.api.request(
                path,
                http_action,
                params,
                action_url,
                api=f"http://{address.ip}:{address.port}",
                binary=binary,
            )
            if response is None:
                self._direct_connections[address] = now + 60
                continue

            # This connection worked, puhs it to the end to give it priority on the next request
            self._direct_connections.push(address)
            self._direct_connections.consecutive_errors = 0
            if binary:
                return response
            return response.get("data", response)

        # Fallback to MyJD API
        self._direct_connections.consecutive_errors += 1
        self._direct_connections.min_cooldown = int(
            now + (60 * self._direct_connections.consecutive_errors)
        )
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

        self.refresh_direct_connections()
        return response.get("data", response)

    def __action_url(self) -> str:
        return "/t_" + self.api.session_token + "_" + self.device.id
