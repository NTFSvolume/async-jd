from pyjd.endpoints import Action
from pyjd.jd_types import LinkCheckResult


class Toolbar(Action, endpoint="toolbar"):
    def add_links_from_dom(self):
        """Unknown."""

        return self.action("/addLinksFromDOM")

    def check_links_from_dom(self):
        """Unknown."""

        return self.action("/checkLinksFromDOM")

    def get_status(self):
        """Get JDownloader status.

        Example result:

        .. code-block :: json

            {
                "running" : false,
                "reconnect" : false,
                "premium" : true,
                "download_complete" : 0,
                "stopafter" : false,
                "limit" : false,
                "limitspeed" : 0,
                "state" : "STOPPED_STATE",
                "download_current" : 0,
                "clipboard" : true,
                "speed" : 0,
                "pause" : false
            }

        """

        return self.action("/getStatus")

    def is_available(self):
        """Unknown."""

        return self.action("/isAvailable")

    def poll_checked_links_from_dom(self, check_id):
        """Unknown."""

        params = [check_id]
        resp = self.action("/pollCheckedLinksFromDOM", params)
        return LinkCheckResult(**resp)

    def special_url_handling(self, url: str):
        """Unknown."""

        params = [url]
        return self.action("/specialURLHandling", params)

    def start_downloads(self):
        """Start downloads."""

        return self.action("/startDownloads")

    def stop_downloads(self):
        """Stops the downloads."""

        return self.action("/stopDownloads")

    def toggle_automatic_reconnect(self):
        """Unknown."""

        return self.action("/toggleAutomaticReconnect")

    def toggle_clipboard_monitoring(self):
        """Unknown."""

        return self.action("/toggleClipboardMonitoring")

    def toggle_download_speed_limit(self):
        """Unknown."""

        return self.action("/toggleDownloadSpeedLimit")

    def toggle_pause_downloads(self):
        """Unknown."""

        return self.action("/togglePauseDownloads")

    def toggle_premium(self):
        """Unknown."""

        return self.action("/togglePremium")

    def toggle_stop_after_current_download(self):
        """Unknown."""

        return self.action("/toggleStopAfterCurrentDownload")

    def trigger_update(self):
        """Unknown."""

        return self.action("/triggerUpdate")
