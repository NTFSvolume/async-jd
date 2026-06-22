from typing import Any, TypedDict, final

from pyjd.endpoints.accounts import Accounts
from pyjd.endpoints.captcha import Captcha
from pyjd.endpoints.config import Config
from pyjd.endpoints.content import Content
from pyjd.endpoints.device import Device
from pyjd.endpoints.dialogs import Dialogs
from pyjd.endpoints.downloads import Downloads
from pyjd.endpoints.events import Events
from pyjd.endpoints.extensions import Extensions
from pyjd.endpoints.linkgrabber import LinkGrabber
from pyjd.endpoints.log import Log
from pyjd.endpoints.plugins import Plugins
from pyjd.endpoints.polling import Polling
from pyjd.endpoints.system import System
from pyjd.endpoints.toolbar import Toolbar
from pyjd.endpoints.ui import UI
from pyjd.endpoints.update import Update
from pyjd.myjd_connection_helper import MyJDConnectionHelper


class DeviceDict(TypedDict, total=True):
    name: str
    id: str
    type: str


@final
class JDDevice:
    """A class that represents a JDownloader device and its functions."""

    def __init__(
        self,
        connector: Any,
        connection_helper: type,
        device_dict: DeviceDict,
        refresh_direct_connections: bool = True,
    ):
        """Initializes the device instance.

        :param connector: The connector object (direct or MyJD)
        :type connector: Any
        :param device_dict: Dictionary with device properties
        :type device_dict: dict
        :returns: A JDDevice object
        :rtype: JDDevice
        """

        self.name = device_dict["name"]
        self.device_id = device_dict["id"]
        self.device_type = device_dict["type"]

        self.connector = connector
        self.connection_helper = conn = _connect(
            self, connection_helper, refresh_direct_connections=refresh_direct_connections
        )

        self.accounts = Accounts(conn)
        self.captcha = Captcha(conn)
        self.config = Config(conn)
        self.content = Content(conn)
        self.dialogs = Dialogs(conn)
        self.device = Device(conn)
        self.downloads = Downloads(conn)
        self.events = Events(conn)
        self.extensions = Extensions(conn)
        self.linkgrabber = LinkGrabber(conn)
        self.log = Log(conn)
        self.plugins = Plugins(conn)
        self.polling = Polling(conn)
        self.system = System(conn)
        self.toolbar = Toolbar(conn)
        self.ui = UI(conn)
        self.update = Update(conn)


def _connect(
    self: JDDevice,
    connection_helper: type,
    *,
    refresh_direct_connections: bool,
) -> MyJDConnectionHelper:
    if connection_helper is MyJDConnectionHelper:
        return connection_helper(self, refresh_direct_connections=refresh_direct_connections)
    return connection_helper(self)
