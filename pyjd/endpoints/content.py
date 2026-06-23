from __future__ import annotations

from pyjd.endpoints import Action
from pyjd.jd_types import IconDescriptor


class Content(Action, endpoint="contentV2"):
    def get_fav_icon(self, hostername: str) -> bytes:
        """Get the fav icon for a hoster.

        :param hostername: Name of the hoster for which the favicon will be
            returned
        :type hostername: str
        :returns: The favicon as png
        :rtype: bytes
        """

        params = [hostername]
        return self.request_bytes("/getFavIcon", params)

    def get_file_icon(self, filename: str) -> bytes:
        params = [filename]
        return self.request_bytes("/getFileIcon", params)

    def get_icon(self, key: str, size: int) -> bytes:
        """Get an icon, scaled for size."""

        params = [key, size]
        return self.request_bytes("/getIcon", params)

    def get_icon_description(self, key: str) -> IconDescriptor:
        params = [key]
        resp = self.action("/getIconDescription", params)
        return IconDescriptor(**resp)
