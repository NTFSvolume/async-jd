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
        return self.action("/getFavIcon", params, binary=True)

    def get_file_icon(self, filename: str) -> bytes:
        """Get the file icon.

        :param filename: The name of the icon
        :type filename: str
        :returns: The icon as png
        :rtype: bytes
        """

        params = [filename]
        return self.action("/getFileIcon", params, True)

    def get_icon(self, key: str, size: int) -> bytes:
        """Get an icon, scaled for size.

        :param filename: The name of the icon
        :type filename: str
        :param size: The size of the icon in px (it's a square)
        :type size: int
        :returns: The icon as png
        :rtype: bytes
        """

        params = [key, size]
        return self.action("/getIcon", params, True)

    def get_icon_description(self, key: str) -> IconDescriptor:
        """Get an icon description.

        :param key: The icon key
        :type key: str
        :returns: Description for the key
        :rtype: str
        """

        params = [key]
        resp = self.action("/getIconDescription", params)
        return IconDescriptor(**resp)
