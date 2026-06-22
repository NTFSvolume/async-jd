import pytest

from pyjd.direct import DirectConnection
from pyjd.jd_device import JDDeviceClient


@pytest.fixture(name="jd")
def connect_to_jdownloader() -> JDDeviceClient:
    conn = DirectConnection("http://localhost:3128")
    return conn.get_device()
