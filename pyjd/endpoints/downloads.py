from typing import Any

from pyjd.endpoints import Action
from pyjd.jd_types import (
    DeleteAction,
    DownloadLink,
    FilePackage,
    Mode,
    Priority,
    Reason,
    SelectionType,
)
from pyjd.queries import LinkQuery, PackageQuery


class Downloads(Action, endpoint="downloadsV2"):
    def cleanup(
        self,
        link_ids: list[int] = [],
        package_ids: list[int] = [],
        delete_action: DeleteAction = DeleteAction.DELETE_DISABLED,
        mode: Mode = Mode.REMOVE_LINKS_ONLY,
        selection_type: SelectionType = SelectionType.ALL,
    ) -> bool:
        """Cleanup the link_ids & package_ids in the download list.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: Package IDs that are used
        :type package_ids: List[int]
        :param action: The class:`jd_types.DeleteAction` that will be performed
        :type action: DeleteAction
        :param mode: The class:`jd_types.Mode` that is used
        :type mode: Mode
        :type selection_type: The class:`jd_types.SelectionType` that is
            applied
        :type selection_type: SelectionType
        :returns: resp
        :rtype: Any
        """

        params = [
            link_ids,
            package_ids,
            delete_action.value,
            mode.value,
            selection_type.value,
        ]
        resp = self.action("/cleanup", params)
        return resp == ""

    def force_download(
        self,
        link_ids: list[int] = [],
        package_ids: list[int] = [],
    ) -> bool:
        """Force downloads for link_ids and package_ids.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: Package IDs that are used
        :type package_ids: List[int]
        :returns: Success
        :rtype: bool
        """

        params = [link_ids, package_ids]
        return self.action("/forceDownload", params)

    def get_download_urls(
        self,
        link_ids: list[int] = [],
        package_ids: list[int] = [],
        url_display_type: list[str] = ["ORIGIN"],
    ) -> dict[str, list[int]]:
        """Get the download urls for link_ids and package_ids.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: Package IDs that are used
        :type package_ids: List[int]
        :param url_display_type: The type of urls that should be returned.
            Example: ['ORIGIN']
        :type url_display_type: List[str]
        :returns: The download urls with their associated packages
        :rtype: Dict[str, List[int]]
        """

        params = [link_ids, package_ids, url_display_type]
        return self.action("/getDownloadUrls", params)

    def get_stop_mark(self) -> int:
        """Get the link id for where the stop mark is at.

        If no stop mark is set, the result it -1

        :returns: Link id for stop mark, or -1
        :rtype: int
        """

        return self.action("/getStopMark")

    def get_stop_marked_link(self) -> DownloadLink | None:
        """Get the :class:`DownloadLink` object for the stopmark.

        :returns: Download link for stop mark, or None
        :rtype: DownloadLink
        """

        resp = self.action("/getStopMarkedLink")

        if resp:
            return DownloadLink(**resp)

        return None

    def get_structure_change_counter(self, old_counter_value: int = 0) -> int:
        """Get the structure change counter.

        Update the application layout, if the structure_change_counter is
        higher than the last.

        :returns: Structure change counter, or -1 if there is no newer change.
        :rtype: int
        """

        params = [old_counter_value]
        return self.action("/getStructureChangeCounter", params)

    def move_links(
        self,
        link_ids: list[int] = [],
        after_link_id: int = -1,
        dest_package_id: int = -1,
    ) -> Any:
        """Move links to a package.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param after_link_id: ?
        :type after_link_id: int
        :param dest_package_id: The ID of the destination package
        :type dest_package_id: int
        :returns: resp
        :rtype: Any
        """

        params = [link_ids, after_link_id, dest_package_id]
        return self.action("/moveLinks", params)

    def move_packages(self, package_ids: list[int] = [], after_dest_package_id: int = -1) -> Any:
        """Move packages.

        :param package_ids: Package IDs that are used
        :type package_ids: List[int]
        :param after_dest_package_id: ?
        :type after_dest_package_id: int
        :returns: resp
        :rtype: Any
        """

        params = [package_ids, after_dest_package_id]
        return self.action("/movePackages", params)

    def move_to_new_package(
        self,
        link_ids: list[int] = [],
        pkg_ids: list[int] = [],
        new_pkg_name: str = "",
        download_path: str = "",
    ) -> Any:
        """Move link_ids and pkg_ids to a new package

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: Package IDs that are used
        :type package_ids: List[int]
        :param new_pkg_name: Name of the new package
        :type new_pkg_name: str
        :param download_path: Download path for the new package
        :type download_path: str
        :returns: resp
        :rtype: Any
        """

        params = [link_ids, pkg_ids, new_pkg_name, download_path]
        return self.action("/movetoNewPackage", params)

    def package_count(self) -> int:
        """Get the number of packages in the download list.

        :returns: Number of packages in download list
        :rtype: int
        """

        return self.action("/packageCount")

    def query_links(self, query_params: LinkQuery | None = None) -> list[DownloadLink]:
        """Query the links in the download list.

        :param query_params: The parameters for the query
        :type query_params: LinkQuery
        :returns: A list of download link objects
        :rtype: List[DownloadLink]
        """

        query_params = query_params or LinkQuery.default()
        params = [query_params.__json__()]
        resp = self.action("/queryLinks", params)
        return [DownloadLink(**link) for link in resp]

    def query_packages(self, query_params: PackageQuery | None = None) -> list[FilePackage]:
        """Query the packages in the download list.

        :param query_params: The parameters for the query
        :type query_params: PackageQuery
        :returns: A list of file packages objects
        :rtype: List[FilePackage]
        """
        query_params = query_params or PackageQuery.default()
        params = [query_params.__json__()]
        resp = self.action("/queryPackages", params)
        return [FilePackage(**package) for package in resp]

    def remove_links(self, link_ids: list[int] = [], package_ids: list[int] = []) -> None:
        """Remove links/packages from download list.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: Package IDs that are used
        :type package_ids: List[int]
        """

        params = [link_ids, package_ids]
        self.action("/removeLinks", params)

    def remove_stop_mark(self) -> None:
        """Remove the stop mark."""
        self.action("/removeStopMark")

    def rename_link(self, link: int = -1, new_name: str = "") -> None:
        """Rename a link.

        :param link: The ID of the link
        :type link: int
        :param new_name: The new name for the link
        :type new_name: str
        """

        params = [link, new_name]
        self.action("/renameLink", params)

    def rename_package(self, package_id: str = "", new_name: str = "") -> None:
        """Rename a package.

        :param package_id: ID of the packages
        :type package_id: int
        :param new_name: New name for the package
        :type new_name: str
        """

        params = [package_id, new_name]
        return self.action("/renamePackage", params)

    def reset_links(self, link_ids: list[int] = [], package_ids: list[int] = []) -> None:
        """Reset links/packages in the download list.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: Package IDs that are used
        :type package_ids: List[int]
        """

        params = [link_ids, package_ids]
        self.action("/resetLinks", params)

    def resume_links(self, link_ids: list[int] = [], package_ids: list[int] = []) -> None:
        """Resume links/packages.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: Package IDs that are used
        :type package_ids: List[int]
        """

        params = [link_ids, package_ids]
        self.action("/resumeLinks", params)

    def set_download_directory(self, directory: str = "", package_ids: list[int] = []) -> None:
        """Set the download directory for a packages.

        :param directory: Path of the download directory
        :type directory: str
        :param package_ids: List of package IDs that are changed.
        :type package_ids: List[int]
        """

        params = [directory, package_ids]
        return self.action("/setDownloadDirectory", params)

    def set_download_password(
        self,
        link_ids: list[int] = [],
        package_ids: list[int] = [],
        password: str = "",
    ) -> bool:
        """Set the download password for links/packages.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: List of package IDs that are changed.
        :type package_ids: List[int]
        :param password: The download password
        :type password: str
        :returns: Success
        :rtype: bool
        """

        params = [link_ids, package_ids, password]
        return self.action("/setDownloadPassword", params)

    def set_enabled(
        self,
        enabled: bool = True,
        link_ids: list[int] = [],
        package_ids: list[int] = [],
    ) -> bool:
        """Enable/disable links and packages.

        :param enabled: Enable on or off
        :type enabled: bool
        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: List of package IDs that are changed.
        :type package_ids: List[int]
        """

        params = [enabled, link_ids, package_ids]
        return self.action("/setEnabled", params)

    def set_priority(
        self,
        priority: Priority = Priority.DEFAULT,
        link_ids: list[int] = [],
        package_ids: list[int] = [],
    ) -> None:
        """Set the priority for links and packages.

        :param priority: The priority for the links/packages.
        :type priority: Priority
        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: List of package IDs that are changed.
        :type package_ids: List[int]
        """

        params = [priority.value, link_ids, package_ids]
        self.action("/setPriority", params)

    def set_stop_mark(self, link_id: int | None = None, package_id: int | None = None) -> None:
        """Set the stop mark to the specified id.

        Only one of link_id and package_id has to be given.

        :param link_id: A link id for the stop mark
        :type link_id: int
        :param package_id: A package id for the stop mark
        :type package_id: int
        """

        params = [link_id, package_id]
        self.action("/setStopMark", params)

    def split_package_by_hoster(
        self, link_ids: list[int] = [], package_ids: list[int] = []
    ) -> None:
        """Split the packages/links by hoster.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: List of package IDs that are changed.
        :type package_ids: List[int]
        """

        params = [link_ids, package_ids]
        self.action("/splitPackageByHoster", params)

    def start_online_status_check(
        self, link_ids: list[int] = [], package_ids: list[int] = []
    ) -> None:
        """Start an online status check for links and packages.

        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param package_ids: List of package IDs that are changed.
        :type package_ids: List[int]
        """

        params = [link_ids, package_ids]
        self.action("/startOnlineStatusCheck", params)

    def unskip(
        self,
        link_ids: list[int] = [],
        package_ids: list[int] = [],
        filter_by_reason: Reason = Reason.DISK_FULL,
    ) -> bool:
        """Un-skip links and packages

        :param package_ids: List of package IDs that are changed.
        :type package_ids: List[int]
        :param link_ids: Link IDs that are used
        :type link_ids: List[int]
        :param filter_by_reason: Filter for the reason why they were skipped.
        :type filter_by_reason: Reason
        :returns: Success
        :rtype: bool
        """

        # package_ids and link_ids are switch for whatever reason...
        params = [package_ids, link_ids, filter_by_reason.value]
        return self.action("/unskip", params)
