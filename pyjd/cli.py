import dataclasses
import logging
from typing import Annotated

from cyclopts import App, Parameter
from dotenv import dotenv_values
from rich.logging import RichHandler
from rich.traceback import install

from pyjd.client import JDDeviceClient
from pyjd.jd_types import LinkCollectingJob
from pyjd.queries import AddLinksQuery

app = App()

install()
logger = logging.getLogger("pyjd")
logger.addHandler(RichHandler(level=logging.DEBUG, rich_tracebacks=True))
logger.setLevel(logging.DEBUG)


@app.command()
def connect() -> JDDeviceClient:
    creds = dotenv_values()
    app.console.log(email := creds["EMAIL"] or "")
    device = JDDeviceClient.myjd_connect(
        email=email,
        password=creds["PASSWORD"] or "",
        device_id=creds.get("DEVICE_ID"),
        device_name=creds.get("DEVICE_NAME"),
    )
    app.console.log(device)
    return device


@app.command()
def add_links(
    link: str, *, query: Annotated[AddLinksQuery | None, Parameter(name="*")] = None
) -> LinkCollectingJob:
    device = connect()
    query = dataclasses.replace(query, links=link) if query else AddLinksQuery(links=link)

    job = device.linkgrabber.add_links(query)
    app.console.log(job)
    return job
