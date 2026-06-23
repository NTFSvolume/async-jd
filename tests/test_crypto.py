from typing import Literal

import pytest
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from pyjd import crypto


@pytest.mark.parametrize(
    ("email", "password", "domain", "expected"),
    [
        (
            "example@example.com",
            "12@34",
            "server",
            b"\xa8\xe0\xcc\x19[,\x1e\x04z\xba\xd8X\x10\x9e\x86\xde\x93A\xa8,wE\xe2\x1a\xb0\xe5\x1c\xc9\xafb\xd5\xc8",
        ),
        (
            "eXamPle@example.com",
            "12@34",
            "server",
            b"\xa8\xe0\xcc\x19[,\x1e\x04z\xba\xd8X\x10\x9e\x86\xde\x93A\xa8,wE\xe2\x1a\xb0\xe5\x1c\xc9\xafb\xd5\xc8",
        ),
        (
            "example@example.com",
            "12@34",
            "device",
            b"v\x85\x91\xae\xbfl\xf7\xb7)/\xef\x9d\x06\xc4\xa2\xa7\t\xcci\xdf\xd4\xa9c\xd2 KzN\xb8\x06\xb0\xef",
        ),
    ],
)
def test_create_secret(
    email: str, password: str, domain: Literal["server", "device"], expected: bytes
):
    result = crypto.create_secret(email, password, domain)
    assert result == expected


@pytest.mark.parametrize(
    ("key", "url", "expected"),
    [
        (
            b"1234",
            "https://example.com/a/b?file=1",
            "c505e775a51039fee7e385f9e28d105a5dca5426da654edd4f4bf4ac7f476612",
        ),
        (
            b"1234",
            "https://example.com/a/b?file=2",
            "2701b114ed1d2d5952ef05f12ebf5785c0bc7482177346f5b6a6df05e83de1a8",
        ),
    ],
)
def test_sign_hmac_sha256(key: bytes, url: str, expected: str) -> None:
    result = crypto.sign_hmac_sha256(key, url)
    assert result == expected


@pytest.mark.parametrize(
    ("key", "data", "expected"),
    [
        (b"1234", b"example.com", "t/W/ycEH0pkui735HsPg9A=="),
        (b"1234", b"example2.com", "Ctt67f4/+iUzHsYmtH/JAA=="),
        (b"abcd", b"example.com", "pmJ066On8lPcT3LgCEd85g=="),
    ],
)
def test_encrypt_secret(key: bytes, data: bytes, expected: str) -> None:
    result = crypto.encrypt_secret(pad(key, AES.block_size * 2), data)
    assert result == expected


@pytest.mark.parametrize(
    ("key", "data", "expected"),
    [
        (b"1234", "t/W/ycEH0pkui735HsPg9A==", b"example.com"),
        (b"1234", "Ctt67f4/+iUzHsYmtH/JAA==", b"example2.com"),
        (b"abcd", "pmJ066On8lPcT3LgCEd85g==", b"example.com"),
    ],
)
def test_decrypt_secret(key: bytes, data: str, expected: str) -> None:
    result = crypto.decrypt_secret(pad(key, AES.block_size * 2), data)
    assert result == expected


@pytest.mark.parametrize(
    ("secret", "session_token", "expected"),
    [
        (
            b"1234",
            "31323334",
            b"\x17\x18\xc2K\x10\xae\xb8\t\x9e?\xc4I`\xabiI\xabv\xa2g5$Y\xf2\x03\xea\x106\xbe\xc3\x82\xc2",
        ),
        (
            b"abcd",
            "31323334",
            b"\xe9\xce\xe7\x1a\xb92\xfd\xe8c3\x8d\x08\xbeM\xe9\xdf\xe3\x9e\xa0I\xbd\xaf\xb3B\xcee\x9e\xc5E\x0bi\xae",
        ),
    ],
)
def test_update_secret(secret: bytes, session_token: str, expected: str) -> None:
    result = crypto.update_secret(secret, session_token)
    assert result == expected
