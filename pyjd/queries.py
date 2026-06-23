# ruff: noqa: N815

from __future__ import annotations

import dataclasses
from typing import Any

from pyjd.common import DictDataClass
from pyjd.jd_types import AbstractType, Priority


@dataclasses.dataclass(slots=True, frozen=True)
class AccountQuery(DictDataClass):
    """Query for premium host accounts.

    The fields are booleans, that can be turned on or off, if you want to have
    query for the information or not.
    By default all possible data is queried.
    """

    enabled: bool = True
    error: bool = True
    maxResults: int = -1
    startAt: int = 0
    trafficLeft: bool = True
    trafficMax: bool = True
    userName: bool = True
    uuidlist: list[int] | None = None
    valid: bool = True
    validUntil: bool = True

    def __repr__(self) -> str:
        return f"<AccountQuery ({self.uuidlist})>"


@dataclasses.dataclass(slots=True, frozen=True)
class AdvancedConfigAPIEntry(DictDataClass):
    abstractType: AbstractType | None = None
    defaultValue: Any | None = None
    docs: str | None = None
    enumLabel: str | None = None
    enumOptions: Any | None = None
    interfaceName: str | None = None
    key: str | None = None
    storage: str | None = None
    type: str | None = None
    value: Any | None = None

    def __repr__(self) -> str:
        return f"<AdvancedConfigAPIEntry ({self.key})>"


@dataclasses.dataclass(slots=True, frozen=True)
class AdvancedConfigQuery(DictDataClass):
    configInterface: str | None = None
    defaultValues: bool = True
    description: bool = True
    enumInfo: bool = True
    includeExtensions: bool = True
    values: bool = True
    pattern: str | None = None

    def __repr__(self) -> str:
        return f"<AdvancedConfigQuery ({self.configInterface})>"


@dataclasses.dataclass(slots=True, frozen=True)
class AddLinksQuery(DictDataClass):
    assignJobID: bool | None = None
    autoExtract: bool | None = None
    autostart: bool | None = None
    deepDecrypt: bool | None = None
    destinationFolder: str | None = None
    downloadPassword: str | None = None
    extractPassword: str | None = None
    links: str | None = None
    sourceUrl: str | None = None
    overwritePackagizerRules: bool | None = None
    packageName: str | None = None
    dataURLs: list[str] = dataclasses.field(default_factory=list)
    priority: Priority | None = Priority.DEFAULT

    def __repr__(self) -> str:
        return f"<AddLinksQuery ({self.packageName})>"


@dataclasses.dataclass(slots=True, frozen=True)
class APIQuery(DictDataClass):
    """A standard api query.

    Most endpoint use a specialized version.
    """

    empty: bool
    maxResults: int
    startAt: int
    forNullKey: str | None = None

    def __repr__(self) -> str:
        return "<APIQuery>"

    @staticmethod
    def default():
        return APIQuery(empty=False, forNullKey="", maxResults=-1, startAt=0)


