from typing import Any

from pyjd.endpoints import Action
from pyjd.jd_types import (
    CrawledLink,
    CrawledPackage,
    DeleteAction,
    JobLinkCrawler,
    LinkCollectingJob,
    LinkVariant,
)
from pyjd.queries import AddLinksQuery, CrawledLinkQuery, CrawledPackageQuery, LinkCrawlerJobsQuery


class LinkGrabber(Action, endpoint="linkgrabberv2"):
    def abort(self, job_id: int = -1) -> bool:
        """Abort one or all jobs.

        :param job_id: If this is given, only the job `job_id` will be aborted.
        :type job_id: int
        :return: Success
        :rtype: bool
        """

        params = [job_id] if job_id > -1 else None
        return self.action("/abort", params)

    def add_container(self, container_type: str, content: str) -> LinkCollectingJob:
        """Add a container of type and content.

        :param container_type: The type of the container
        :type container_type: str
        :param content: The content of the container
        :type content: str
        :return: A link collecting job
        :rtype: LinkCollectingJob
        """

        params = [container_type, content]
        resp = self.action("/addContainer", params)
        return LinkCollectingJob(**resp)

    def add_links(self, add_links_query: AddLinksQuery) -> LinkCollectingJob:
        """
        Add links to the linkcollector

        :param add_links_query: An AddLinksQuery object
        :type params: AddLinksQuery
        :return: A link collecting job
        :rtype: LinkCollectingJob
        """

        params = [add_links_query.__json__()]
        resp = self.action("/addLinks", params)
        return LinkCollectingJob(**resp)

    def add_variant_copy(
        self,
        link_id: int,
        destination_after_link_id: int,
        destination_package_id: int,
        variant_id: int,
    ) -> Any:
        """Unkown."""

        params = [
            link_id,
            destination_after_link_id,
            destination_package_id,
            variant_id,
        ]
        return self.action("/addVariantCopy", params)

    def cleanup(
        self,
        delete_action: DeleteAction,
        mode,
        selection_type,
        link_ids=[],
        package_ids=[],
    ):
        """Clean packages and/or links of the linkgrabber list.

        Requires at least a ``package_ids`` or ``link_ids`` list, or both.

        :param package_ids: Package UUIDs.
        :type package_ids: List[int]
        :param link_ids: Link UUIDs.
        :type link_ids: List[int]
        :param action: DeleteAction to be done on cleanup.
        :type action: jd_types.DeleteAction
        :param mode: Mode to use.
        :type mode: jd_types.Mode
        :param selection_type: Type of selection to use.
        :type selection_type: jd_types.SelectionType
        """

        params = [link_ids, package_ids]
        params += [delete_action.value, mode.value, selection_type.value]
        return self.action("/cleanup", params)

    def clear_list(self):
        """Clears Linkgrabbers list."""

        return self.action("/clearList")

    def get_children_changed(self, structure_watermark):
        """Unkown."""

        params = [structure_watermark]
        return self.action("/getChildrenChanged", params)

    def get_download_folder_history_selection_base(self):
        """Returns the download folder selection.

        :return: List of strings with paths to available download folders.
        :rtype: List[str]
        """

        return self.action("/getDownloadFolderHistorySelectionBase")

    def get_download_urls(
        self,
        link_ids: list[int],
        package_ids: list[int],
        url_display_types: list[str] = ["ORIGIN"],
    ):
        """Gets download urls from Linkgrabber.

        :param package_ids: Package UUIDs.
        :type package_ids: List[int]
        :param link_ids: link UUIDs.
        :type link_ids: List[int]
        :param url_display_types: No clue. Not documented
        :type url_display_types: List
        """

        params = [link_ids, package_ids, url_display_types]
        return self.action("/getDownloadUrls", params)

    def get_package_count(self):
        """Get package count in linkgrabber"""

        return self.action("/getPackageCount")

    def get_variants(self, link_id: str):
        """Gets the variants of a url/download (not package)

        For example a youtube link gives you a package with three downloads,
        the audio, the video and a picture, and each of those downloads have
        different variants (audio quality, video quality, and picture quality).

        :param params: The UUID of the download you want the variants.
        :type params: List[int]
        :rtype: Variants in a list with dictionaries like this one:

            .. code-block :: json

                [
                    {
                        "id": "M4A_256",
                        "name": "256kbit/s M4A-Audio"
                    },
                    {
                        "id": "AAC_256",
                        "name": "256kbit/s AAC-Audio"
                    }
                ]

        """

        params = [link_id]
        resp = self.action("/getVariants", params)
        return [LinkVariant(variant) for variant in resp]

    def is_collecting(self):
        """Bool status query about the collecting process"""

        return self.action("/isCollecting")

    def move_links(self, link_ids, after_link_id, dest_package_id):
        """Unkown."""

        params = [link_ids, after_link_id, dest_package_id]
        return self.action("/moveLinks", params)

    def move_packages(self, package_ids, after_dest_package_id):
        """Unkown."""

        params = [package_ids, after_dest_package_id]
        return self.action("/movePackages", params)

    def move_to_downloadlist(self, link_ids, package_ids):
        """Moves packages and/or links to download list.

        :param link_ids: Link UUIDs.
        :type link_ids: List[int]
        :param package_ids: Package UUIDs.
        :type package_ids: List[int]
        """

        params = [link_ids, package_ids]
        return self.action("/moveToDownloadlist", params)

    def move_to_new_package(self, link_ids, package_ids, new_pkg_name, download_path):
        """Moves packages and/or links to a new package

        :param link_ids: Link UUIDs.
        :type link_ids: List[int]
        :param package_ids: Package UUIDs.
        :type package_ids: List[int]
        :param new_pkg_name: The name of the new package
        :type new_pkg_name: str
        :param download_path: Download path for the new package
        :type download_path: str
        """

        params = [link_ids, package_ids, new_pkg_name, download_path]
        return self.action("/movetoNewPackage", params)

    def query_link_crawler_jobs(self, link_crawler_jobs_query=LinkCrawlerJobsQuery.default()):
        """Query link crawler jobs.

        :param crawled_link_query: Query to filter by
        :type crawled_link_query: jd_types.LinkCrawlerJobsQuery
        :return: List of crawled packages
        :rtype: List[jd_types.JobLinkCrawler]
        """

        params = [link_crawler_jobs_query.__json__()]
        resp = self.action("/queryLinkCrawlerJobs", params)

        return [JobLinkCrawler(**job) for job in resp]

    def query_links(self, crawled_link_query=CrawledLinkQuery.default()):
        """Get the links in the linkcollector/linkgrabber

        :param params: A CrawledLinkQuery object with options.
        :type params: CrawledLinkQuery
        :return: List of CrawledLink objects
        :rtype: List[CrawledLink]

        """

        params = [crawled_link_query.__json__()]
        resp = self.action("/queryLinks", params)

        return [CrawledLink(**link) for link in resp]

    def query_packages(self, crawled_package_query=CrawledPackageQuery.default()):
        """Get the crawled packages in the linkgrabber

        :param params: A dictionary of parameters to pass.
        :type params: jd_types.CrawledPackageQuery
        :return: A list of crawled packages:
        """

        params = [crawled_package_query.__json__()]
        resp = self.action("/queryPackages", params)

        return [CrawledPackage(**package) for package in resp]

    def remove_links(self, link_ids, package_ids):
        """Unknown."""

        params = [link_ids, package_ids]
        return self.action("/removeLinks", params)

    def rename_link(self, link_id, new_name):
        """Unknown."""

        params = [link_id, new_name]
        return self.action("/renameLink", params)

    def rename_package(self, package_id, new_name):
        """Unknown."""

        params = [package_id, new_name]
        return self.action("/renamePackage", params)

    def set_download_directory(self, directory, package_ids):
        """Unknown."""

        params = [directory, package_ids]
        return self.action("/setDownloadDirectory", params)

    def set_download_password(self, link_ids, package_ids, password):
        """Unknown."""

        params = [link_ids, package_ids, password]
        return self.action("/setDownloadPassword", params)

    def set_enabled(self, enabled, link_ids, package_ids):
        """Sets the UUIDs as enabled

        :param enabled: Enable or disable the IDs
        :type enabled: bool
        :param link_ids: List of link UUIDs
        :type link_ids: List[int]
        :param package_ids: List of package UUIDs
        :type package_ids: List[int]
        """

        params = [enabled, link_ids, package_ids]
        return self.action("/setEnabled", params=params)

    def set_priority(self, priority, link_ids, package_ids):
        """Sets the priority of links or packages.

        :param package_ids: Package UUIDs.
        :type package_ids: List[int]
        :param link_ids: link UUIDs.
        :type link_ids: List[int]
        :param priority: Priority to set.
            Priorities: HIGHEST, HIGHER, HIGH, DEFAULT, LOWER
        :type priority: str
        """

        params = [priority, link_ids, package_ids]
        return self.action("/setPriority", params)

    def set_variant(self, link_id, variant_id):
        """Unknown."""

        params = [link_id, variant_id]
        return self.action("/setVariant", params)

    def split_package_by_hoster(self, link_ids, pkg_ids):
        """Unknown."""

        params = [link_ids, pkg_ids]
        return self.action("/splitPackageByHoster", params)

    def start_online_check(self, link_ids, package_ids):
        """Unknown."""

        params = [link_ids, package_ids]
        return self.action("/startOnlineStatusCheck", params)

    def help(self):
        """Returns the API help."""

        return self.action("/linkgrabberv2/help", http_action="GET")
