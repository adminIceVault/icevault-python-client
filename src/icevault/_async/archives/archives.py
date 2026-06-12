from __future__ import annotations

from uuid import UUID
from icevault.archives.endpoints import ArchiveUrls
from icevault.archives.models import (
    GetArchiveFileter,
    ArchiveResponseModel,
    PreviewResponseModel, \
    RestoreArchiveResponseModel,
    DownloadResponseModel,
    ArchiveModel,
    UpdateArchiveModel,
)
from icevault.enums import MethodEnum
import typing
if typing.TYPE_CHECKING:
    from icevault._async.async_client import AsyncClient



class AsyncArchives:
    def __init__(self, client: AsyncClient) -> None:
        self.client: AsyncClient = client

    async def filter(self, archive_filter: GetArchiveFileter | dict | None = None) -> ArchiveResponseModel:
        """Fetch and parse filtered archives list."""
        if archive_filter is None:
            archive_filter = GetArchiveFileter()
        elif isinstance(archive_filter, dict):
            archive_filter = GetArchiveFileter(**archive_filter)

        params = archive_filter.model_dump(exclude_none=True)
        response = await self.client._execute_request(
            method=MethodEnum.GET,
            path=ArchiveUrls.filter.get_url(),
            params=params
        )

        return ArchiveResponseModel.model_validate(response.json())

    async def preview_url(self, uuid: UUID) -> str:
        """
        Generate url for download preview
        :param uuid:
        :return:
        """
        response = await self.client._execute_request(
            method=MethodEnum.GET,
            path=ArchiveUrls.preview.get_url(uuid=uuid),
            params={},
        )
        return PreviewResponseModel.model_validate(response.json())

    async def download_preview(self, uuid: UUID, destination_path: str) -> None:
        """Download preview for given uuid"""
        preview_response = await self.preview_url(uuid=uuid)
        return await self.client._async_stream_runner(
            method=MethodEnum.GET,
            url=preview_response.url,
            destination_path=destination_path
        )

    async def restore(self, uuid: UUID) -> RestoreArchiveResponseModel:
        """
        Generate url for download preview
        :param uuid:
        :return:
        """
        response = await self.client._execute_request(
            method=MethodEnum.GET,
            path=ArchiveUrls.restore.get_url(uuid=uuid),
            params={},
        )
        return RestoreArchiveResponseModel.model_validate(response.json())

    async def get_download_url(self, uuid: UUID) -> DownloadResponseModel:
        """Fetch the pre-signed download configuration."""
        response = await self.client._execute_request(
            method=MethodEnum.GET,
            path=ArchiveUrls.download.get_url(uuid=uuid)
        )
        return DownloadResponseModel.model_validate(response.json())

    async def download(self, uuid: UUID, destination_path: str | None = None) -> typing.Any:
        """
        Download file payloads securely.
        Automatically respects Sync/Async runtime architecture.
        """
        file_info = await self.get_download_url(uuid)

        return await self.client._async_stream_runner(
            method=MethodEnum.GET,
            url=file_info.url,
            destination_path=destination_path
        )

    async def delete(self, uuid: UUID) -> None:
        """Delete file payloads securely."""
        response = await self.client._execute_request(
            method=MethodEnum.DELETE,
            path=ArchiveUrls.delete.get_url(uuid=uuid)
        )

    async def update_archive(
        self,
        uuid: UUID,
        model=UpdateArchiveModel,
    ) -> ArchiveModel:
        """Update archive payloads securely."""
        response = await self.client._execute_request(
            method=MethodEnum.PATCH,
            path=ArchiveUrls.patch.get_url(uuid=uuid),
            params=model.model_dump(exclude_none=True),

        )
        return ArchiveModel.model_validate(response.json())

    async def cancel_deletion(
        self,
        uuid: UUID,
    ) -> ArchiveModel:
        """Update archive payloads securely."""
        response = await self.client._execute_request(
            method=MethodEnum.POST,
            path=ArchiveUrls.cancel_deletion.get_url(uuid=uuid),
        )
        return ArchiveModel.model_validate(response.json())