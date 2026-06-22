import dataclasses
import json
from typing import Any

import requests

from .jd_device import JDDevice


@dataclasses.dataclass(slots=True)
class DirectConnector:
    base_url: str = "http://localhost:3128"
    headers: dict[str, str] | None = None

    def is_connected(self) -> bool:
        """Check if the JDownloader is reachable.

        This makes a dummy request to the JDownloader and returns True if it
        was successful

        :returns: Connection status
        :rtype: bool
        """
        try:
            requests.get(self.base_url + "/jd/version", headers=self.headers)
        except Exception:
            return False
        else:
            return True

    def get_device(self) -> JDDevice:
        return JDDevice(
            self,
            DirectConnectionHelper,
            {
                "id": "local",
                "name": "Local JDownloader",
                "type": "jd",
            },
        )


@dataclasses.dataclass(slots=True)
class DirectConnectionHelper:
    device: JDDevice

    def action(
        self,
        path: str,
        params: Any | None = None,
        http_action: str = "POST",
        *,
        binary: bool = False,
    ) -> Any:
        """Make the request to the JDownloader.

        :param path: The URL endpoint (excluding base_url) that is called.
        :type path: str
        :param params: Parameters for the request
        :type params: list, dict or str
        :param http_action: The HTTP method (unused)
        :type http_action: str
        :param binary: Return the response as byte array
        :type binary: bool
        :returns: The result of the request
        :rtype: byte_array, dict, string
        """
        assert http_action == "POST"
        rurl = f"{self.device.connector.base_url}{path}"

        param_list = []
        if params:
            for param in params:
                param_list.append(json.dumps(param))
        rparams = "?" + "&".join(param_list)

        if binary:
            return requests.get(rurl + rparams, headers=self.device.connector.headers).content

        rstr = requests.get(rurl + rparams, headers=self.device.connector.headers).content.decode()
        robj = json.loads(rstr)
        return robj.get("data", robj)
