import pytest

from pyjd.jd_device import JDDevice


@pytest.mark.parametrize(
    "url",
    [
        "youtube.com",
        "example.org",
    ],
)
def test_get_fav_icon(jd: JDDevice, url: str) -> None:
    assert type(jd.content.get_fav_icon(url)) == bytes


def test_get_file_icon(jd: JDDevice) -> None:
    assert type(jd.content.get_file_icon(".rar")) == bytes


def test_get_icon(jd: JDDevice) -> None:
    assert type(jd.content.get_icon("clear", 18)) == bytes
