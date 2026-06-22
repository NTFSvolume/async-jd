"""
These are the types and constants that are defined in JDownloader.

For more information, see here:
    https://my.jdownloader.org/developers/index.html#tag_342
"""
# ruff: noqa: N815

from __future__ import annotations

import dataclasses as py_dataclasses
from enum import StrEnum
from typing import Any, ClassVar

from pydantic import dataclasses


class _DictDataClass:
    __dataclass_fields__: ClassVar[dict[str, py_dataclasses.Field[Any]]]

    def __json__(self) -> dict[str, Any]:
        return py_dataclasses.asdict(self)


class AbstractType(StrEnum):
    """Abstract types that are used for config entries."""

    BOOLEAN = "BOOLEAN"
    INT = "INT"
    LONG = "LONG"
    STRING = "STRING"
    OBJECT = "OBJECT"
    OBJECT_LIST = "OBJECT_LIST"
    STRING_LIST = "STRING_LIST"
    ENUM = "ENUM"
    BYTE = "BYTE"
    CHAR = "CHAR"
    DOUBLE = "DOUBLE"
    FLOAT = "FLOAT"
    SHORT = "SHORT"
    BOOLEAN_LIST = "BOOLEAN_LIST"
    BYTE_LIST = "BYTE_LIST"
    SHORT_LIST = "SHORT_LIST"
    LONG_LIST = "LONG_LIST"
    INT_LIST = "INT_LIST"
    FLOAT_LIST = "FLOAT_LIST"
    ENUM_LIST = "ENUM_LIST"
    DOUBLE_LIST = "DOUBLE_LIST"
    CHAR_LIST = "CHAR_LIST"
    UNKNOWN = "UNKNOWN"
    HEX_COLOR = "HEX_COLOR"
    HEX_COLOR_LIST = "HEX_COLOR_LIST"
    ACTION = "ACTION"


class DeleteAction(StrEnum):
    """Delete actions, that can be executed.

    This corresponds to the "Action" enum of JDownloader.
    """

    DELETE_ALL = "DELETE_ALL"
    DELETE_DISABLED = "DELETE_DISABLED"
    DELETE_FAILED = "DELETE_FAILED"
    DELETE_FINISHED = "DELETE_FINISHED"
    DELETE_DUPE = "DELETE_DUPE"
    DELETE_MODE = "DELETE_MODE"


class AvailableLinkState(StrEnum):
    """The availability of a link."""

    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"
    TEMP_UNKNOWN = "TEMP_UNKNOWN"


class BasicAuthType(StrEnum):
    """Types of basic auth protocols."""

    FTP = "FTP"
    HTTP = "HTTP"


class Context(StrEnum):
    """Contextmenu selection."""

    LGC = "LGC"  # linkgrabber rightclick
    DLC = "DLC"  # downloadlist rightclick


class MenuType(StrEnum):
    """Menu types"""

    CONTAINER = "CONTAINER"
    ACTION = "ACTION"
    LINK = "LINK"


class Mode(StrEnum):
    """Modes for package deletion."""

    REMOVE_LINKS_AND_DELETE_FILES = "REMOVE_LINKS_AND_DELETE_FILES"
    REMOVE_LINKS_AND_RECYCLE_FILES = "REMOVE_LINKS_AND_RECYCLE_FILES"
    REMOVE_LINKS_ONLY = "REMOVE_LINKS_ONLY"


class Priority(StrEnum):
    """Download priority for packages."""

    HIGHEST = "HIGHEST"
    HIGHER = "HIGHER"
    HIGH = "HIGH"
    DEFAULT = "DEFAULT"
    LOW = "LOW"
    LOWER = "LOWER"
    LOWEST = "LOWEST"


class Reason(StrEnum):
    """Reasons for exceptions."""

    CONNECTION_UNAVAILABLE = "CONNECTION_UNAVAILABLE"
    TOO_MANY_RETRIES = "TOO_MANY_RETRIES"
    CAPTCHA = "CAPTCHA"
    MANUAL = "MANUAL"
    DISK_FULL = "DISK_FULL"
    NO_ACCOUNT = "NO_ACCOUNT"
    INVALID_DESTINATION = "INVALID_DESTINATION"
    FILE_EXISTS = "FILE_EXISTS"
    UPDATE_RESTART_REQUIRED = "UPDATE_RESTART_REQUIRED"
    FFMPEG_MISSING = "FFMPEG_MISSING"
    FFPROBE_MISSING = "FFPROBE_MISSING"


