from __future__ import annotations

import httpx
from icevault.constants import DEBUG
from icevault.exceptions import IceVaultError


class BaseClient:
    """Shared configuration and helpers for IceVault API clients."""

    DEFAULT_BASE_URL = "https://icevault.space/"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        """Initialize shared client settings.

        Args:
            api_key: Bearer token or API key used to authenticate requests.
            base_url: Override the default IceVault API base URL.
            timeout: Request timeout in seconds.
        """
        self._api_key = api_key
        self._base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout

    @property
    def base_url(self) -> str:
        """Return the configured API base URL."""
        return self._base_url

    def _build_headers(self, is_external: bool = False) -> dict[str, str]:
        """Build default request headers."""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "icevault-python-sdk",
        }
        if self._api_key is not None and not is_external:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Translate non-success HTTP responses into SDK errors."""
        if response.is_success:
            return

        response.read()
        if DEBUG:
            print("--- S3 XML ERROR DETAIL ---")
            print(response.text)
            print("---------------------------")

        raise IceVaultError(
            f"Request failed with status {response.status_code}",
            status_code=response.status_code,
            response_body=response.text,
        )
