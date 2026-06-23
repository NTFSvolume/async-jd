from __future__ import annotations

from typing import Self, final

from pyjd.direct import DirectConnection
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
from pyjd.myjd.api import MyJDAPI
from pyjd.myjd.connection import MyJDConnection


@final
class JDDeviceClient:
    """A class that represents a JDownloader device and its functions."""

    def __init__(self, connection: DirectConnection | MyJDConnection) -> None:
        self.connection = connection
        self.accounts = Accounts(connection)
        self.captcha = Captcha(connection)
        self.config = Config(connection)
        self.content = Content(connection)
        self.dialogs = Dialogs(connection)
        self.device = Device(connection)
        self.downloads = Downloads(connection)
        self.events = Events(connection)
        self.extensions = Extensions(connection)
        self.linkgrabber = LinkGrabber(connection)
        self.log = Log(connection)
        self.plugins = Plugins(connection)
        self.polling = Polling(connection)
        self.system = System(connection)
        self.toolbar = Toolbar(connection)
        self.ui = UI(connection)
        self.update = Update(connection)

    @classmethod
    def direct_connect(
        cls,
        base_url: str = "http://localhost:3128",
        headers: dict[str, str] | None = None,
    ) -> Self:
        return cls(DirectConnection(base_url, headers))

    @classmethod
    def myjd_connect(
        cls,
        email: str,
        password: str,
        device_id: str | None,
        device_name: str | None,
    ) -> Self:
        api = MyJDAPI()
        api.connect(email, password)
        device = api.get_device(device_id, device_name)
        return cls(MyJDConnection(api, device))
