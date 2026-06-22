import base64
import dataclasses
import hashlib
import hmac
import json
import logging
import time
from collections.abc import Generator, Iterable
from typing import Any, Literal
from urllib.parse import quote

import requests
from Crypto.Cipher import AES

from pyjd.jd_device import DeviceDict, JDDevice
from pyjd.myjd_connection_helper import MyJDConnectionHelper

logger = logging.getLogger(__name__)

_AES_BLOCK_SIZE = 16


@dataclasses.dataclass(slots=True)
class Session:
    login_secret: bytes | None = None
    device_secret: bytes | None = None
    session_token: str | None = None
    regain_token: str | None = None
    server_encryption_token: bytes | None = None
    device_encryption_token: bytes | None = None
    devices: list[DeviceDict] = dataclasses.field(default_factory=list)
    connected: bool = False


def _pad_bytes(s: bytes) -> bytes:
    """Pad a string

    :param s: String to pad
    :type s: bytes
    :return: Padded ``s``.
    :rtype: bytes
    """

    return (
        s
        + (
            (_AES_BLOCK_SIZE - len(s) % _AES_BLOCK_SIZE)
            * chr(_AES_BLOCK_SIZE - len(s) % _AES_BLOCK_SIZE)
        ).encode()
    )


def _unpad_bytes(s: bytes) -> bytes:
    """Unpad a string.

    :param s: String to unpad
    :type s: bytes
    :return: Unpadded ``s``.
    :rtype: bytes
    """

    return s[0 : -s[-1]]


class MyJDConnector:
    """Main class for connecting to the MyJD API."""

    def __init__(self) -> None:
        """Initialize MyJD connector."""

        self.__request_id = int(time.time() * 1000)
        self.__api_url = "https://api.jdownloader.org"
        self.__app_key = "https://github.com/NTFSvolume/async-jd"
        self.__api_version = 1
        self.__devices: list[DeviceDict] = []
        self.__login_secret: bytes | None = None
        self.__device_secret: bytes | None = None
        self.__session_token: str | None = None
        self.__regain_token = None
        self.__server_encryption_token: bytes | None = None
        self.__device_encryption_token: bytes | None = None
        self.__connected = False
        self._session: Session = Session()

    @property
    def session_token(self) -> str | None:
        return self.__session_token

    @property
    def connected(self) -> bool:
        return self.__connected

    def set_app_key(self, app_key: str) -> None:
        self.__app_key = app_key

    def __update_encryption_tokens(self) -> None:
        """Update the ``server_encryption_token`` and
        ``device_encryption_token``.
        """
        if not self.__session_token:
            raise RuntimeError("No session token available")

        s_token = self.__session_token

        if not self.__device_secret:
            raise RuntimeError("No device secret available")

        def digest(token: bytes) -> bytes:
            return hashlib.sha256(token + bytearray.fromhex(s_token)).digest()

        self.__server_encryption_token = digest(self._server_encryption_token())
        self.__device_encryption_token = digest(self.__device_secret)

    def update_request_id(self) -> None:
        """Update ``__request_id``.

        This has to be done for every new request.
        """

        self.__request_id = int(time.time())

    def connect(self, email: str, password: str) -> bool:
        self.update_request_id()
        self.__login_secret = None
        self.__device_secret = None
        self.__session_token = None
        self.__regain_token = None
        self.__server_encryption_token = None
        self.__device_encryption_token = None
        self.__devices = []
        self.__connected = False

        self.__login_secret = _create_secret(email, password, "server")
        self.__device_secret = _create_secret(email, password, "device")
        response = self.request_api(
            "/my/connect",
            "GET",
            [
                ("email", email),
                ("appkey", self.__app_key),
            ],
        )
        self.__connected = True
        self.update_request_id()
        self.__session_token = response["sessiontoken"]
        self.__regain_token = response["regaintoken"]
        self.__update_encryption_tokens()
        self.update_devices()

        return response

    def reconnect(self) -> bool:
        """Re-establish connection to the API.

        :returns: True if successful, False if there was any error.
        :rtype: bool
        """

        response = self.request_api(
            "/my/reconnect",
            "GET",
            [
                ("sessiontoken", self.__session_token),
                ("regaintoken", self.__regain_token),
            ],
        )
        self.update_request_id()
        self.__session_token = response["sessiontoken"]
        self.__regain_token = response["regaintoken"]
        self.__update_encryption_tokens()
        return response

    def disconnect(self) -> bool:
        """Disconnect from the API.

        :returns: True if successful, False if there was any error.
        :rtype: bool
        """

        response = self.request_api(
            "/my/disconnect", "GET", [("sessiontoken", self.__session_token)]
        )
        self.update_request_id()
        self.__login_secret = None
        self.__device_secret = None
        self.__session_token = None
        self.__regain_token = None
        self.__server_encryption_token = None
        self.__device_encryption_token = None
        self.__devices = []
        self.__connected = False
        self._session = Session()

        return response

    def get_session(self) -> dict[str, Any]:
        """Get the current session.

        :returns: The current session
        :rtype: dict
        """

        def encode(val: bytes | None) -> str | None:
            return base64.b64encode(val).decode("ASCII") if val else None

        return {
            "login_secret": encode(self.__login_secret),
            "device_secret": encode(self.__device_secret),
            "session_token": self.__session_token,
            "regain_token": self.__regain_token,
            "server_encryption_token": encode(self.__server_encryption_token),
            "device_encryption_token": encode(self.__device_encryption_token),
            "devices": self.__devices,
            "connected": self.__connected,
        }

    def from_session(self, session: dict[str, Any]) -> None:
        def decode(val: str) -> bytes:
            return base64.b64decode(val.encode("ASCII"))

        self.__login_secret = decode(session["login_secret"])
        self.__device_secret = decode(session["device_secret"])
        self.__session_token = session["session_token"]
        self.__regain_token = session["regain_token"]
        self.__server_encryption_token = decode(session["server_encryption_token"])
        self.__device_encryption_token = decode(session["device_encryption_token"])
        self.__devices = session["devices"]
        self.__connected = session["connected"]

    def update_devices(self) -> bool:
        response = self.request_api(
            "/my/listdevices", "GET", [("sessiontoken", self.__session_token)]
        )
        self.update_request_id()
        self.__devices = response["list"]
        return response

    @property
    def devices(self) -> list[DeviceDict]:
        return [d.copy() for d in self.__devices]

    def get_device(
        self,
        device_name: str | None = None,
        device_id: str | None = None,
        refresh_direct_connections=True,
    ) -> JDDevice:

        if not self.connected:
            raise (Exception("No connection established\n"))

        if not (device_id or device_name):
            raise ValueError("Either device_id or device_name are required")

        for device in self.__devices:
            if device_id is not None and device["id"] != device_id:
                continue
            if device_name is not None and device["name"] != device_name:
                continue

            return JDDevice(
                self,
                MyJDConnectionHelper,
                device,
                refresh_direct_connections=refresh_direct_connections,
            )

        raise (Exception("Device not found\n"))

    def request_api(
        self,
        path: str,
        http_method: Literal["GET", "POST"] = "GET",
        params: Iterable[tuple[str, Any]] | None = None,
        action: str | None = None,
        api: str | None = None,
        binary: bool = False,
    ) -> Any:
        """Make a request to the MyJD API."""

        api = api or self.__api_url
        data = None
        query = None
        json_data = None
        if not self.connected and path != "/my/connect":
            raise (RuntimeError("No connection established\n"))

        if http_method == "GET":
            query = "&".join([*_prepare_get_query(params), f"rid={self.__request_id}"])
            url = f"{path}?{query}"
            sig = _sign_hmac_sha256(self._server_encryption_token(), url)
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
            if not self.__device_encryption_token:
                raise RuntimeError("No device encryption token\n")

            json_data = _encrypt(self.__device_encryption_token, b_data)
            request_url = api + (action or "") + path

        try:
            encrypted_response = _make_request(
                request_url,
                headers={"Content-Type": "application/aesjson-jd; charset=utf-8"}
                if json_data
                else None,
                data=json_data,
                timeout=3,
            )

        except requests.exceptions.RequestException:
            return None

        if encrypted_response.status_code != 200:
            error_msg = self._decode_error(encrypted_response)

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

            raise (RuntimeError(msg))

        if binary:
            self.update_request_id()

            # Binary content is not encrypted
            return encrypted_response.content

        return self._decode_response(encrypted_response, action)

    def _decode_error(self, encrypted_response: requests.Response) -> Any:
        try:
            return json.loads(encrypted_response.text)
        except json.JSONDecodeError:
            try:
                return json.loads(
                    _decrypt(self._device_encryption_token(), encrypted_response.text)
                )
            except json.JSONDecodeError:
                raise RuntimeError(
                    "Failed to decode response: {}", encrypted_response.text
                ) from None

    def _server_encryption_token(self) -> bytes:
        if self.__server_encryption_token:
            return self.__server_encryption_token
        if not self.__login_secret:
            raise RuntimeError("No login secret\n")
        return self.__login_secret

    def _device_encryption_token(self) -> bytes:
        if not self.__device_encryption_token:
            raise RuntimeError("No device encryption token\n")
        return self.__device_encryption_token

    def _decode_response(
        self, encrypted_response: requests.Response, action: str | None
    ) -> Any | None:
        secret_token = (
            self._server_encryption_token() if action is None else self._device_encryption_token()
        )

        response = _decrypt(secret_token, encrypted_response.text)
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
        url_value = value if name == "encryptedLoginSecret" else quote(value)
        yield f"{name}={url_value}"


