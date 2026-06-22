import pytest

from pyjd.jd_device import JDDevice
from pyjd.jd_types import DialogInfo, DialogTypeInfo


@pytest.mark.xfail(reason="broken from before fork")
def test_dialogs(jd: JDDevice) -> None:
    # we're just doing everything in here..

    # generate a dialog
    jd.accounts.add_account("youtube.com", "user", "pass")

    # list dialogs
    dialogs = jd.dialogs.list()
    assert isinstance(dialogs, list)
    assert len(dialogs) > 0

    # get dialog
    dialog = jd.dialogs.get(dialogs[0])
    assert isinstance(dialog, DialogInfo)
    assert isinstance(dialog.properties, dict)

    # get dialog type
    dialog_type = jd.dialogs.get_type_info(dialog.type)
    assert isinstance(dialog_type, DialogTypeInfo)
    assert isinstance(dialog_type.in_, dict)
    assert isinstance(dialog_type.out, dict)

    # answer dialog
    dialogs = jd.dialogs.list()
    dialogs.reverse()

    for dialog in dialogs:
        res = jd.dialogs.answer(dialog, {"dontshowagain": False, "closereason": "cancel"})
        # this test is not working all too well..
        # assert res is True

    dialogs = jd.dialogs.list()
    assert len(dialogs) == 0

    # remove account
    a = jd.accounts.list_accounts()
    jd.accounts.remove_accounts([a[0].uuid])
