"""
These are the types and constants that are defined in JDownloader.

For more information, see here:
    https://my.jdownloader.org/developers/index.html#tag_342
"""
# ruff: noqa: N815

from __future__ import annotations

import dataclasses as py_dataclasses
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Protocol

from pydantic import dataclasses

if TYPE_CHECKING:
    from collections.abc import Sequence


class API(ABC):
    @abstractmethod
    def request(
        self,
        path: str,
        http_method: Literal["GET", "POST"] = "GET",
        params: Sequence[tuple[str, Any]] | None = None,
        action: str | None = None,
        api: str | None = None,
        *,
        binary: bool = False,
    ) -> Any: ...

    @abstractmethod
    def raw_request(
        self,
        path: str,
        http_method: Literal["GET", "POST"] = "GET",
        params: Sequence[tuple[str, Any]] | None = None,
        action: str | None = None,
        api: str | None = None,
    ) -> bytes: ...


class Connection(Protocol):
    def action(
        self,
        path: str,
        params: Sequence[tuple[str, Any]] | None = None,
        *,
        binary: bool = False,
    ) -> Any: ...


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

    errorString: str | None = None
    errorType: str | None = None
    hostname: str | None = None
    trafficLeft: int | None = None
    trafficMax: int | None = None
    username: str | None = None
    uuid: int | None = None

    validUntil: int | None = None
    valid: bool | None = None
    enabled: bool | None = None

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
class AdvancedConfigQuery(_DictDataClass):
    defaultValues: bool
    description: bool
    enumInfo: bool
    includeExtensions: bool
    values: bool
    configInterface: str | None = None
    pattern: str | None = None

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
    created: int | None = None
    enabled: bool | None = None
    hostmask: str | None = None
    id: int | None = None
    lastValidated: int | None = None
    password: str | None = None
    type: BasicAuthType | None = None
    username: str | None = None

    def __repr__(self) -> str:
        return f"<BasicAuth ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class AddLinksQuery(_DictDataClass):
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
    dataURLs: list[str] = py_dataclasses.field(default_factory=list)
    priority: Priority | None = Priority.DEFAULT

    def __repr__(self) -> str:
        return f"<AddLinksQuery ({self.packageName})>"


@dataclasses.dataclass(slots=True, frozen=True)
class APIQuery(_DictDataClass):
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
class CaptchaJob(_DictDataClass):
    captchaCategory: str | None = None
    created: int | None = None
    explain: str | None = None
    hoster: str | None = None
    id: int | None = None
    link: int | None = None
    timeout: int | None = None
    type: str | None = None

    def __repr__(self) -> str:
        return f"<CaptchaJob ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkVariant(_DictDataClass):
    iconKey: str | None = None
    id: str | None = None
    name: str | None = None

    def __repr__(self) -> str:
        return f"<LinkVariant ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class CrawledLink(_DictDataClass):
    availability: AvailableLinkState | None
    bytesTotal: int | None = None
    comment: str | None = None
    downloadPassword: str | None = None
    enabled: bool | None = None
    host: str | None = None
    name: str | None = None
    packageUUID: int | None = None
    priority: Priority | None = None
    url: str | None = None
    uuid: int | None = None
    variant: LinkVariant | None = None
    variants: bool | None = None

    def __repr__(self) -> str:
        return f"<CrawledLink ({self.uuid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class CrawledLinkQuery(_DictDataClass):
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
class CrawledPackage(_DictDataClass):
    bytesTotal: int | None = None
    childCount: int | None = None
    comment: str | None = None
    downloadPassword: str | None = None
    enabled: bool | None = None
    hosts: list[str] | None = None
    name: str | None = None
    offlineCount: int | None = None
    onlineCount: int | None = None
    priority: Priority | None = None
    saveTo: str | None = None
    tempUnknownCount: int | None = None
    unknownCount: int | None = None
    uuid: int | None = None

    def __repr__(self) -> str:
        return f"<CrawledPackage ({self.uuid})"


@dataclasses.dataclass(slots=True, frozen=True)
class CrawledPackageQuery(_DictDataClass):
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
class DialogInfo(_DictDataClass):
    properties: dict[str, str] | None
    type: str | None = None

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
    addedDate: int | None = None
    bytesLoaded: int | None = None
    bytesTotal: int | None = None
    comment: str | None = None
    downloadPassword: str | None = None
    enabled: bool | None = None
    eta: int | None = None
    extractionStatus: str | None = None
    finished: bool | None = None
    finishedDate: int | None = None
    host: str | None = None
    name: str | None = None
    packageUUID: int | None = None
    priority: Priority | None = None
    running: int | None = None
    skipped: int | None = None
    speed: int | None = None
    status: str | None = None
    statusIconKey: str | None = None
    url: str | None = None
    uuid: int | None = None

    def __repr__(self) -> str:
        return f"<DownloadLink ({self.uuid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class EnumOption(_DictDataClass):
    label: str | None = None
    name: str | None = None

    def __repr__(self) -> str:
        return f"<EnumOption ({self.name})>"


