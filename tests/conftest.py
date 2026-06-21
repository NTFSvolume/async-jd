import pytest

from pyjd.direct_connector import DirectConnector
from pyjd.jd_device import JDDevice


@pytest.fixture(name="jd")
def connect_to_jdownloader() -> JDDevice:
    conn = DirectConnector("http://localhost:3128")
    return conn.get_device()