class SelectionType(StrEnum):
    """Types for selection"""

    SELECTED = "SELECTED"
    UNSELECTED = "UNSELECTED"
    ALL = "ALL"
    NONE = "NONE"


class SkipRequest(StrEnum):
    """Captcha skip request"""

    SINGLE = "SINGLE"
    BLOCK_HOSTER = "BLOCK_HOSTER"
    BLOCK_ALL_CAPTCHAS = "BLOCK_ALL_CAPTCHAS"
    BLOCK_PACKAGE = "BLOCK_PACKAGE"
    REFRESH = "REFRESH"
    STOP_CURRENT_ACTION = "STOP_CURRENT_ACTION"
    TIMEOUT = "TIMEOUT"


class Status(StrEnum):
    """Status"""

    NA = "NA"
    PENDING = "PENDING"
    FINISHED = "FINISHED"


#
# structures and objects
#


@dataclasses.dataclass(slots=True, frozen=True)
class Account(_DictDataClass):
    """This is a premium hoster account

    Initializes itself from a query result (dict)
    """

    enabled: bool | None
    errorString: str | None
    errorType: str | None
    hostname: str | None
    trafficLeft: int | None
    trafficMax: int | None
    username: str | None
    uuid: int | None
    valid: bool | None
    validUntil: int | None

    def __repr__(self) -> str:
        return f"<Account ({self.uuid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class AccountQuery(_DictDataClass):
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

    @staticmethod
    def default():
        return AccountQuery(
            enabled=True,
            error=True,
            maxResults=-1,
            startAt=0,
            trafficLeft=True,
            trafficMax=True,
            userName=True,
            uuidlist=None,
            valid=True,
            validUntil=True,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class AdvancedConfigAPIEntry(_DictDataClass):
    abstractType: AbstractType | None
    defaultValue: Any | None
    docs: str | None
    enumLabel: str | None
    enumOptions: Any | None
    interfaceName: str | None
    key: str | None
    storage: str | None
    type: str | None
    value: Any | None

    def __repr__(self) -> str:
        return f"<AdvancedConfigAPIEntry ({self.key})>"


@dataclasses.dataclass(slots=True, frozen=True)
class AdvancedConfigQuery(_DictDataClass):
    configInterface: str | None
    defaultValues: bool
    description: bool
    enumInfo: bool
    includeExtensions: bool
    pattern: str | None
    values: bool

    def __repr__(self) -> str:
        return f"<AdvancedConfigQuery ({self.configInterface})>"

    @staticmethod
    def default():
        return AdvancedConfigQuery(
            configInterface=None,
            defaultValues=True,
            description=True,
            enumInfo=True,
            includeExtensions=True,
            pattern=None,
            values=True,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class BasicAuth(_DictDataClass):
    created: int | None
    enabled: bool | None
    hostmask: str | None
    id: int | None
    lastValidated: int | None
    password: str | None
    type: BasicAuthType | None
    username: str | None

    def __repr__(self) -> str:
        return f"<BasicAuth ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class AddLinksQuery(_DictDataClass):
    assignJobID: bool | None
    autoExtract: bool | None
    autostart: bool | None
    deepDecrypt: bool | None
    destinationFolder: str | None
    downloadPassword: str | None
    extractPassword: str | None
    links: str | None
    sourceUrl: str | None
    overwritePackagizerRules: bool | None
    packageName: str | None
    dataURLs: list[str] = []
    priority: Priority | None = Priority.DEFAULT

    def __repr__(self) -> str:
        return f"<AddLinksQuery ({self.packageName})>"


@dataclasses.dataclass(slots=True, frozen=True)
class APIQuery(_DictDataClass):
    """A standard api query.

    Most endpoint use a specialized version.
    """

    empty: bool
    forNullKey: str | None
    maxResults: int
    startAt: int

    def __repr__(self) -> str:
        return "<APIQuery>"

    @staticmethod
    def default():
        return APIQuery(empty=False, forNullKey="", maxResults=-1, startAt=0)


@dataclasses.dataclass(slots=True, frozen=True)
class CaptchaJob(_DictDataClass):
    captchaCategory: str | None
    created: int | None
    explain: str | None
    hoster: str | None
    id: int | None
    link: int | None
    timeout: int | None
    type: str | None

    def __repr__(self) -> str:
        return f"<CaptchaJob ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkVariant(_DictDataClass):
    iconKey: str | None
    id: str | None
    name: str | None

    def __repr__(self) -> str:
        return f"<LinkVariant ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class CrawledLink(_DictDataClass):
    availability: AvailableLinkState | None
    bytesTotal: int | None
    comment: str | None
    downloadPassword: str | None
    enabled: bool | None
    host: str | None
    name: str | None
    packageUUID: int | None
    priority: Priority | None
    url: str | None
    uuid: int | None
    variant: LinkVariant | None
    variants: bool | None

    def __repr__(self) -> str:
        return f"<CrawledLink ({self.uuid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class CrawledLinkQuery(_DictDataClass):
    availability: bool | None
    bytesTotal: bool | None
    comment: bool | None
    enabled: bool | None
    host: bool | None
    jobUUIDs: list[int] | None
    maxResults: int | None
    packageUUIDs: list[int] | None
    password: bool | None
    priority: bool | None
    startAt: int | None
    status: bool | None
    url: bool | None
    variantID: bool | None
    variantIcon: bool | None
    variantName: bool | None
    variants: bool | None

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
class CrawledPackage(_DictDataClass):
    bytesTotal: int | None
    childCount: int | None
    comment: str | None
    downloadPassword: str | None
    enabled: bool | None
    hosts: list[str] | None
    name: str | None
    offlineCount: int | None
    onlineCount: int | None
    priority: Priority | None
    saveTo: str | None
    tempUnknownCount: int | None
    unknownCount: int | None
    uuid: int | None

    def __repr__(self) -> str:
        return f"<CrawledPackage ({self.uuid})"


@dataclasses.dataclass(slots=True, frozen=True)
class CrawledPackageQuery(_DictDataClass):
    availableOfflineCount: bool | None
    availableOnlineCount: bool | None
    availableTempUnknownCount: bool | None
    availableUnknownCount: bool | None
    bytesTotal: bool | None
    childCount: bool | None
    comment: bool | None
    enabled: bool | None
    hosts: bool | None
    maxResults: int | None
    packageUUIDs: list[int] | None
    priority: bool | None
    saveTo: bool | None
    startAt: int | None
    status: bool | None

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
class DialogInfo(_DictDataClass):
    properties: dict[str, str] | None
    type: str | None

    def __repr__(self) -> str:
        return f"<DialogInfo ({self.type})>"


@dataclasses.dataclass(slots=True, frozen=True)
class DialogTypeInfo(_DictDataClass):
    in_: dict[str, str] | None
    out: dict[str, str] | None

    def __repr__(self) -> str:
        return "<DialogTypeInfo>"


@dataclasses.dataclass(slots=True, frozen=True)
class DownloadLink(_DictDataClass):
    addedDate: int | None
    bytesLoaded: int | None
    bytesTotal: int | None
    comment: str | None
    downloadPassword: str | None
    enabled: bool | None
    eta: int | None
    extractionStatus: str | None
    finished: bool | None
    finishedDate: int | None
    host: str | None
    name: str | None
    packageUUID: int | None
    priority: Priority | None
    running: int | None
    skipped: int | None
    speed: int | None
    status: str | None
    statusIconKey: str | None
    url: str | None
    uuid: int | None

    def __repr__(self) -> str:
        return f"<DownloadLink ({self.uuid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class EnumOption(_DictDataClass):
    label: str | None
    name: str | None

    def __repr__(self) -> str:
        return f"<EnumOption ({self.name})>"


@dataclasses.dataclass(slots=True, frozen=True)
class Extension(_DictDataClass):
    configInterface: str | None
    description: str | None
    enabled: bool | None
    iconKey: str | None
    id: str | None
    installed: bool | None
    name: str | None

    def __repr__(self) -> str:
        return f"<Extension ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class ExtensionQuery(_DictDataClass):
    configInterface: bool | None
    description: bool | None
    enabled: bool | None
    iconKey: bool | None
    installed: bool | None
    name: bool | None
    pattern: str | None

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
class FilePackage(_DictDataClass):
    activeTask: str | None
    bytesLoaded: int | None
    bytesTotal: int | None
    childCount: int | None
    comment: str | None
    downloadPassword: str | None
    enabled: bool | None
    eta: int | None
    finished: bool | None
    hosts: list[str] | None
    name: str | None
    priority: Priority | None
    running: bool | None
    saveTo: str | None
    speed: int | None
    status: str | None
    statusIconKey: str | None
    uuid: int | None

    def __repr__(self) -> str:
        return f"<FilePackage ({self.uuid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class IconDescriptor(_DictDataClass):
    cls: str | None
    key: str | None
    prps: Any | None
    rsc: list[IconDescriptor] | None

    def __repr__(self) -> str:
        return f"<IconDescriptor ({self.key})>"


@dataclasses.dataclass(slots=True, frozen=True)
class JobLinkCrawler(_DictDataClass):
    broken: int | None
    checking: bool | None
    crawled: int | None
    crawledId: int | None
    crawling: bool | None
    filtered: int | None
    jobId: int | None
    unhandled: int | None

    def __repr__(self) -> str:
        return f"<JobLinkCrawler ({self.crawledId})>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkStatus(_DictDataClass):
    host: str | None
    linkCheckID: str | None
    name: str | None
    size: int | None
    status: AvailableLinkState | None
    url: str | None

    def __repr__(self) -> str:
        return f"<LinkStatus ({self.linkCheckID})>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkCheckResult(_DictDataClass):
    link: list[LinkStatus] | None
    status: Status | None

    def __repr__(self) -> str:
        return "<LinkCheckResult>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkCollectingJob(_DictDataClass):
    id: int | None

    def __repr__(self) -> str:
        return f"<LinkCollectingJob ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkCrawlerJobsQuery(_DictDataClass):
    collectorInfo: bool | None
    jobIds: list[int] | None

    def __repr__(self) -> str:
        return "<LinkCrawlerJobsQuery>"

    @staticmethod
    def default():
        return LinkCrawlerJobsQuery(collectorInfo=True, jobIds=None)


@dataclasses.dataclass(slots=True, frozen=True)
class LinkQuery(_DictDataClass):
    addedDate: bool | None
    bytesLoaded: bool | None
    bytesTotal: bool | None
    comment: bool | None
    enabled: bool | None
    eta: bool | None
    extractionStatus: bool | None
    finished: bool | None
    finishedDate: bool | None
    host: bool | None
    jobUUIDs: list[int] | None
    maxResults: int | None
    packageUUIDs: list[int] | None
    password: bool | None
    priority: bool | None
    running: bool | None
    skipped: bool | None
    speed: bool | None
    startAt: int | None
    status: bool | None
    url: bool | None

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
class LogFolder(_DictDataClass):
    created: int | None
    current: bool | None
    lastModified: int | None

    def __repr__(self) -> str:
        return "<LogFolder>"


@dataclasses.dataclass(slots=True, frozen=True)
class MenuStructure(_DictDataClass):
    children: list[MenuStructure] | None
    icon: str | None
    id: str | None
    name: str | None
    type: MenuType | None

    def __repr__(self) -> str:
        return f"<MenuStructure ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class PackageQuery(_DictDataClass):
    bytesLoaded: bool | None
    bytesTotal: bool | None
    childCount: bool | None
    comment: bool | None
    enabled: bool | None
    eta: bool | None
    finished: bool | None
    hosts: bool | None
    maxResults: int | None
    packageUUIDs: list[int] | None
    priority: bool | None
    running: bool | None
    saveTo: bool | None
    speed: bool | None
    startAt: int | None
    status: bool | None

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
class Plugin(_DictDataClass):
    abstractType: AbstractType | None
    className: str | None
    defaultValue: Any | None
    displayName: str | None
    docs: str | None
    enumLabel: str | None
    enumOptions: Any | None
    interfaceName: str | None
    key: str | None
    pattern: str | None
    storage: str | None
    type: str | None
    value: Any | None
    version: str | None

    def __repr__(self) -> str:
        return f"<Plugin ({self.className})>"


@dataclasses.dataclass(slots=True, frozen=True)
class PluginsQuery(_DictDataClass):
    pattern: str | None
    version: str | None

    def __repr__(self) -> str:
        return f"<PluginsQuery ({self.pattern})>"

    @staticmethod
    def default():
        return PluginsQuery(pattern="", version=None)


@dataclasses.dataclass(slots=True, frozen=True)
class PublisherResponse(_DictDataClass):
    eventids: list[str] | None
    publisher: str | None

    def __repr__(self) -> str:
        return f"<PublisherResponse ({self.publisher})>"


@dataclasses.dataclass(slots=True, frozen=True)
class SubscriptionResponse(_DictDataClass):
    exclusions: list[str] | None
    maxKeepalive: int | None
    maxPolltimeout: int | None
    subscribed: bool | None
    subscriptionid: int | None
    subscriptions: list[str] | None

    def __repr__(self) -> str:
        return f"<SubscriptionResponse ({self.subscriptionid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class IPandPort(_DictDataClass):
    port: int
    ip: str


@dataclasses.dataclass(slots=True, frozen=True)
class DirectConnectionInfos(_DictDataClass):
    infos: list[IPandPort] | None
    rebindProtectionDetected: bool | None
    mode: str | None