def _prepare_post_query(params: Iterable[Any] | None = None) -> Generator[Any]:
    if params is None:
        return

    for param in params:
        yield param if isinstance(param, list) else json.dumps(param)


def _make_request(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: Any = None,
    timeout: int = 60,
) -> requests.Response:
    logger.debug(f"Request to {url}")
    return requests.get(url, headers=headers, timeout=timeout, data=data)


def _create_secret(email: str, password: str, domain: str) -> bytes:
    """Create the login_secret and device_secret.

    :param domain: The domain of the secret ("server" for login_secret and
        "device" for device_secret)
    """

    data = email.lower() + password + domain.lower()
    return hashlib.sha256(data.encode("utf-8")).digest()


def _sign_hmac_sha256(key: bytes, data: str) -> str:
    return hmac.new(key, data.encode("utf-8"), hashlib.sha256).hexdigest()


def _encrypt(secret_token: bytes, data: bytes) -> str:
    data = _pad_bytes(data)
    middle = len(secret_token) // 2
    init_vector, key = secret_token[:middle], secret_token[middle:]
    cypher = AES.new(key, AES.MODE_CBC, init_vector)
    return base64.b64encode(cypher.encrypt(data)).decode("utf-8")


def _decrypt(secret_token: bytes, data: str) -> bytes:
    middle = len(secret_token) // 2
    init_vector, key = secret_token[:middle], secret_token[middle:]
    cypher = AES.new(key, AES.MODE_CBC, init_vector)
    return _unpad_bytes(cypher.decrypt(base64.b64decode(data)))
