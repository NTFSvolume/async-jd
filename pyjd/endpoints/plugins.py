from pyjd.endpoints import Action
from pyjd.jd_types import (
    AdvancedConfigAPIEntry,
    AdvancedConfigQuery,
    Plugin,
    PluginsQuery,
)


class Plugins(Action, endpoint="plugins"):
    def get(self, interface_name, display_name, key):
        """Get a plugin."""

        params = [interface_name, display_name, key]
        return self.action("/get", params)

    def get_all_plugin_regex(self):
        """Get all plugin regular expressions."""

        return self.action("/getAllPluginRegex")

    def get_plugin_regex(self, url):
        """Get plugin regular expressions for a url."""

        params = [url]
        return self.action("/getPluginRegex", params)

    def list(self, plugins_query=PluginsQuery.default()):
        """List plugins with query."""

        params = [plugins_query.dict()]
        resp = self.action("/list", params)
        return [Plugin(**p) for p in resp]

    def query(self, config_query=AdvancedConfigQuery.default()):
        """Query plugin configurations."""

        params = [config_query.dict()]
        resp = self.action("/query", params)

        return [AdvancedConfigAPIEntry(**c) for c in resp]

    def reset(self, interface_name: str, display_name: str, key: str):
        """Reset plugin config."""

        params = [interface_name, display_name, key]
        return self.action("/reset", params)

    def set(self, interface_name, display_name, key, new_value):
        """Set a plugin config value."""

        params = [interface_name, display_name, key, new_value]
        return self.action("/set", params)
