from decimal import Decimal

from uuid import UUID

from icevault._async.storage.s3 import PartEtag
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from icevault.types import DecimalStr, UUIDStr
from icevault.enums import CaseInsensitiveStrEnum, StorageClassEnum


class UploadType(CaseInsensitiveStrEnum):
    multipart = "multipart"
    archive = "archive"


class ArchiveUploadModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    archive_size_kb: DecimalStr | None = Field(None)
    archive_part_count: int | None = None
    archive_name: str | None = None
    file_count: int
    chunk_size_kb: int
    storage_class: StorageClassEnum
    content_type: str = "application/zip"
    is_encrypted: bool = False
    password_hint: str = ""


class PreviewUPloadModel(BaseModel):
    preview_part_count: int | None = None
    preview_size_kb: DecimalStr | None = None
    preview_name: str | None = None
    file_count: int
    chunk_size_kb: int
    storage_class: StorageClassEnum
    content_type: str = "application/zip"
    is_encrypted: bool = False
    password_hint: str = ""


class InitiateUploadPayloadModel(BaseModel):
    collection_id: UUID | None = None
    archive: ArchiveUploadModel | None = None
    preview: PreviewUPloadModel | None = None
    expirers_in_sec: int = 3600


class FileResponseModel(BaseModel):
    url: str
    path: str
    storage_class: str
    fields: dict[str, str]
    part_urls: dict[int, str]
    upload_type: UploadType = UploadType.archive

class InitUploadResponseModel(BaseModel):
    status: str
    message: str | None = None
    uuid: UUID
    archive: FileResponseModel | None = None
    preview: FileResponseModel | None = None
    expires_at: datetime | None = None

class ConfirmUploadPayloadModel(BaseModel):
    uuid: UUIDStr
    archive_hashes: dict[int, str] | None = None
    preview_hashes: dict[int, str] | None = None


class ConfirmUploadResponseModel(BaseModel):
    status: str


class StreamResultModel(BaseModel):
    tags: list[PartEtag]