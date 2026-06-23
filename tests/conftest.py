import pytest

from pyjd.client import JDDeviceClient


@pytest.fixture(name="jd")
def connect_to_jdownloader() -> JDDeviceClient:
    return JDDeviceClient.direct_connect("http://localhost:3128")
