from pyjd.endpoints import Action
from pyjd.jd_types import LogFolder


class Log(Action, endpoint="log"):
    def get_available_logs(self) -> list[LogFolder]:
        """Returns a list of available logs.

        :return: List of log folders
        :rtype: jd_types.LogFolder
        """

        resp = self.action("/getAvailableLogs")
        return [LogFolder(**folder) for folder in resp]

    def send_log_file(self, log_folders) -> str:
        """Returns a log file.

        :return: The log file
        :rtype: str
        """

        params = [log_folders]
        return self.action("/sendLogFile", params)
