import builtins
from typing import Any

from pyjd.endpoints import Action
from pyjd.jd_types import EnumOption
from pyjd.queries import AdvancedConfigAPIEntry, AdvancedConfigQuery, ListConfigQuery


class Config(Action, endpoint="config"):
    def get(self, interface_name: str, storage: str | None, key: str) -> Any:
        """Get value from interface by key.

        :param interface_name: The name of the JDownloader interface
        :type interface_name: str
        :param storage: The storage for the config entry.
            (None, for normal settings, or the extensions name for extension
            settings)
        :type storage: str
        :param key: The key of the config entry
        :type key: str
        :returns: The value of the config entry
        :rtype: Any
        """

        params = [interface_name, storage, key]
        return self.action("/get", params)

    def get_default(self, interface_name: str, storage: str, key: str) -> Any:
        """Get default value from interface by key.

        :param interface_name: The name of the JDownloader interface
        :type interface_name: str
        :param storage: The storage for the config entry.
            (None, for normal settings, or the extensions name for extension
            settings)
        :type storage: str
        :param key: The key of the config entry
        :type key: str
        :returns: The default value of the config entry
        :rtype: Any
        """

        params = [interface_name, storage, key]
        return self.action("/getDefault", params)

    def list(
        self,
        query: ListConfigQuery | None = None,
    ) -> list[AdvancedConfigAPIEntry]:
        """List all available config entries.

        :param pattern: A regex pattern to query by. If no pattern is given,
            all config items will be returned
        :type pattern: str
        :param returnDescription: If description should be returned
        :type returnDescription: boolean
        :param returnValues: If values should be returned
        :type returnValues: boolean
        :param returnDefaultValues: If default values should be returned
        :type returnDefaultValues: boolean
        :param returnEnumInfo: If enum info should be returned
        :type returnEnumInfo: boolean
        :return: A list of (matching) config items
        :rtype: List[AdvancedConfigAPIEntry]
        """

        query = query or ListConfigQuery()
        resp = self.action("/list", list(dict(query).values()))
        return [AdvancedConfigAPIEntry(**entry) for entry in resp]

    def list_enum(self, enum_type: str) -> builtins.list[EnumOption]:
        """List all possible enum values for the type.

        The enum_type is the AdvancedConfigAPIEntry.config_type for an Enum.
        (e.g.: 'org.jdownloader.settings.DelayWriteMode')

        :param enum_type: The enum type
        :type enum_type: str
        :returns: A list of possible options for the enum_type
        :rtype: List[EnumOption]
        """

        params = [enum_type]
        resp = self.action("/listEnum", params)
        return [EnumOption(**entry) for entry in resp]

    def query(
        self, advanced_config_query: AdvancedConfigQuery | None = None
    ) -> builtins.list[AdvancedConfigAPIEntry]:
        """Query config entries with an :class:`AdvancedConfigQuery`.

        :param advanced_config_query: The query options
        :type advanced_config_query: AdvancedConfigQuery
        :returns: A list of config entries
        :rtype: List[AdvancedConfigAPIEntry]
        """

        query = advanced_config_query or AdvancedConfigQuery()
        params = [query.__json__()]
        resp = self.action("/query", params=params)
        return [AdvancedConfigAPIEntry(**entry) for entry in resp]

    def reset(self, interface_name: str, storage: str, key: str) -> bool:
        """Reset a config entry.

        :param interface_name: The name of the JDownloader interface
        :type interface_name: str
        :param storage: The storage for the config entry.
            (None, for normal settings, or the extensions name for extension
            settings)
        :type storage: str
        :param key: The key of the config entry
        :type key: str
        :returns: Success
        :rtype: bool
        """

        params = [interface_name, storage, key]
        return self.action("/reset", params)

    def set(self, interface_name: str, storage: str, key: str, value: str) -> bool:
        """Set a config entry.

        :param interface_name: The name of the JDownloader interface
        :type interface_name: str
        :param storage: The storage for the config entry.
            (None, for normal settings, or the extensions name for extension
            settings)
        :type storage: str
        :param key: The key of the config entry
        :type key: str
        :param value: The new value for the config. Integers, booleans, etc.
            should be converted to strings.
        :type value: str
        :returns: Success
        :rtype: bool
        """

        params = [interface_name, storage, key, value]
        return self.action("/set", params)