@dataclasses.dataclass(slots=True, frozen=True)
class Extension(_DictDataClass):
    configInterface: str | None = None
    description: str | None = None
    enabled: bool | None = None
    iconKey: str | None = None
    id: str | None = None
    installed: bool | None = None
    name: str | None = None

    def __repr__(self) -> str:
        return f"<Extension ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class ExtensionQuery(_DictDataClass):
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
class FilePackage(_DictDataClass):
    activeTask: str | None = None
    bytesLoaded: int | None = None
    bytesTotal: int | None = None
    childCount: int | None = None
    comment: str | None = None
    downloadPassword: str | None = None
    enabled: bool | None = None
    eta: int | None = None
    finished: bool | None = None
    hosts: list[str] | None = None
    name: str | None = None
    priority: Priority | None = None
    running: bool | None = None
    saveTo: str | None = None
    speed: int | None = None
    status: str | None = None
    statusIconKey: str | None = None
    uuid: int | None = None

    def __repr__(self) -> str:
        return f"<FilePackage ({self.uuid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class IconDescriptor(_DictDataClass):
    cls: str | None = None
    key: str | None = None
    prps: Any | None = None
    rsc: list[IconDescriptor] | None = None

    def __repr__(self) -> str:
        return f"<IconDescriptor ({self.key})>"


@dataclasses.dataclass(slots=True, frozen=True)
class JobLinkCrawler(_DictDataClass):
    broken: int | None = None
    checking: bool | None = None
    crawled: int | None = None
    crawledId: int | None = None
    crawling: bool | None = None
    filtered: int | None = None
    jobId: int | None = None
    unhandled: int | None = None

    def __repr__(self) -> str:
        return f"<JobLinkCrawler ({self.crawledId})>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkStatus(_DictDataClass):
    host: str | None = None
    linkCheckID: str | None = None
    name: str | None = None
    size: int | None = None
    status: AvailableLinkState | None = None
    url: str | None = None

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
    id: int | None = None

    def __repr__(self) -> str:
        return f"<LinkCollectingJob ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkCrawlerJobsQuery(_DictDataClass):
    collectorInfo: bool | None = None
    jobIds: list[int] | None = None

    def __repr__(self) -> str:
        return "<LinkCrawlerJobsQuery>"

    @staticmethod
    def default():
        return LinkCrawlerJobsQuery(collectorInfo=True, jobIds=None)


@dataclasses.dataclass(slots=True, frozen=True)
class LinkQuery(_DictDataClass):
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
class LogFolder(_DictDataClass):
    created: int | None = None
    current: bool | None = None
    lastModified: int | None = None

    def __repr__(self) -> str:
        return "<LogFolder>"


@dataclasses.dataclass(slots=True, frozen=True)
class MenuStructure(_DictDataClass):
    children: list[MenuStructure] | None
    icon: str | None = None
    id: str | None = None
    name: str | None = None
    type: MenuType | None = None

    def __repr__(self) -> str:
        return f"<MenuStructure ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class PackageQuery(_DictDataClass):
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
class Plugin(_DictDataClass):
    abstractType: AbstractType | None
    className: str | None = None
    defaultValue: Any | None = None
    displayName: str | None = None
    docs: str | None = None
    enumLabel: str | None = None
    enumOptions: Any | None = None
    interfaceName: str | None = None
    key: str | None = None
    pattern: str | None = None
    storage: str | None = None
    type: str | None = None
    value: Any | None = None
    version: str | None = None

    def __repr__(self) -> str:
        return f"<Plugin ({self.className})>"


@dataclasses.dataclass(slots=True, frozen=True)
class PluginsQuery(_DictDataClass):
    pattern: str | None = None
    version: str | None = None

    def __repr__(self) -> str:
        return f"<PluginsQuery ({self.pattern})>"

    @staticmethod
    def default():
        return PluginsQuery(pattern="", version=None)


@dataclasses.dataclass(slots=True, frozen=True)
class PublisherResponse(_DictDataClass):
    eventids: list[str] | None
    publisher: str | None = None

    def __repr__(self) -> str:
        return f"<PublisherResponse ({self.publisher})>"


@dataclasses.dataclass(slots=True, frozen=True)
class SubscriptionResponse(_DictDataClass):
    exclusions: list[str] | None
    maxKeepalive: int | None = None
    maxPolltimeout: int | None = None
    subscribed: bool | None = None
    subscriptionid: int | None = None
    subscriptions: list[str] | None = None

    def __repr__(self) -> str:
        return f"<SubscriptionResponse ({self.subscriptionid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class IPandPort(_DictDataClass):
    port: int
    ip: str


@dataclasses.dataclass(slots=True, frozen=True)
class DirectConnectionInfos(_DictDataClass):
    infos: list[IPandPort] | None
    rebindProtectionDetected: bool | None = None
    mode: str | None = None
