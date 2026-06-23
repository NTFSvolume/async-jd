from __future__ import annotations

import base64
import hashlib
import hmac

from Crypto.Cipher import AES


def _pad_bytes(string: bytes) -> bytes:
    """Pad a string

    :param s: String to pad
    :type s: bytes
    :return: Padded ``s``.
    :rtype: bytes
    """

    return (
        string
        + (
            (AES.block_size - len(string) % AES.block_size)
            * chr(AES.block_size - len(string) % AES.block_size)
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


def create_secret(email: str, password: str, domain: str) -> bytes:
    """Create the login_secret and device_secret.

    :param domain: The domain of the secret ("server" for login_secret and
        "device" for device_secret)
    """

    data = email.lower() + password + domain.lower()
    return hashlib.sha256(data.encode("utf-8")).digest()


def sign_hmac_sha256(key: bytes, data: str) -> str:
    return hmac.new(key, data.encode("utf-8"), hashlib.sha256).hexdigest()


def encrypt_secret(secret_token: bytes, data: bytes) -> str:
    data = _pad_bytes(data)
    middle = len(secret_token) // 2
    init_vector, key = secret_token[:middle], secret_token[middle:]
    cypher = AES.new(key, AES.MODE_CBC, init_vector)
    return base64.b64encode(cypher.encrypt(data)).decode("utf-8")


def decrypt_secret(secret_token: bytes, data: str) -> bytes:
    middle = len(secret_token) // 2
    init_vector, key = secret_token[:middle], secret_token[middle:]
    cypher = AES.new(key, AES.MODE_CBC, init_vector)
    return _unpad_bytes(cypher.decrypt(base64.b64decode(data)))
