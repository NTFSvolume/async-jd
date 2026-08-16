from cyclopts import App
from dotenv import dotenv_values

from pyjd.client import JDDeviceClient

app = App()


@app.command()
def connect() -> None:
    creds = dotenv_values()
    app.console.log(email := creds["EMAIL"] or "")
    device = JDDeviceClient.myjd_connect(
        email=email,
        password=creds["PASSWORD"] or "",
        device_id=creds["DEVICE_ID"],
    )
    app.console.log(device)
    if device:
        pass
