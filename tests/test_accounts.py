from __future__ import annotations

import dataclasses
import uuid
from typing import TYPE_CHECKING

from pyjd.jd_types import Account, BasicAuth, BasicAuthType
from pyjd.queries import AccountQuery

if TYPE_CHECKING:
    from collections.abc import Iterable

    from pyjd.client import JDDeviceClient


def _all_same_type(values: Iterable[object], type_: type) -> bool:
    return set(map(type, values)) == {type_}


def _new_account(jd: JDDeviceClient, hoster: str = "youtube.com") -> str:
    username = str(uuid.uuid4())
    jd.accounts.add_account(hoster, username, "pass2")
    return username


def test_add_account(jd: JDDeviceClient) -> None:
    username = _new_account(jd)
    username2 = _new_account(jd, "host that does not exists.com")
    names = [a.username for a in jd.accounts.list_accounts()]
    assert username in names
    assert username2 not in names


def test_disable_accounts(jd: JDDeviceClient) -> None:
    username = _new_account(jd)
    accounts = jd.accounts.list_accounts()
    account = next(a for a in accounts if a.username == username)
    jd.accounts.disable_accounts([account.uuid])
    account = jd.accounts.list_accounts(AccountQuery(uuidlist=[account.uuid]))
    assert not account[0].enabled


def test_enable_accounts(jd: JDDeviceClient) -> None:
    username = _new_account(jd)
    account = next(a for a in jd.accounts.list_accounts() if a.username == username)
    assert account.enabled is True

    def get_account():
        return jd.accounts.list_accounts(AccountQuery(uuidlist=[account.uuid]))[0]

    jd.accounts.disable_accounts([account.uuid])
    assert get_account().enabled is None
    jd.accounts.enable_accounts([account.uuid])
    assert get_account().enabled is True


def test_get_premium_hoster_url(jd: JDDeviceClient) -> None:
    destination = "https%3A%2F%2Fwww.youtube.com%2F&captcha%2Fwebinterface"
    expected = "https://update3.jdownloader.org/jdserv/BuyPremiumInterface/redirect?" + destination
    url = jd.accounts.get_premium_hoster_url("youtube.com")
    assert type(url) is str
    assert url
    query = url.rpartition("?")[-1]
    assert query.startswith(destination)
    assert url.startswith(expected)


def test_list_accounts(jd: JDDeviceClient) -> None:
    accounts = jd.accounts.list_accounts()
    assert type(accounts) is list
    old_accounts = len(accounts)
    _ = _new_account(jd)
    new_accounts = jd.accounts.list_accounts()
    assert old_accounts + 1 == len(new_accounts)
    assert _all_same_type(new_accounts, Account)


def test_list_premium_hoster(jd: JDDeviceClient) -> None:
    hosters = jd.accounts.list_premium_hoster()
    assert type(hosters) is list
    assert type(hosters[0]) is str
    assert len(hosters) > 500


def test_list_premium_hoster_and_urls(jd: JDDeviceClient) -> None:
    urls = jd.accounts.list_premium_hoster_urls()
    hosters = jd.accounts.list_premium_hoster()
    assert type(urls) is dict
    assert len(hosters) == len(urls.keys())
    _ = urls.pop("genericusenet")
    assert _all_same_type(urls.values(), str)


def test_refresh_accounts(jd: JDDeviceClient) -> None:
    accounts = jd.accounts.list_accounts()
    ids = [a.uuid for a in accounts if a.uuid]
    assert len(ids) > 0
    assert jd.accounts.refresh_accounts(ids) is True


def test_set_username_and_password(jd: JDDeviceClient) -> None:
    a = jd.accounts.list_accounts()[0]
    assert a.uuid
    username = str(uuid.uuid4())
    res = jd.accounts.set_username_and_password(a.uuid, username, "pass")
    assert res is True
    a = jd.accounts.list_accounts(AccountQuery(uuidlist=[a.uuid]))
    assert a[0].username == username


def test_add_basic_auth(jd: JDDeviceClient) -> None:
    resp = jd.accounts.add_basic_auth(BasicAuthType.HTTP, "example.org", "user", "pass")
    assert type(resp) is int
    assert resp > 1e5


def test_update_basic_auth(jd: JDDeviceClient) -> None:
    username = str(uuid.uuid4())
    account_id = jd.accounts.add_basic_auth(BasicAuthType.HTTP, "example.org", username, "pass")

    def get_account():
        return next(f for f in jd.accounts.list_basic_auth() if account_id == f.id)

    username2 = str(uuid.uuid4())
    updated_account = dataclasses.replace(get_account(), username=username2)
    assert jd.accounts.update_basic_auth(updated_account) is True

    updated_account = next(f for f in jd.accounts.list_basic_auth() if updated_account.id == f.id)
    assert get_account().username == username2


def test_remove_accounts(jd: JDDeviceClient) -> None:
    username = str(uuid.uuid4())
    jd.accounts.add_account("youtube.com", username, "pass2")
    accounts = [a.uuid for a in jd.accounts.list_accounts()]
    assert accounts
    jd.accounts.remove_accounts(accounts)
    assert jd.accounts.list_accounts() == []


def test_list_basic_auths(jd: JDDeviceClient) -> None:
    jd.accounts.add_basic_auth(BasicAuthType.HTTP, "example.org", "user", "pass")
    accounts = jd.accounts.list_basic_auth()
    assert type(accounts) is list
    assert len(accounts) > 0
    assert _all_same_type(accounts, BasicAuth)


def test_remove_basic_auths(jd: JDDeviceClient) -> None:
    username = str(uuid.uuid4())
    jd.accounts.add_basic_auth(BasicAuthType.HTTP, "example.org", username, "pass")
    accounts = jd.accounts.list_basic_auth()
    assert accounts
    jd.accounts.remove_basic_auths([a.id for a in accounts])
    assert jd.accounts.list_basic_auth() == []
