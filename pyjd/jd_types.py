"""
These are the types and constants that are defined in JDownloader.

For more information, see here:
    https://my.jdownloader.org/developers/index.html#tag_342
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AbstractType(str, Enum):
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


class DeleteAction(str, Enum):
    """Delete actions, that can be executed.

    This corresponds to the "Action" enum of JDownloader.
    """

    DELETE_ALL = "DELETE_ALL"
    DELETE_DISABLED = "DELETE_DISABLED"
    DELETE_FAILED = "DELETE_FAILED"
    DELETE_FINISHED = "DELETE_FINISHED"
    DELETE_DUPE = "DELETE_DUPE"
    DELETE_MODE = "DELETE_MODE"


class AvailableLinkState(str, Enum):
    """The availability of a link."""

    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"
    TEMP_UNKNOWN = "TEMP_UNKNOWN"


class BasicAuthType(str, Enum):
    """Types of basic auth protocols."""

    FTP = "FTP"
    HTTP = "HTTP"


class Context(str, Enum):
    """Contextmenu selection."""

    LGC = "LGC"  # linkgrabber rightclick
    DLC = "DLC"  # downloadlist rightclick


class MenuType(str, Enum):
    """Menu types"""

    CONTAINER = "CONTAINER"
    ACTION = "ACTION"
    LINK = "LINK"


class Mode(str, Enum):
    """Modes for package deletion."""

    REMOVE_LINKS_AND_DELETE_FILES = "REMOVE_LINKS_AND_DELETE_FILES"
    REMOVE_LINKS_AND_RECYCLE_FILES = "REMOVE_LINKS_AND_RECYCLE_FILES"
    REMOVE_LINKS_ONLY = "REMOVE_LINKS_ONLY"


class Priority(str, Enum):
    """Download priority for packages."""

    HIGHEST = "HIGHEST"
    HIGHER = "HIGHER"
    HIGH = "HIGH"
    DEFAULT = "DEFAULT"
    LOW = "LOW"
    LOWER = "LOWER"
    LOWEST = "LOWEST"


class Reason(str, Enum):
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


class SelectionType(str, Enum):
    """Types for selection"""

    SELECTED = "SELECTED"
    UNSELECTED = "UNSELECTED"
    ALL = "ALL"
    NONE = "NONE"


class SkipRequest(str, Enum):
    """Captcha skip request"""

    SINGLE = "SINGLE"
    BLOCK_HOSTER = "BLOCK_HOSTER"
    BLOCK_ALL_CAPTCHAS = "BLOCK_ALL_CAPTCHAS"
    BLOCK_PACKAGE = "BLOCK_PACKAGE"
    REFRESH = "REFRESH"
    STOP_CURRENT_ACTION = "STOP_CURRENT_ACTION"
    TIMEOUT = "TIMEOUT"


class Status(str, Enum):
    """Status"""

    NA = "NA"
    PENDING = "PENDING"
    FINISHED = "FINISHED"


#
# structures and objects
#


class Account(BaseModel):
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


class AccountQuery(BaseModel):
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
    uuidlist: list[int] | None
    valid: bool = True
    validUntil: bool = True

    def __repr__(self):
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


class AdvancedConfigAPIEntry(BaseModel):
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

    def __repr__(self):
        return f"<AdvancedConfigAPIEntry ({self.key})>"


class AdvancedConfigQuery(BaseModel):
    configInterface: str | None
    defaultValues: bool
    description: bool
    enumInfo: bool
    includeExtensions: bool
    pattern: str | None
    values: bool

    def __repr__(self):
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


class BasicAuth(BaseModel):
    created: int | None
    enabled: bool | None
    hostmask: str | None
    id: int | None
    lastValidated: int | None
    password: str | None
    type: BasicAuthType | None
    username: str | None

    def __repr__(self):
        return f"<BasicAuth ({self.id})>"


class AddLinksQuery(BaseModel):
    assignJobID: bool | None
    autoExtract: bool | None
    autostart: bool | None
    dataURLs: list[str] = []
    deepDecrypt: bool | None
    destinationFolder: str | None
    downloadPassword: str | None
    extractPassword: str | None
    links: str | None
    overwritePackagizerRules: bool | None
    packageName: str | None
    priority: Priority | None = Priority.DEFAULT
    sourceUrl: str | None

    def __repr__(self):
        return f"<AddLinksQuery ({self.packageName})>"


class APIQuery(BaseModel):
    """A standard api query.

    Most endpoint use a specialized version.
    """

    empty: bool
    forNullKey: str | None
    maxResults: int
    startAt: int

    def __repr__(self):
        return "<APIQuery>"

    @staticmethod
    def default():
        return APIQuery(empty=False, forNullKey="", maxResults=-1, startAt=0)


class CaptchaJob(BaseModel):
    captchaCategory: str | None
    created: int | None
    explain: str | None
    hoster: str | None
    id: int | None
    link: int | None
    timeout: int | None
    type: str | None

    def __repr__(self):
        return f"<CaptchaJob ({self.id})>"


class LinkVariant(BaseModel):
    iconKey: str | None
    id: str | None
    name: str | None

    def __repr__(self):
        return f"<LinkVariant ({self.id})>"


class CrawledLink(BaseModel):
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

    def __repr__(self):
        return f"<CrawledLink ({self.uuid})>"


class CrawledLinkQuery(BaseModel):
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

    def __repr__(self):
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


class CrawledPackage(BaseModel):
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

    def __repr__(self):
        return f"<CrawledPackage ({self.uuid})"


class CrawledPackageQuery(BaseModel):
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

    def __repr__(self):
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


class DialogInfo(BaseModel):
    properties: dict[str, str] | None
    type: str | None

    def __repr__(self):
        return f"<DialogInfo ({self.type})>"


class DialogTypeInfo(BaseModel):
    in_: dict[str, str] | None = Field(..., alias="in")
    out: dict[str, str] | None

    def __repr__(self):
        return "<DialogTypeInfo>"


class DownloadLink(BaseModel):
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

    def __repr__(self):
        return f"<DownloadLink ({self.uuid})>"


class EnumOption(BaseModel):
    label: str | None
    name: str | None

    def __repr__(self):
        return f"<EnumOption ({self.name})>"


class Extension(BaseModel):
    configInterface: str | None
    description: str | None
    enabled: bool | None
    iconKey: str | None
    id: str | None
    installed: bool | None
    name: str | None

    def __repr__(self):
        return f"<Extension ({self.id})>"


class ExtensionQuery(BaseModel):
    configInterface: bool | None
    description: bool | None
    enabled: bool | None
    iconKey: bool | None
    installed: bool | None
    name: bool | None
    pattern: str | None

    def __repr__(self):
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


class FilePackage(BaseModel):
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

    def __repr__(self):
        return f"<FilePackage ({self.uuid})>"


class IconDescriptor(BaseModel):
    cls: str | None
    key: str | None
    prps: Any | None
    rsc: list[IconDescriptor] | None

    def __repr__(self):
        return f"<IconDescriptor ({self.key})>"


class JobLinkCrawler(BaseModel):
    broken: int | None
    checking: bool | None
    crawled: int | None
    crawledId: int | None
    crawling: bool | None
    filtered: int | None
    jobId: int | None
    unhandled: int | None

    def __repr__(self):
        return f"<JobLinkCrawler ({self.crawledId})>"


class LinkStatus(BaseModel):
    host: str | None
    linkCheckID: str | None
    name: str | None
    size: int | None
    status: AvailableLinkState | None
    url: str | None

    def __repr__(self):
        return f"<LinkStatus ({self.linkCheckID})>"


class LinkCheckResult(BaseModel):
    link: list[LinkStatus] | None
    status: Status | None

    def __repr__(self):
        return "<LinkCheckResult>"


class LinkCollectingJob(BaseModel):
    id: int | None

    def __repr__(self):
        return f"<LinkCollectingJob ({self.id})>"


class LinkCrawlerJobsQuery(BaseModel):
    collectorInfo: bool | None
    jobIds: list[int] | None

    def __repr__(self):
        return "<LinkCrawlerJobsQuery>"

    @staticmethod
    def default():
        return LinkCrawlerJobsQuery(collectorInfo=True, jobIds=None)


class LinkQuery(BaseModel):
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

    def __repr__(self):
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


class LogFolder(BaseModel):
    created: int | None
    current: bool | None
    lastModified: int | None

    def __repr__(self):
        return "<LogFolder>"


class MenuStructure(BaseModel):
    children: list[MenuStructure] | None
    icon: str | None
    id: str | None
    name: str | None
    type: MenuType | None

    def __repr__(self):
        return f"<MenuStructure ({self.id})>"


class PackageQuery(BaseModel):
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

    def __repr__(self):
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


class Plugin(BaseModel):
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

    def __repr__(self):
        return f"<Plugin ({self.className})>"


class PluginsQuery(BaseModel):
    pattern: str | None
    version: str | None

    def __repr__(self):
        return f"<PluginsQuery ({self.pattern})>"

    @staticmethod
    def default():
        return PluginsQuery(pattern="", version=None)


class PublisherResponse(BaseModel):
    eventids: list[str] | None
    publisher: str | None

    def __repr__(self):
        return f"<PublisherResponse ({self.publisher})>"


class SubscriptionResponse(BaseModel):
    exclusions: list[str] | None
    maxKeepalive: int | None
    maxPolltimeout: int | None
    subscribed: bool | None
    subscriptionid: int | None
    subscriptions: list[str] | None

    def __repr__(self):
        return f"<SubscriptionResponse ({self.subscriptionid})>"


class IPandPort(BaseModel):
    port: int
    ip: str


class DirectConnectionInfos(BaseModel):
    infos: list[IPandPort] | None
    rebindProtectionDetected: bool | None
    mode: str | None
