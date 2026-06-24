from __future__ import annotations

from pyjd.endpoints import Action
from pyjd.jd_types import Account, BasicAuth, BasicAuthType
from pyjd.queries import AccountQuery

type AccountID = int
type URL = str
type Hoster = str


class Accounts(Action, endpoint="accountsV2"):
    def add_account(self, premium_hoster: str, username: str, password: str) -> None:
        params = [premium_hoster, username, password]
        self.action("/addAccount", params)

    def add_basic_auth(
        self,
        auth_type: BasicAuthType,
        hostmask: str,
        username: str,
        password: str,
    ) -> AccountID:
        params = [auth_type.value, hostmask, username, password]
        return self.action("/addBasicAuth", params)

    def disable_accounts(self, account_ids: list[AccountID]) -> None:
        self.action("/disableAccounts", [account_ids])

    def enable_accounts(self, account_ids: list[AccountID]) -> None:
        self.action("/enableAccounts", [account_ids])

    def get_premium_hoster_url(self, hoster: str) -> URL:
        """Get the url for a premium hoster.

        Note: The url will be a redirect over the jdownloader.org servers.
        """
        return self.action("/getPremiumHosterUrl", [hoster])

    def list_accounts(self, account_query: AccountQuery | None = None) -> list[Account]:
        account_query = account_query or AccountQuery()
        params = [account_query.__json__()]
        resp = self.action("/listAccounts", params)
        return [Account(**acc) for acc in resp]

    def list_basic_auth(self) -> list[BasicAuth]:
        resp = self.action("/listBasicAuth")
        return [BasicAuth(**auth) for auth in resp]

    def list_premium_hoster(self) -> list[str]:
        return self.action("/listPremiumHoster")

    def list_premium_hoster_urls(self) -> dict[Hoster, URL]:
        return self.action("/listPremiumHosterUrls")

    def refresh_accounts(self, account_ids: list[AccountID]) -> None:
        resp = self.action("/refreshAccounts", [account_ids])
        return resp == ""

    def remove_accounts(self, account_ids: list[AccountID]) -> None:
        return self.action("/removeAccounts", [account_ids])

    def remove_basic_auths(self, basic_auth_ids: list[AccountID]) -> bool:
        return self.action("/removeBasicAuths", [basic_auth_ids])

    def set_username_and_password(
        self,
        account_id: AccountID,
        username: str,
        password: str,
    ) -> bool:
        params = [account_id, username, password]
        return self.action("/setUserNameAndPassword", params)

    def update_basic_auth(self, basic_auth: BasicAuth) -> bool:
        return self.action("/updateBasicAuth", [basic_auth.__json__()])
