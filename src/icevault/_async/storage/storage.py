from datetime import datetime

from icevault.storage.endpoints import StorageUrls
from icevault.storage.models import InitUploadResponseModel, InitiateUploadPayloadModel, ConfirmUploadPayloadModel, \
    ConfirmUploadResponseModel, ArchiveUploadModel, StorageClassEnum, FileResponseModel, StreamResultModel
import typing
import os
from icevault.enums import MethodEnum
from pathlib import Path
from icevault._async.storage.async_zip import create_secure_archive
from icevault.constants import ARCHIVE_CHANK_SIZE
from icevault._async.storage.s3 import upload_part, Part, PartEtag
from decimal import Decimal

from pydantic.v1.networks import Parts

if typing.TYPE_CHECKING:
    from icevault import AsyncClient

def gererate_archive_name():
    now = datetime.now()
    return f"vault_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.zip"

class AsyncStorage:
    def __init__(self, client: "AsyncClient", chunk_size: int | None = None) -> None:
        self.client: "AsyncClient" = client
        self.chunk_size = chunk_size or ARCHIVE_CHANK_SIZE

    async def init_upload(self, payload: InitiateUploadPayloadModel) -> InitUploadResponseModel:
        """Fetch and parse filtered archives list."""
        data = payload.model_dump()
        response = await self.client._execute_request(
            method=MethodEnum.POST,
            path=StorageUrls.upload.get_url(),
            json=data
        )
        return InitUploadResponseModel.model_validate(response.json())

    async def confirm_upload(self, payload: ConfirmUploadPayloadModel) -> ConfirmUploadResponseModel:
        """Confirm uploading files"""
        params = payload.model_dump()
        response = await self.client._execute_request(
            method=MethodEnum.POST,
            path=StorageUrls.confirm.get_url(),
            json=params
        )

    async def stream_file(self, file_upload_meta: FileResponseModel, path: str) -> StreamResultModel:
        """"""
        result: list[PartEtag] = await upload_part(
            parts=[Part(
                part_no=part_no,
                url=part_url,
            ) for part_no, part_url in file_upload_meta.part_urls.items()],
            file_path=path,
            chunk_size=self.chunk_size,
        )
        return StreamResultModel(
            tags=result,
        )

    async def upload_files(
        self,
        file_paths: list[str | Path],
        archive_name: str | None = None,
        storage_class: StorageClassEnum | str = StorageClassEnum.DEEP_ARCHIVE,
        passwrod: str | None = None,
        password_hint: str | None = None,
        password: str | None = None,
    ):
        """Upload files"""
        if isinstance(storage_class, str):
            storage_class = StorageClassEnum(storage_class)
        file_paths = [f for f in file_paths if os.path.isfile(f)]
        if not file_paths:
            raise FileNotFoundError(f"No files found at file path: {file_paths}")

        if not archive_name:
            archive_name = gererate_archive_name()
        archive_path: Path = await create_secure_archive(
            file_paths=file_paths,
            password=password,
        )
        file_size_bytes: int = os.path.getsize(archive_path)
        size_kb: Decimal = Decimal(file_size_bytes) / Decimal("1024")
        chunks_ = int(file_size_bytes / self.chunk_size + 1)
        archive_payload = ArchiveUploadModel(
            archive_size_kb=size_kb,
            archive_part_count=chunks_,
            archive_name=archive_name,
            file_count=len(file_paths),
            chunk_size_kb=self.chunk_size,
            storage_class=storage_class,
            is_encrypted=passwrod is not None,
            password_hint=password_hint or "",
        )
        init_payload = InitiateUploadPayloadModel(
            archive=archive_payload,
        )
        upload_urls: InitUploadResponseModel = await self.init_upload(payload=init_payload)

        hashes = await self.stream_file(upload_urls.archive, archive_path)
        os.remove(archive_path)
        print(hashes)
        await self.confirm_upload(
            payload=ConfirmUploadPayloadModel(
                uuid=upload_urls.uuid,
                archive_hashes={i.part_no: i.etag for i in hashes.tags},
            ),
        )