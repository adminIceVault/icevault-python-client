from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Any
from icevault.constants import ALL_COLLECTIONS_ID
from icevault.enums import CaseInsensitiveStrEnum, StorageClassEnum
from pydantic import BaseModel, ConfigDict, model_validator


class StatusArchiveEnum(CaseInsensitiveStrEnum):
    PENDING = "PENDING"
    ARCHIVED = "ARCHIVED"
    UPLOADED = "UPLOADED"
    RESTORED = "RESTORED"
    DELETED = "DELETED"
    REQUESTED_RESTORING = "REQUESTED_RESTORING"
    REQUESTED = "REQUESTED"
    FAILED = "FAILED"

    @classmethod
    def all(cls):
        return list(map(lambda x: x.value, cls))

class OrderByEnum(CaseInsensitiveStrEnum):
    created_at = "created_at"
    status = "status"
    preview_count = "preview_count"
    file_name = "file_name"
    archive_size = "archive_size"



class GetArchiveFileter(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        str_to_enum="lenient"
    )

    collection_id: str | None = ALL_COLLECTIONS_ID
    limit: int = 100
    offset: int = 0
    search: str | None = None
    status: list[StatusArchiveEnum] | None = StatusArchiveEnum.all()
    is_encrypted: bool = None
    order_by: OrderByEnum | None = OrderByEnum.created_at
    ascending: bool = True

    @model_validator(mode="before")
    @classmethod
    def wrap_single_status_to_list(cls, data: Any) -> Any:
        if isinstance(data, dict) and "status" in data:
            status_val = data["status"]
            if isinstance(status_val, (str, StatusArchiveEnum)):
                data["status"] = [status_val]
        return data

class ArchiveModel(BaseModel):
    uuid: UUID
    created_at: datetime
    size_mb: Decimal
    name: str
    preview_count: int | None = None
    available_to: datetime | None = None
    originals_kb: Decimal | None = None
    previews_kb: Decimal | None = None
    archive_hash: str | None = None
    is_encrypted: bool = False
    password_hint: str | None = None
    storage_class: StorageClassEnum
    buket_id: str | None = None
    status: StatusArchiveEnum

class ArchiveResponseModel(BaseModel):
    items: tuple[ArchiveModel, ...]
    count: int

class PreviewResponseModel(BaseModel):
    url: str

class DownloadResponseModel(BaseModel):
    url: str

class RestoreArchiveResponseModel(BaseModel):
    status: str
    message: str | None = None
    uuid: UUID

class UpdateArchiveModel(BaseModel):
    name: str