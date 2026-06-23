import dataclasses

from pyjd.client import JDDeviceClient
from pyjd.queries import AdvancedConfigQuery


def test_get(jd: JDDeviceClient) -> None:
    cfg = jd.config.get(
        "org.jdownloader.plugins.components.youtube.YoutubeConfig",
        "cfg/plugins/youtube/Youtube",
        "MaxVideoResolution",
    )
    assert cfg == "P_4320"  # this is jdownloader's default value


def test_get_default(jd: JDDeviceClient) -> None:
    cfg = jd.config.get(
        "org.jdownloader.plugins.components.youtube.YoutubeConfig",
        "cfg/plugins/youtube/Youtube",
        "MaxVideoResolution",
    )
    assert cfg == "P_4320"  # this is jdownloader's default value


def test_list(jd: JDDeviceClient) -> None:
    youtube_config = jd.config.list(".*youtube.*")
    all_config = jd.config.list()
    assert len(youtube_config) > 0
    assert len(youtube_config) < len(all_config)


def test_list_enum(jd: JDDeviceClient) -> None:
    options = jd.config.list_enum("org.jdownloader.plugins.components.youtube.itag.VideoResolution")
    assert type(options) is list
    assert len(options) > 0


def test_query(jd: JDDeviceClient) -> None:
    query = AdvancedConfigQuery.default()
    query = dataclasses.replace(query, pattern=".*youtube.*")
    res = jd.config.query(query)
    assert type(res) is list
    assert len(res) > 0


def test_set(jd: JDDeviceClient) -> None:
    res = jd.config.set(
        "org.jdownloader.plugins.components.youtube.YoutubeConfig",
        "cfg/plugins/youtube/Youtube",
        "MaxVideoResolution",
        "P_1080",
    )
    assert res

    value = jd.config.get(
        "org.jdownloader.plugins.components.youtube.YoutubeConfig",
        "cfg/plugins/youtube/Youtube",
        "MaxVideoResolution",
    )
    assert value == "P_1080"


def test_reset(jd: JDDeviceClient) -> None:
    res = jd.config.reset(
        "org.jdownloader.plugins.components.youtube.YoutubeConfig",
        "cfg/plugins/youtube/Youtube",
        "MaxVideoResolution",
    )
    assert res

    value = jd.config.get(
        "org.jdownloader.plugins.components.youtube.YoutubeConfig",
        "cfg/plugins/youtube/Youtube",
        "MaxVideoResolution",
    )
    assert value == "P_4320"
