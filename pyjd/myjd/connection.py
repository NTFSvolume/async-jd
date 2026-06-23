from __future__ import annotations

import dataclasses
import logging
import time
from typing import TYPE_CHECKING, Any, Literal

import requests

from pyjd.jd_types import Address, DirectConnectionInfos

if TYPE_CHECKING:
    from collections.abc import Generator

    from pyjd.common import Params
    from pyjd.jd_types import JDDevice
    from pyjd.myjd.api import MyJDAPI

logger = logging.getLogger(__name__)

type Cooldown = float


@dataclasses.dataclass(slots=True)
class DirectConnections:
    _enabled: bool = True
    _address_map: dict[Address, Cooldown] = dataclasses.field(default_factory=dict)
    cooldown: int = 0
    consecutive_errors: int = 0

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self) -> None:
        self._enabled = False
        self._address_map.clear()

    def __getitem__(self, address: Address) -> Cooldown:
        return self._address_map[address]

    def __setitem__(self, address: Address, cooldown: Cooldown) -> None:
        self._address_map[address] = cooldown

    def __iter__(self) -> Generator[tuple[Address, Cooldown]]:
        yield from reversed(tuple(self._address_map.items()))

    def __bool__(self) -> bool:
        return self._enabled and bool(self._address_map) and time.time() > self.cooldown

    def push(self, address: Address) -> None:
        self._address_map[address] = self._address_map.pop(address, 0)

    def refresh(self, valid_addresses: set[Address]) -> None:
        unavaiable = self._address_map.keys() - valid_addresses
        new = valid_addresses - self._address_map.keys()
        for address in unavaiable:
            del self._address_map[address]

        # Push existing ones last to give them priority
        for address in (*new, *tuple(self._address_map)):
            self.push(address)

    def register_error(self) -> None:
        self.consecutive_errors += 1
        self.cooldown = int(time.time() + (60 * self.consecutive_errors))


@dataclasses.dataclass(slots=True)
class MyJDConnection:
    api: MyJDAPI
    device: JDDevice
    _direct_conns: DirectConnections = dataclasses.field(
        init=False, default_factory=DirectConnections
    )
    _ready: bool = dataclasses.field(init=False, default=False)

    def refresh_direct_connections(self) -> None:
        if not self._direct_conns.enabled or time.time() < self._direct_conns.cooldown:
            return

        logger.info("refreshing direct connections")
        resp = self.api.request_json(
            "/device/getDirectConnectionInfos",
            "POST",
            action=self.__action_url(),
        )
        resp = DirectConnectionInfos(**resp.get("data", resp))

        if not resp.infos:
            return

        self._direct_conns.refresh(set(resp.infos))

    def enable_direct_connection(self) -> None:
        self._direct_conns.enabled = True
        self.refresh_direct_connections()

    def disable_direct_connect(self) -> None:
        self._direct_conns.enabled = False

    def request_json(
        self,
        path: str,
        params: Params | None = (),
        http_action: Literal["GET", "POST"] = "POST",
    ) -> Any:
        response = self.request(path, params, http_action)
        data = self.api.decode_response(response, self.__action_url())
        if data is None:
            return None
        return data.get("data", data)

    def request(
        self,
        path: str,
        params: Params | None = (),
        http_action: Literal["GET", "POST"] = "POST",
    ) -> requests.Response:
        if not self._ready:
            try:
                self.refresh_direct_connections()
            finally:
                self._ready = True

        if not self._direct_conns:
            return self._myjd_request(path, params, http_action)

        action_url = self.__action_url()
        now = time.time()
        for address, cooldown in self._direct_conns:
            if now < cooldown:
                continue

            try:
                response = self.api.request(
                    path,
                    http_action,
                    params,
                    action_url,
                    api=f"http://{address.ip}:{address.port}",
                )
            except requests.exceptions.RequestException:
                self._direct_conns[address] = now + 60
                continue

            # This connection worked, push it to the end to give it priority on the next request
            self._direct_conns.push(address)
            self._direct_conns.consecutive_errors = 0
            return response

        # Fallback to MyJD API
        self._direct_conns.register_error()
        return self._myjd_request(path, params, http_action)

    def request_bytes(
        self,
        path: str,
        params: Params | None = (),
        http_action: Literal["GET", "POST"] = "POST",
    ) -> bytes:
        return self.request(path, params, http_action).content

    def _myjd_request(
        self,
        path: str,
        params: Any | None = (),
        http_action: Literal["GET", "POST"] = "POST",
    ) -> requests.Response:
        response = self.api.request(path, http_action, params, self.__action_url())
        self.refresh_direct_connections()
        return response

    def __action_url(self) -> str:
        return "/t_" + self.api.session_token + "_" + self.device.id
