from pyjd.jd_device import JDDevice
from pyjd.jd_types import DirectConnectionInfos


def test_get_direct_connection_infos(jd: JDDevice) -> None:
    res = jd.device.get_direct_connection_infos()
    assert isinstance(res, DirectConnectionInfos)


def test_get_session_public_key(jd: JDDevice) -> None:
    jd.device.get_session_public_key()


def test_ping(jd: JDDevice) -> None:
    assert jd.device.ping() is True
