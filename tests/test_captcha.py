from pyjd.client import JDDeviceClient


def test_get() -> None:
    # no captchas available for testing
    assert True


def test_get_captcha_job() -> None:
    # no captcha jobs available for testing
    assert True


def test_list(jd: JDDeviceClient) -> None:
    jd.captcha.list()


def test_skip() -> None:
    # no captchas available for testing
    assert True


def test_solve() -> None:
    # no captchas available for testing
    assert True
