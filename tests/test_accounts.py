import dataclasses

from pyjd.client import JDDeviceClient
from pyjd.jd_types import AccountQuery, BasicAuthType


def test_add_account(jd: JDDeviceClient) -> None:
    jd.accounts.add_account("youtube.com", "user", "pass")
    jd.accounts.add_account("archive.org", "user", "pass")


def test_add_basic_auth(jd: JDDeviceClient) -> None:
    jd.accounts.add_basic_auth(BasicAuthType.HTTP, "example.org", "user", "pass")


def test_disable_accounts(jd: JDDeviceClient) -> None:
    a = jd.accounts.list_accounts()[0]
    assert a.uuid
    jd.accounts.disable_accounts([a.uuid])
    a = jd.accounts.list_accounts(AccountQuery(uuidlist=[a.uuid]))
    assert not a[0].enabled


def test_enable_accounts(jd: JDDeviceClient) -> None:
    a = jd.accounts.list_accounts()[0]
    assert a.uuid
    jd.accounts.enable_accounts([a.uuid])
    a = jd.accounts.list_accounts(AccountQuery(uuidlist=[a.uuid]))
    assert a[0].enabled is True


def test_get_premium_hoster_url(jd: JDDeviceClient) -> None:
    expected = "https://update3.jdownloader.org/jdserv/BuyPremiumInterface/redirect?https%3A%2F%2Fwww.youtube.com%2F&captcha%2Fwebinterface%2F07072023_1321"
    url = jd.accounts.get_premium_hoster_url("youtube.com")

    assert url[:-13] == expected[:-13]


def test_list_accounts(jd: JDDeviceClient) -> None:
    accounts = jd.accounts.list_accounts()
    assert len(accounts) == 2


def test_list_basic_auths(jd: JDDeviceClient) -> None:
    basicAuths = jd.accounts.list_basic_auth()
    assert len(basicAuths) == 1


def test_list_premium_hoster_and_urls(jd: JDDeviceClient) -> None:
    # test both `list_premium_hoster()` and `list_premium_hoster_urls()`

    hosters = jd.accounts.list_premium_hoster()
    urls = jd.accounts.list_premium_hoster_urls()

    assert type(hosters) is list
    assert type(hosters[0]) is str
    assert type(urls) is dict

    assert len(hosters) == len(urls.keys())


def test_refresh_accounts(jd: JDDeviceClient) -> None:
    accounts = jd.accounts.list_accounts()
    ids = [a.uuid for a in accounts if a.uuid]
    assert ids
    jd.accounts.refresh_accounts(ids)


def test_set_username_and_password(jd: JDDeviceClient) -> None:
    a = jd.accounts.list_accounts()[0]
    assert a.uuid
    res = jd.accounts.set_username_and_password(a.uuid, "test", "pass")
    assert res is True

    a = jd.accounts.list_accounts(AccountQuery(uuidlist=[a.uuid]))
    assert a[0].username == "test"


def test_update_basic_auth(jd: JDDeviceClient) -> None:
    b = jd.accounts.list_basic_auth()[0]
    b = dataclasses.replace(b, username="test")
    res = jd.accounts.update_basic_auth(b)
    assert res is True
    b = jd.accounts.list_basic_auth()[0]
    assert b.username == "test"


def test_remove_accounts(jd: JDDeviceClient) -> None:
    for a in jd.accounts.list_accounts():
        if a and a.uuid:
            jd.accounts.remove_accounts([a.uuid])


def test_remove_basic_auths(jd: JDDeviceClient) -> None:
    b = jd.accounts.list_basic_auth()[0]
    assert b.id
    jd.accounts.remove_basic_auths([b.id])
