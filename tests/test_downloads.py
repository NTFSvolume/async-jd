from pyjd.jd_device import JDDeviceClient


def test_cleanup(jd: JDDeviceClient) -> None:
    assert jd.downloads.cleanup() is True


def test_force_download(jd: JDDeviceClient) -> None:
    jd.downloads.force_download()


def test_get_download_urls(jd: JDDeviceClient) -> None:
    # jd.downloads.get_download_urls()
    pass


def test_get_stop_mark(jd: JDDeviceClient) -> None:
    jd.downloads.get_stop_mark()


def test_get_stop_marked_link(jd: JDDeviceClient) -> None:
    jd.downloads.get_stop_marked_link()


def test_get_structure_change_counter(jd: JDDeviceClient) -> None:
    jd.downloads.get_structure_change_counter()


def test_move_links(jd: JDDeviceClient) -> None:
    jd.downloads.move_links()


def test_move_packages(jd: JDDeviceClient) -> None:
    jd.downloads.move_packages()


def test_move_to_new_package(jd: JDDeviceClient) -> None:
    jd.downloads.move_to_new_package()


def test_package_count(jd: JDDeviceClient) -> None:
    jd.downloads.package_count()


def test_query_links(jd: JDDeviceClient) -> None:
    jd.downloads.query_links()


def test_query_packages(jd: JDDeviceClient) -> None:
    jd.downloads.query_packages()


def test_remove_links(jd: JDDeviceClient) -> None:
    jd.downloads.remove_links()


def test_remove_stop_mark(jd: JDDeviceClient) -> None:
    jd.downloads.remove_stop_mark()


def test_rename_link(jd: JDDeviceClient) -> None:
    jd.downloads.rename_link()


def test_rename_package(jd: JDDeviceClient) -> None:
    jd.downloads.rename_package()


def test_reset_links(jd: JDDeviceClient) -> None:
    jd.downloads.reset_links()


def test_resume_links(jd: JDDeviceClient) -> None:
    jd.downloads.resume_links()


def test_set_download_directory(jd: JDDeviceClient) -> None:
    jd.downloads.set_download_directory()


def test_set_download_password(jd: JDDeviceClient) -> None:
    jd.downloads.set_download_password()


def test_set_enabled(jd: JDDeviceClient) -> None:
    jd.downloads.set_enabled()


def test_set_priority(jd: JDDeviceClient) -> None:
    jd.downloads.set_priority()


def test_set_stop_mark(jd: JDDeviceClient) -> None:
    jd.downloads.set_stop_mark()


def test_split_package_by_hoster(jd: JDDeviceClient) -> None:
    jd.downloads.split_package_by_hoster()


def test_start_online_status_check(jd: JDDeviceClient) -> None:
    jd.downloads.start_online_status_check()


def test_unskip(jd: JDDeviceClient) -> None:
    jd.downloads.unskip()
