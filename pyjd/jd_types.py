"""
These are the types and constants that are defined in JDownloader

https://my.jdownloader.org/developers/index.html#tag_342
"""
# ruff: noqa: N815

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any

from pyjd.common import DictDataClass

if TYPE_CHECKING:
    import dataclasses
else:
    try:
        from pydantic import dataclasses
    except ImportError:
        import dataclasses


@dataclasses.dataclass(slots=True, frozen=True)
class JDDevice:
    name: str
    id: str
    type: str


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
    FTP = "FTP"
    HTTP = "HTTP"


class Context(StrEnum):
    """Contextmenu selection."""

    LGC = "LGC"
    "linkgrabber rightclick"

    DLC = "DLC"
    "downloadlist rightclick"


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


@dataclasses.dataclass(slots=True, frozen=True)
class Account(DictDataClass):
    """This is a premium hoster account

    Initializes itself from a query result (dict)
    """

    uuid: int
    errorString: str | None = None
    errorType: str | None = None
    hostname: str | None = None
    trafficLeft: int | None = None
    trafficMax: int | None = None
    username: str | None = None
    validUntil: int | None = None
    valid: bool | None = None
    enabled: bool | None = None

    def __repr__(self) -> str:
        return f"<Account ({self.uuid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class BasicAuth(DictDataClass):
    id: int
    created: int | None = None
    enabled: bool | None = None
    hostmask: str | None = None
    lastValidated: int | None = None
    password: str | None = None
    type: BasicAuthType | None = None
    username: str | None = None

    def __repr__(self) -> str:
        return f"<BasicAuth ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class CaptchaJob(DictDataClass):
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
class LinkVariant(DictDataClass):
    iconKey: str | None = None
    id: str | None = None
    name: str | None = None

    def __repr__(self) -> str:
        return f"<LinkVariant ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class CrawledLink(DictDataClass):
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
class CrawledPackage(DictDataClass):
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
class DialogInfo(DictDataClass):
    properties: dict[str, str] | None
    type: str | None = None

    def __repr__(self) -> str:
        return f"<DialogInfo ({self.type})>"


@dataclasses.dataclass(slots=True, frozen=True)
class DialogTypeInfo(DictDataClass):
    in_: dict[str, str] | None
    out: dict[str, str] | None

    def __repr__(self) -> str:
        return "<DialogTypeInfo>"


@dataclasses.dataclass(slots=True, frozen=True)
class DownloadLink(DictDataClass):
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
class EnumOption(DictDataClass):
    label: str | None = None
    name: str | None = None

    def __repr__(self) -> str:
        return f"<EnumOption ({self.name})>"


@dataclasses.dataclass(slots=True, frozen=True)
class Extension(DictDataClass):
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
class FilePackage(DictDataClass):
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
class IconDescriptor(DictDataClass):
    cls: str | None = None
    key: str | None = None
    prps: Any | None = None
    rsc: list[IconDescriptor] | None = None

    def __repr__(self) -> str:
        return f"<IconDescriptor ({self.key})>"


@dataclasses.dataclass(slots=True, frozen=True)
class JobLinkCrawler(DictDataClass):
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
class LinkStatus(DictDataClass):
    host: str | None = None
    linkCheckID: str | None = None
    name: str | None = None
    size: int | None = None
    status: AvailableLinkState | None = None
    url: str | None = None

    def __repr__(self) -> str:
        return f"<LinkStatus ({self.linkCheckID})>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkCheckResult(DictDataClass):
    link: list[LinkStatus] | None
    status: Status | None

    def __repr__(self) -> str:
        return "<LinkCheckResult>"


@dataclasses.dataclass(slots=True, frozen=True)
class LinkCollectingJob(DictDataClass):
    id: int | None = None

    def __repr__(self) -> str:
        return f"<LinkCollectingJob ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class LogFolder(DictDataClass):
    created: int | None = None
    current: bool | None = None
    lastModified: int | None = None

    def __repr__(self) -> str:
        return "<LogFolder>"


@dataclasses.dataclass(slots=True, frozen=True)
class MenuStructure(DictDataClass):
    children: list[MenuStructure] | None
    icon: str | None = None
    id: str | None = None
    name: str | None = None
    type: MenuType | None = None

    def __repr__(self) -> str:
        return f"<MenuStructure ({self.id})>"


@dataclasses.dataclass(slots=True, frozen=True)
class Plugin(DictDataClass):
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
class PublisherResponse(DictDataClass):
    eventids: list[str] | None
    publisher: str | None = None

    def __repr__(self) -> str:
        return f"<PublisherResponse ({self.publisher})>"


@dataclasses.dataclass(slots=True, frozen=True)
class SubscriptionResponse(DictDataClass):
    exclusions: list[str] | None
    maxKeepalive: int | None = None
    maxPolltimeout: int | None = None
    subscribed: bool | None = None
    subscriptionid: int | None = None
    subscriptions: list[str] | None = None

    def __repr__(self) -> str:
        return f"<SubscriptionResponse ({self.subscriptionid})>"


@dataclasses.dataclass(slots=True, frozen=True)
class Address(DictDataClass):
    port: int
    ip: str


@dataclasses.dataclass(slots=True, frozen=True)
class DirectConnectionInfos(DictDataClass):
    infos: list[Address] | None
    rebindProtectionDetected: bool | None = None
    mode: str | None = None
