"""HTTP client skeleton for the IceVault REST API."""

from __future__ import annotations

from types import TracebackType
from typing import Any

import httpx

from icevault._async.archives.archives import AsyncArchives
from icevault._async.storage.storage import AsyncStorage
from icevault.base_client import BaseClient
from icevault.enums import MethodEnum


class AsyncClient(BaseClient):
    """Asynchronous IceVault API client backed by ``httpx.AsyncClient``."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        **client_kwargs: Any,
    ) -> None:
        """Create an asynchronous client instance."""
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout)
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=self._build_headers(),
            timeout=self._timeout,
            **client_kwargs,
        )
        self.archives = AsyncArchives(self)
        self.storages = AsyncStorage(self)


    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def _execute_request(
        self,
        method: MethodEnum,
        path: str,
        **kwargs: Any
    ) -> Any:
        url = path.lstrip("/")
        headers = self._build_headers()
        response = await self._client.request(method.value, url, headers=headers, **kwargs)
        self._raise_for_status(response)
        return response


    async def _async_request_runner(self, method, path, target_model, **kwargs):
        response = await self._client.request(method.value, path.lstrip("/"), headers=self._build_headers(), **kwargs)
        response.raise_for_status()
        return target_model.model_validate(response.json())

    async def _async_stream_runner(self, method: MethodEnum, url: str, destination_path: str | None = None):
        """Asynchronous isolated stream for external URLs (S3/R2)."""
        headers = {"Accept-Encoding": "identity", "User-Agent": "icevault-python-sdk"}

        async with httpx.AsyncClient() as client:
            async with client.stream(method.value, url, headers=headers) as response:
                response.raise_for_status()

                if not destination_path:
                    return await response.aread()
                with open(destination_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=65536):
                        f.write(chunk)

                return destination_path