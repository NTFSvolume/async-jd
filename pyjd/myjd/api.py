from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import time
import urllib.parse
from typing import TYPE_CHECKING, Any, Literal

from pyjd.common import make_request
from pyjd.crypto import create_secret, decrypt_secret, encrypt_secret, sign_hmac_sha256
from pyjd.jd_types import JDDevice
from pyjd.myjd.session import MyJDSession, MyJDSessionBackup

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

    import requests

logger = logging.getLogger(__name__)


def _new_request_id() -> int:
    return int(time.time() * 1000)


class MyJDAPI:
    """Main class for connecting to the MyJD API."""

    def __init__(self, appkey: str | None = None) -> None:
        self.__request_id = _new_request_id()
        self.__api_url = "https://api.jdownloader.org"
        self.__app_key = appkey or "https://github.com/NTFSvolume/async-jd"
        self.__api_version = 1
        self._session: MyJDSession = MyJDSession()

    def __repr__(self) -> str:
        return f"<{type(self).__name__}(session={self._session!r})>"

    @property
    def session_token(self) -> str:
        if not self._session.token:
            raise RuntimeError("No session token available")

        return self._session.token

    @property
    def __server_encryption_token(self) -> bytes:
        if self._session.server_encryption_token:
            return self._session.server_encryption_token
        if not self._session.login_secret:
            raise RuntimeError("No login secret")
        return self._session.login_secret

    @property
    def __device_encryption_token(self) -> bytes:
        if not self._session.device_encryption_token:
            raise RuntimeError("No device encryption token")
        return self._session.device_encryption_token

    @property
    def connected(self) -> bool:
        return self._session.connected

    def set_app_key(self, app_key: str) -> None:
        self.__app_key = app_key

    def __update_encryption_tokens(self) -> None:
        """Update the ``server_encryption_token`` and
        ``device_encryption_token``.
        """

        s_token = self.session_token

        if not self._session.device_secret:
            raise RuntimeError("No device secret available")

        def digest(token: bytes) -> bytes:
            return hashlib.sha256(token + bytearray.fromhex(s_token)).digest()

        self._session.server_encryption_token = digest(self.__server_encryption_token)
        self._session.device_encryption_token = digest(self._session.device_secret)

    def update_request_id(self) -> None:
        """Update ``__request_id``.

        This has to be done for every new request.
        """
        self.__request_id = _new_request_id()

    def connect(self, email: str, password: str) -> bool:
        self.update_request_id()
        self._session = MyJDSession(
            login_secret=create_secret(email, password, "server"),
            device_secret=create_secret(email, password, "device"),
        )
        response = self.request_json(
            "/my/connect",
            "GET",
            [
                ("email", email),
                ("appkey", self.__app_key),
            ],
        )
        self._session.connected = True
        self.update_request_id()
        self._session.token = response["sessiontoken"]
        self._session.regain_token = response["regaintoken"]
        self.__update_encryption_tokens()
        self.update_devices()
        return response

    def reconnect(self) -> bool:
        """Re-establish connection to the API.

        :returns: True if successful, False if there was any error.
        :rtype: bool
        """
        response = self.request_json(
            "/my/reconnect",
            "GET",
            [
                ("sessiontoken", self._session.token),
                ("regaintoken", self._session.regain_token),
            ],
        )
        self.update_request_id()
        self._session.token = response["sessiontoken"]
        self._session.regain_token = response["regaintoken"]
        self.__update_encryption_tokens()
        return response

    def disconnect(self) -> bool:
        """Disconnect from the API.

        :returns: True if successful, False if there was any error.
        :rtype: bool
        """

        response = self.request_json(
            "/my/disconnect", "GET", [("sessiontoken", self._session.token)]
        )
        self.update_request_id()
        self._session = MyJDSession()
        return response

    def export_session(self) -> MyJDSessionBackup:
        return MyJDSessionBackup.freeze(self._session)

    def import_session(self, session: MyJDSessionBackup | MyJDSession) -> None:
        if type(session) is MyJDSession:
            self._session = dataclasses.replace(session)
        else:
            self._session = session.unfreeze()

    def update_devices(self) -> bool:
        response = self.request_json(
            "/my/listdevices", "GET", [("sessiontoken", self._session.token)]
        )
        self.update_request_id()
        self._session.devices = [JDDevice(**d) for d in response["list"]]
        return response

    @property
    def devices(self) -> list[JDDevice]:
        return self._session.devices

    def get_device(self, device_name: str | None = None, device_id: str | None = None) -> JDDevice:
        if not self.connected:
            raise RuntimeError("No connection established\n")

        if not (device_id or device_name):
            raise ValueError("Either device_id or device_name are required")

        for device in self._session.devices:
            if device_id is not None and device.id != device_id:
                continue
            if device_name is not None and device.name != device_name:
                continue

            return device

        raise LookupError("Device not found\n")

    def raw_request(
        self,
        path: str,
        http_method: Literal["GET", "POST"] = "GET",
        params: Iterable[tuple[str, Any]] | None = None,
        action: str | None = None,
        api: str | None = None,
    ) -> requests.Response:
        """Make a request to the MyJD API."""

        api = api or self.__api_url
        data = None
        query = None
        json_data = None
        if not self.connected and path != "/my/connect":
            raise RuntimeError("No connection established\n")

        if http_method == "GET":
            query = "&".join([*_prepare_get_query(params), f"rid={self.__request_id}"])
            url = f"{path}?{query}"
            sig = sign_hmac_sha256(self.__server_encryption_token, url)
            request_url = f"{api}{url}&signature={sig}"
        else:
            data = json.dumps(
                {
                    "apiVer": self.__api_version,
                    "url": path,
                    "params": list(_prepare_post_query(params)),
                    "rid": self.__request_id,
                }
            )
            # Removing quotes around null elements.
            data = data.replace('"null"', "null").replace("'null'", "null")
            b_data = data.encode("utf-8")
            if not self._session.device_encryption_token:
                raise RuntimeError("No device encryption token\n")

            json_data = encrypt_secret(self._session.device_encryption_token, b_data)
            request_url = api + (action or "") + path

        resp = make_request(
            request_url,
            headers={"Content-Type": "application/aesjson-jd; charset=utf-8"}
            if json_data
            else None,
            data=json_data,
            timeout=3,
        )
        if resp.status_code == 200:
            return resp

        error_msg = self._decode_error(resp)

        msg = (
            "\n\tSOURCE: "
            + error_msg["src"]
            + "\n\tTYPE: "
            + error_msg["type"]
            + "\n------\nREQUEST_URL: "
            + api
            + path
        )

        if http_method == "GET" and query:
            msg += query

        msg += "\n"
        if data is not None:
            msg += "DATA:\n" + data

        raise RuntimeError(msg)

    def request_json(
        self,
        path: str,
        http_method: Literal["GET", "POST"] = "GET",
        params: Iterable[tuple[str, Any]] | None = None,
        action: str | None = None,
        api: str | None = None,
    ) -> Any:
        """Make a request to the MyJD API."""
        resp = self.raw_request(path, http_method, params, action, api)
        return self._decode_response(resp, action)

    def request_bytes(
        self,
        path: str,
        http_method: Literal["GET", "POST"] = "GET",
        params: Iterable[tuple[str, Any]] | None = None,
        action: str | None = None,
        api: str | None = None,
    ) -> bytes:
        resp = self.raw_request(path, http_method, params, action, api)
        self.update_request_id()
        # Binary content is not encrypted
        return resp.content

    def _decode_error(self, encrypted_response: requests.Response) -> Any:
        try:
            return json.loads(encrypted_response.text)
        except json.JSONDecodeError:
            try:
                return json.loads(
                    decrypt_secret(self.__device_encryption_token, encrypted_response.text)
                )
            except json.JSONDecodeError:
                raise RuntimeError(
                    "Failed to decode response: {}", encrypted_response.text
                ) from None

    def _decode_response(
        self, encrypted_response: requests.Response, action: str | None
    ) -> Any | None:
        secret_token = (
            self.__server_encryption_token if action is None else self.__device_encryption_token
        )

        response = decrypt_secret(secret_token, encrypted_response.text)
        json_data = json.loads(response.decode("utf-8"))
        if json_data["rid"] != self.__request_id:
            self.update_request_id()
            return None

        self.update_request_id()
        return json_data


def _prepare_get_query(params: Iterable[tuple[str, str]] | None) -> Generator[str]:
    if params is None:
        return
    for name, value in params:
        url_value = value if name == "encryptedLoginSecret" else urllib.parse.quote(value)
        yield f"{name}={url_value}"


def _prepare_post_query(params: Iterable[Any] | None = None) -> Generator[Any]:
    if params is None:
        return

    for param in params:
        yield param if isinstance(param, list) else json.dumps(param)
