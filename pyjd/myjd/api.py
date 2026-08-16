from __future__ import annotations

import json
import logging
import urllib.parse
from typing import TYPE_CHECKING, Any

from pyjd.common import REQUEST_ID, Params, make_request, next_request_id, prepare_api_json
from pyjd.crypto import (
    create_secret,
    decrypt_secret,
    encrypt_secret,
    sign_hmac_sha256,
    update_secret,
)
from pyjd.jd_types import JDDevice
from pyjd.myjd.session import MyJDSession, MyJDSessionBackup

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

    import requests

logger = logging.getLogger(__name__)


class MyJDAPI:
    """Main class for connecting to the MyJD API."""

    def __init__(self, appkey: str | None = None) -> None:
        self.__api_url = "https://api.jdownloader.org"
        self.__app_key = appkey or "https://github.com/NTFSvolume/async-jd"
        self.__api_version = 1
        self.__session: MyJDSession = MyJDSession()

    def __repr__(self) -> str:
        return f"<{type(self).__name__}(session={self.__session!r})>"

    @property
    def __server_encryption_token(self) -> bytes:
        if self.__session.server_encryption_token:
            return self.__session.server_encryption_token
        if not self.__session.login_secret:
            raise RuntimeError("No login secret")
        return self.__session.login_secret

    @property
    def __device_encryption_token(self) -> bytes:
        if not self.__session.device_encryption_token:
            raise RuntimeError("No device encryption token")
        return self.__session.device_encryption_token

    @property
    def session_token(self) -> str:
        if not self.__session.token:
            raise RuntimeError("No session token available")

        return self.__session.token

    @property
    def connected(self) -> bool:
        return self.__session.connected

    @property
    def devices(self) -> tuple[JDDevice, ...]:
        return self.__session.devices

    def set_app_key(self, app_key: str) -> None:
        self.__app_key = app_key

    def __update_encryption_tokens(self) -> None:
        """Update the ``server_encryption_token`` and
        ``device_encryption_token``.
        """

        if not self.__session.device_secret:
            raise RuntimeError("No device secret available")

        self.__session.server_encryption_token = update_secret(
            self.__server_encryption_token, self.session_token
        )
        self.__session.device_encryption_token = update_secret(
            self.__session.device_secret, self.session_token
        )

    def connect(self, email: str, password: str) -> bool:
        self.__session = MyJDSession(
            login_secret=create_secret(email, password, "server"),
            device_secret=create_secret(email, password, "device"),
        )

        url = self._sign_url(
            "/my/connect",
            ("email", email),
            ("appkey", self.__app_key),
            token=self.__session.login_secret,
        )
        response = self.request_json(url)
        self.__session.connected = True
        self.__session.token = response["sessiontoken"]
        self.__session.regain_token = response["regaintoken"]
        self.__update_encryption_tokens()
        self.update_devices()
        return response

    def reconnect(self) -> bool:
        """Re-establish connection to the API.

        :returns: True if successful, False if there was any error.
        :rtype: bool
        """
        url = self._sign_url(
            "/my/reconnect",
            ("sessiontoken", self.session_token),
            ("regaintoken", self.__session.regain_token),
        )
        response = self.request_json(url)
        self.__session.token = response["sessiontoken"]
        self.__session.regain_token = response["regaintoken"]
        self.__update_encryption_tokens()
        return response

    def disconnect(self) -> bool:
        url = self._sign_url("/my/disconnect", ("sessiontoken", self.session_token))
        resp = self.request_json(url)
        self.__session = MyJDSession()
        assert type(resp) is bool
        return resp

    def export_session(self) -> MyJDSessionBackup:
        return MyJDSessionBackup.freeze(self.__session)

    def import_session(self, session: MyJDSessionBackup) -> None:
        self.__session = session.unfreeze()

    def update_devices(self) -> None:
        url = self._sign_url("/my/listdevices", ("sessiontoken", self.session_token))
        response = self.request_json(url, [self.session_token], method="GET")
        self.__session.devices = tuple(JDDevice(**d) for d in response["list"])

    def _sign_url(
        self, path: str, *params: tuple[str, str | None], token: bytes | None = None
    ) -> str:
        query = "&".join([*_quote_query_params(params), f"rid={next_request_id()}"])
        url = f"{path}?{query}"
        sig = sign_hmac_sha256(token or self.__server_encryption_token, url)
        return f"{url}&signature={sig}"

    def get_device(
        self,
        *,
        name: str | None = None,
        id: str | None = None,  # noqa: A002
    ) -> JDDevice:
        if not self.connected:
            raise RuntimeError("No connection established")

        if not (id or name):
            raise ValueError("Either device_id or device_name are required")

        for device in self.__session.devices:
            if id is not None and device.id != id:
                continue
            if name is not None and device.name != name:
                continue

            return device

        raise LookupError("Device not found")

    def request(
        self,
        path: str,
        params: Params | None = None,
        action: str | None = None,
        api: str | None = None,
        method: str = "POST",
    ) -> requests.Response:
        """Make a request to the MyJD API."""
        api = api or self.__api_url
        is_connect = path.partition("?")[0] == "/my/connect"
        if not (self.connected or is_connect):
            raise RuntimeError("No connection established")

        request_url = api + (action or "") + path

        if is_connect or method == "GET":
            resp = make_request(request_url, timeout=30, method="GET")
        else:
            data = prepare_api_json(path, params).encode("utf-8")
            resp = make_request(
                request_url,
                headers={"Content-Type": "application/aesjson-jd; charset=utf-8"},
                data=encrypt_secret(self.__device_encryption_token, data),
                timeout=30,
                method="POST",
            )
        if resp.status_code == 200:
            return resp

        error = _decode_error(resp.text, self.__session.device_encryption_token)
        raise RuntimeError(str(error))

    def request_json(
        self,
        path: str,
        params: Params | None = None,
        action: str | None = None,
        api: str | None = None,
        method: str = "POST",
    ) -> Any:
        """Make a request to the MyJD API."""
        resp = self.request(path, params, action, api, method=method)
        token = self.__server_encryption_token if action is None else self.__device_encryption_token
        return self.decode_response(resp, token)

    def decode_response(self, encrypted_response: requests.Response, token: bytes) -> Any | None:
        response = decrypt_secret(token, encrypted_response.text)
        data = json.loads(response.decode("utf-8"))
        rid = REQUEST_ID.get()
        if data["rid"] != rid:
            raise RuntimeError(f"Request id {rid} does not match {data['rid']}")
        return data


def _quote_query_params(params: Iterable[tuple[str, str | None]] | None) -> Generator[str]:
    if params is None:
        return
    for name, value in params:
        if value is None:
            raise RuntimeError(f"{name} is not available")
        url_value = value if name == "encryptedLoginSecret" else urllib.parse.quote(value)
        yield f"{name}={url_value}"


def _decode_error(text: str, token: bytes | None) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        if not token:
            raise RuntimeError("Failed to decode response: {}", text) from None
        try:
            return json.loads(decrypt_secret(token, text))
        except json.JSONDecodeError:
            raise RuntimeError("Failed to decode response: {}", text) from None
