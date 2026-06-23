from __future__ import annotations

import base64
import dataclasses
from typing import TYPE_CHECKING, Self, final

if TYPE_CHECKING:
    from pyjd.jd_types import JDDevice


@final
@dataclasses.dataclass(slots=True)
class MyJDSession:
    login_secret: bytes | None = None
    device_secret: bytes | None = None
    token: str | None = None
    regain_token: str | None = None
    server_encryption_token: bytes | None = None
    device_encryption_token: bytes | None = None
    devices: tuple[JDDevice, ...] = ()
    connected: bool = False

    def __repr__(self) -> str:
        return f"<{type(self).__name__}(token={self.token!r}, connected={self.connected!r}, devices={len(self.devices)!r})>"


@dataclasses.dataclass(slots=True, frozen=True)
class MyJDSessionBackup:
    login_secret: str | None
    device_secret: str | None
    token: str | None
    regain_token: str | None
    server_encryption_token: str | None
    device_encryption_token: str | None
    devices: tuple[JDDevice, ...]
    connected: bool

    @staticmethod
    def encode_secret(val: bytes | None) -> str | None:
        return base64.b64encode(val).decode("ASCII") if val else None

    @staticmethod
    def decode_secret(val: str | None) -> bytes | None:
        return base64.b64decode(val.encode("ASCII")) if val else None

    @classmethod
    def freeze(cls, session: MyJDSession) -> Self:
        return cls(
            login_secret=cls.encode_secret(session.login_secret),
            device_secret=cls.encode_secret(session.device_secret),
            token=session.token,
            regain_token=session.regain_token,
            server_encryption_token=cls.encode_secret(session.server_encryption_token),
            device_encryption_token=cls.encode_secret(session.device_encryption_token),
            devices=session.devices,
            connected=session.connected,
        )

    def unfreeze(self) -> MyJDSession:
        return MyJDSession(
            login_secret=self.decode_secret(self.login_secret),
            device_secret=self.decode_secret(self.device_secret),
            token=self.token,
            regain_token=self.regain_token,
            server_encryption_token=self.decode_secret(self.server_encryption_token),
            device_encryption_token=self.decode_secret(self.device_encryption_token),
            devices=list(self.devices),
            connected=self.connected,
        )
