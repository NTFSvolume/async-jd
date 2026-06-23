from __future__ import annotations

from pyjd.endpoints import Action
from pyjd.jd_types import Account, BasicAuth, BasicAuthType
from pyjd.queries import AccountQuery


class Accounts(Action, endpoint="accountsV2"):
    def add_account(self, premium_hoster: str, username: str, password: str) -> None:
        """Add a premium hoster account.

        .. warning:: The password is used in plain text, so beware...

        :param premium_hoster: The name of the premium hoster.
            See ``list_premium_hoster`` for possible names.
        :type premium_hoster: str
        :param username: User name or email address for that account.
        :type username: str
        :param password: Password for that account.
        :type password: str
        :return: empty
        :rtype: None
        """

        params = [premium_hoster, username, password]
        self.action("/addAccount", params)

    def add_basic_auth(
        self, auth_type: BasicAuthType, hostmask: str, username: str, password: str
    ) -> int:
        """Add a basic auth account.

        These accounts are plain HTTP or FTP connections, with passwords.

        :param auth_type: The auth type has to be on of the following:

            - "HTTP"
            - "FTP"
        :type auth_type: BasicAuthType
        :param hostmask: Mask of the account host.
        :type hostmask: str
        :param username: User name for the account.
        :type username: str
        :param password: Password for the account.
        :type password: str
        :return: The ID of the newly created basic auth account.
        :rtype: int
        """

        params = [auth_type.value, hostmask, username, password]
        return self.action("/addBasicAuth", params)

    def disable_accounts(self, account_ids: list[int]) -> None:
        """Disable premium hoster accounts.

        :param account_ids: A list of account uuids.
        :type account_ids: List[int]
        :return: empty
        :rtype: None
        """

        params = [account_ids]
        self.action("/disableAccounts", params)

    def enable_accounts(self, account_ids: list[int]) -> None:
        """Enable premium hoster accounts.

        :param account_ids: A list of account uuids.
        :type account_ids: List[int]
        """

        params = [account_ids]
        self.action("/enableAccounts", params)

    def get_premium_hoster_url(self, hoster: str) -> str:
        """Get the url for a premium hoster.

        Note: The url will be a redirect over the jdownloader.org servers.

        :param hoster: The name of a hoster.
        :type hoster: str
        :return: The url for ``hoster``.
        :rtype: str
        """

        params = [hoster]
        return self.action("/getPremiumHosterUrl", params)

    def list_accounts(self, account_query: AccountQuery | None = None) -> list[Account]:
        """List premium hoster accounts.

        :param params: An AccountQuery object.
        :type: AccountQuery
        :return: A list of accounts
        :rtype: List[Account]
        """

        account_query = account_query or AccountQuery()
        params = [account_query.__json__()]
        resp = self.action("/listAccounts", params)
        return [Account(**acc) for acc in resp]

    def list_basic_auth(self) -> list[BasicAuth]:
        """List basic auth accounts.

        :return: A list of basic auth accounts.
        :rtype: list[BasicAuthentication]
        """

        resp = self.action("/listBasicAuth")
        return [BasicAuth(**auth) for auth in resp]

    def list_premium_hoster(self) -> list[str]:
        """List known premium hosters.

        :return: A list of all known premium hosters.
        :rtype: List[str]
        """

        return self.action("/listPremiumHoster")

    def list_premium_hoster_urls(self) -> dict[str, str]:
        """List known premium hosters with urls.

        :return: A map of all known premium hosters to urls.
        :rtype: Dict[str, str]
        """

        return self.action("/listPremiumHosterUrls")

    def refresh_accounts(self, account_ids: list[int]) -> None:
        """Let JDownloader refresh the account status for ``account_ids``.

        :param account_ids: A list of account ids
        :type account_ids: List[int]
        :return: empty
        :rtype: None
        """

        params = [account_ids]
        self.action("/refreshAccounts", params)

    def remove_accounts(self, account_ids: list[int]) -> None:
        """Remove the accounts for ``account_ids``.

        :param account_ids: A list of account ids
        :type account_ids: List[int]
        :return: empty
        :rtype: None
        """

        params = [account_ids]
        self.action("/removeAccounts", params)

    def remove_basic_auths(self, basic_auth_ids: list[int]) -> bool:
        """Remove basic auths for ``basic_auth_ids``.

        :param basic_auth_ids: A list of basic auth ids.
        :type account_ids: List[int]
        :return: Success.
        :rtype: bool
        """

        params = [basic_auth_ids]
        return self.action("/removeBasicAuths", params)

    def set_username_and_password(self, account_id: int, username: str, password: str) -> bool:
        """Set a new username and password for a premium hoster account.

        :param account_id: The ID of the account.
        :type account_id: int
        :param username: The new username.
        :type username: str
        :param password: The new password.
        :type password: str
        :return: Success
        :rtype: bool
        """

        params = [account_id, username, password]
        return self.action("/setUserNameAndPassword", params)

    def update_basic_auth(self, basic_authentication: BasicAuth) -> bool:
        """Update the credentials for a basic auth.

        .. note ::

            It is recommended to use the result of a ``list_basic_auth`` query
            for the input parameters. This way all necessary fields are filled
            and you can just update select parameters.

        :param basic_authentication: The new account parameters.
        :type basic_authentication: dict, BasicAuthentication
        :return: Success
        :rtype: bool
        """

        params = [basic_authentication.__json__()]
        return self.action("/updateBasicAuth", params)
