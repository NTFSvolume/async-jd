from __future__ import annotations

import dataclasses
import logging
import time
from typing import TYPE_CHECKING, Any, Literal

from pyjd.jd_types import API, Connection

if TYPE_CHECKING:
    from pyjd.jd_device import JDDevice

logger = logging.getLogger(__name__)


@dataclasses.dataclass(slots=True, frozen=True)
class _DirectConnection:
    ip: str
    port: int


@dataclasses.dataclass(slots=True)
class DirectConnectionContext:
    info: list[Any] | None = None
    cooldowns: dict[_DirectConnection, int] = dataclasses.field(default_factory=dict)
    enabled: bool = True
    cooldown: int = 0
    consecutive_errors: int = 0


class MyJDConnection(Connection):
    def __init__(
        self,
        api: API,
        device: JDDevice,
        *,
        refresh_direct_connections: bool = True,
    ) -> None:
        self.api: API = api
        self.device: JDDevice = device
        self._direct_ctx: DirectConnectionContext = DirectConnectionContext()
        if refresh_direct_connections:
            self.__refresh_direct_connections()

    def refresh_direct_connections(self) -> None:
        """Check again if a direct connection is possible."""
        self.__refresh_direct_connections()

    def __refresh_direct_connections(self) -> None:
        """Check again if a direct connection is possible."""
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
            self._direct_ctx.cooldowns = {
                conn: self._direct_ctx.cooldowns.get(conn, 0)
                for info in connections
                if (conn := _DirectConnection(**info))
            }

    def enable_direct_connection(self) -> None:
        self._direct_ctx.enabled = True
        self.__refresh_direct_connections()

    def disable_direct_connect(self) -> None:
        self._direct_ctx.enabled = False
        self._direct_ctx.cooldowns.clear()

    def action(
        self,
        path: str,
        params: Any | None = [],
        http_action: Literal["GET", "POST"] = "POST",
        *,
        binary: bool = False,
    ) -> dict | None:
        """Execute any action for the device using the params.

        All the information about the parameters and their default values,
        types, etc. can be found in the API specification for MyJDownloader
        (https://my.jdownloader.org/developers/).

        :param path: The URL of the endpoint (excluding the base url)
        :type path: str
        :param params: URL parameters, in a list of tuples.
            Example: ``[("param1","ex"),("param2","ex2")]`` becomes
            ``/example?param1=ex&param2=ex2``
        :type params: List
        :param http_action: The HTTP request type ('GET' or 'POST')
        :type http_action: str
        :param binary: Return binary response, if needed
        :type binary: bool
        :return: Response from the MyJD API
        :rtype: dict
        """

        action_url = self.__action_url()

        if (
            not self._direct_ctx.enabled
            or self._direct_ctx.info is None
            or time.time() < self._direct_ctx.cooldown
        ):
            # No direct connection available, use the MyJD API
            response = self.api.request(path, http_action, params, action_url, binary=binary)

            if response is None:
                return None
            if binary:
                return response
            if self._direct_ctx.enabled and time.time() >= self._direct_ctx.cooldown:
                self.__refresh_direct_connections()

            if "data" in response:
                return response["data"]
            return response

        # A direct connection is available, try to use it
        now = time.time()
        for connection, cooldown in self._direct_ctx.cooldowns.items():
            if now < cooldown:
                continue
            # Use the direct connection

            api = f"http://{connection.ip}:{connection.port}"

            response = self.api.request(path, http_action, params, action_url, api, binary=binary)

            if response is None:
                # Don't try this connection for a minute.
                connection["cooldown"] = time.time() + 60

            elif binary:
                return response

            else:
                # This connection worked, push it to the top of the
                # list.
                self._direct_ctx.info.remove(connection)
                self._direct_ctx.info.insert(0, connection)
                self._direct_ctx.consecutive_errors = 0

                if "data" in response:
                    return response["data"]
                return response

        # None of the direct connections worked, set a cooldown for all
        # direct connections
        self._direct_ctx.consecutive_errors += 1
        self._direct_ctx.cooldown = int(time.time() + (60 * self._direct_ctx.consecutive_errors))

        # Use the MyJD API instead
        response = self.api.request(path, http_action, params, action_url, binary=binary)

        if response is None:
            return None

        self.__refresh_direct_connections()
        return response.get("data", response)

    def __action_url(self) -> str:
        """Generate the action url for the device and session."""

        return "/t_" + self.api.get_session_token() + "_" + self.device.id
