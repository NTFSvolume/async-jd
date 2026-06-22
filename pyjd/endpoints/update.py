from pyjd.endpoints import Action


class Update(Action, endpoint="update"):
    def is_update_available(self) -> str:
        """Returns if an update is available."""

        return self.action("/isUpdateAvailable")

    def restart_and_update(self) -> str:
        """Restarts and update."""

        return self.action("/restartAndUpdate")

    def run_update_check(self) -> str:
        """Runs an update check."""

        return self.action("/runUpdateCheck")