@dataclasses.dataclass(slots=True, frozen=True)
class CrawledLinkQuery(DictDataClass):
    availability: bool | None = None
    bytesTotal: bool | None = None
    comment: bool | None = None
    enabled: bool | None = None
    host: bool | None = None
    jobUUIDs: list[int] | None = None
    maxResults: int | None = None
    packageUUIDs: list[int] | None = None
    password: bool | None = None
    priority: bool | None = None
    startAt: int | None = None
    status: bool | None = None
    url: bool | None = None
    variantID: bool | None = None
    variantIcon: bool | None = None
    variantName: bool | None = None
    variants: bool | None = None

    def __repr__(self) -> str:
        return "<CrawledLinkQuery>"

    @staticmethod
    def default():
        return CrawledLinkQuery(
            availability=True,
            bytesTotal=True,
            comment=True,
            enabled=True,
            host=True,
            jobUUIDs=None,
            maxResults=-1,
            packageUUIDs=None,
            password=True,
            priority=True,
            startAt=0,
            status=True,
            url=True,
            variantID=True,
            variantIcon=True,
            variantName=True,
            variants=True,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class CrawledPackageQuery(DictDataClass):
    availableOfflineCount: bool | None = None
    availableOnlineCount: bool | None = None
    availableTempUnknownCount: bool | None = None
    availableUnknownCount: bool | None = None
    bytesTotal: bool | None = None
    childCount: bool | None = None
    comment: bool | None = None
    enabled: bool | None = None
    hosts: bool | None = None
    maxResults: int | None = None
    packageUUIDs: list[int] | None = None
    priority: bool | None = None
    saveTo: bool | None = None
    startAt: int | None = None
    status: bool | None = None

    def __repr__(self) -> str:
        return "<CrawledPackageQuery>"

    @staticmethod
    def default():
        return CrawledPackageQuery(
            availableOfflineCount=True,
            availableOnlineCount=True,
            availableTempUnknownCount=True,
            availableUnknownCount=True,
            bytesTotal=True,
            childCount=True,
            comment=True,
            enabled=True,
            hosts=True,
            maxResults=-1,
            packageUUIDs=None,
            priority=True,
            saveTo=True,
            startAt=0,
            status=True,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class ExtensionQuery(DictDataClass):
    configInterface: bool | None = None
    description: bool | None = None
    enabled: bool | None = None
    iconKey: bool | None = None
    installed: bool | None = None
    name: bool | None = None
    pattern: str | None = None

    def __repr__(self) -> str:
        return "<ExtensionQuery>"

    @staticmethod
    def default():
        return ExtensionQuery(
            configInterface=True,
            description=True,
            enabled=True,
            iconKey=True,
            installed=True,
            name=True,
            pattern=None,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class LinkCrawlerJobsQuery(DictDataClass):
    collectorInfo: bool | None = None
    jobIds: list[int] | None = None

    def __repr__(self) -> str:
        return "<LinkCrawlerJobsQuery>"

    @staticmethod
    def default():
        return LinkCrawlerJobsQuery(collectorInfo=True, jobIds=None)


@dataclasses.dataclass(slots=True, frozen=True)
class LinkQuery(DictDataClass):
    addedDate: bool | None = None
    bytesLoaded: bool | None = None
    bytesTotal: bool | None = None
    comment: bool | None = None
    enabled: bool | None = None
    eta: bool | None = None
    extractionStatus: bool | None = None
    finished: bool | None = None
    finishedDate: bool | None = None
    host: bool | None = None
    jobUUIDs: list[int] | None = None
    maxResults: int | None = None
    packageUUIDs: list[int] | None = None
    password: bool | None = None
    priority: bool | None = None
    running: bool | None = None
    skipped: bool | None = None
    speed: bool | None = None
    startAt: int | None = None
    status: bool | None = None
    url: bool | None = None

    def __repr__(self) -> str:
        return "<LinkQuery>"

    @staticmethod
    def default():
        return LinkQuery(
            addedDate=True,
            bytesLoaded=True,
            bytesTotal=True,
            comment=True,
            enabled=True,
            eta=True,
            extractionStatus=True,
            finished=True,
            finishedDate=True,
            host=True,
            jobUUIDs=None,
            maxResults=-1,
            packageUUIDs=None,
            password=True,
            priority=True,
            running=True,
            skipped=True,
            speed=True,
            startAt=0,
            status=True,
            url=True,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class PackageQuery(DictDataClass):
    bytesLoaded: bool | None = None
    bytesTotal: bool | None = None
    childCount: bool | None = None
    comment: bool | None = None
    enabled: bool | None = None
    eta: bool | None = None
    finished: bool | None = None
    hosts: bool | None = None
    maxResults: int | None = None
    packageUUIDs: list[int] | None = None
    priority: bool | None = None
    running: bool | None = None
    saveTo: bool | None = None
    speed: bool | None = None
    startAt: int | None = None
    status: bool | None = None

    def __repr__(self) -> str:
        return "<PackageQuery>"

    @staticmethod
    def default():
        return PackageQuery(
            bytesLoaded=True,
            bytesTotal=True,
            childCount=True,
            comment=True,
            enabled=True,
            eta=True,
            finished=True,
            hosts=True,
            maxResults=-1,
            packageUUIDs=None,
            priority=True,
            running=True,
            saveTo=True,
            speed=True,
            startAt=0,
            status=True,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class PluginsQuery(DictDataClass):
    pattern: str | None = None
    version: str | None = None

    def __repr__(self) -> str:
        return f"<PluginsQuery ({self.pattern})>"

    @staticmethod
    def default():
        return PluginsQuery(pattern="", version=None)


@dataclasses.dataclass(slots=True, frozen=True)
class ListConfigQuery(DictDataClass):
    pattern: str = ""
    returnDescription: bool = True
    returnValues: bool = True
    returnDefaultValues: bool = True
    returnEnumInfo: bool = True
