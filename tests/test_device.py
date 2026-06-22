from pyjd.jd_device import JDDeviceClient
from pyjd.jd_types import DirectConnectionInfos


def test_get_direct_connection_infos(jd: JDDeviceClient) -> None:
    res = jd.device.get_direct_connection_infos()
    assert isinstance(res, DirectConnectionInfos)


def test_get_session_public_key(jd: JDDeviceClient) -> None:
    jd.device.get_session_public_key()


def test_ping(jd: JDDeviceClient) -> None:
    assert jd.device.ping() is True
