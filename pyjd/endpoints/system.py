from pyjd.endpoints import Action


class System(Action, endpoint="system"):
    def exit_jd(self) -> str:
        """Stop the JDownloader."""

        return self.action("/exitJD")

    def get_storage_infos(self, path: str | None = None) -> dict:
        """Get storage information."""

        params = [path]
        return self.action("/getStorageInfos", params)

    def get_system_infos(self) -> dict:
        """Get system information."""

        return self.action("/getSystemInfos")

    def hibernate_os(self) -> str:
        """Hibernate the OS."""

        return self.action("/hibernateOS")

    def restart_jd(self) -> str:
        """Restart the JDownloader."""

        return self.action("/restartJD")

    def shutdown_os(self, force: bool = False) -> str:
        """Shutdown the OS."""

        params = [force]
        return self.action("/shutdownOS", params)

    def standby_os(self) -> str:
        """Put the OS in standby."""

        return self.action("/standbyOS")
