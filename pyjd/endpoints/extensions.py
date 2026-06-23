from pyjd.endpoints import Action
from pyjd.jd_types import Extension
from pyjd.queries import ExtensionQuery


class Extensions(Action, endpoint="extensions"):
    def install(self, extension_id: str) -> bool:
        """Install the extension with extension_id.

        :param extension_id: The ID of the extension
        :type extension_id: str
        :return: Success
        :rtype: boolean
        """

        params = [extension_id]
        return self.action("/install", params)

    def is_enabled(self, extension_id: str) -> bool:
        """Check if the extension of extension_id is enabled.

        :param extension_id: ID of the extension
        :type extension_id: str
        :return: Is enabled
        :rtype: boolean
        """

        params = [extension_id]
        return self.action("/isEnabled", params)

    def is_installed(self, extension_id: str) -> bool:
        """Check if the extension of extension_id is installed.

        :param extension_id: ID of the extension
        :type extension_id: str
        :return: Is installed
        :rtype: boolean
        """

        params = [extension_id]
        return self.action("/isInstalled", params)

    def list_extensions(self, query: ExtensionQuery = ExtensionQuery.default()) -> list[Extension]:
        """List all extensions.

        :param query: A query to filter by (default: all)
        :type query: jd_types.ExtensionQuery
        :result: A list of extensions
        :rtype: List[jd_types.Extension]
        """

        params = [query.__json__()]
        resp = list(self.action("/list", params))
        return [Extension(**ext) for ext in resp]

    def set_enabled(self, extension_id: str, enabled: bool) -> bool:
        """Enable/Disable an extensions.

        :param extension_id: ID of the extension
        :type extension_id: str
        :param enabled: Enable or disable
        :type enabled: boolean
        :return: Success
        :rtype: boolean
        """

        params = [extension_id, enabled]
        return self.action("/setEnabled", params)
