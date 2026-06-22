from pyjd.endpoints import Action
from pyjd.jd_types import DirectConnectionInfos


class Device(Action, endpoint="device"):
    def get_direct_connection_infos(self) -> DirectConnectionInfos | None:
        if resp := self.action("/getDirectConnectionInfos"):
            return DirectConnectionInfos(**resp)

        return None

    def get_session_public_key(self) -> str:
        return self.action("/getSessionPublicKey")

    def ping(self) -> bool:
        return self.action("/ping")
