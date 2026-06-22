from __future__ import annotations

from dataclasses import dataclass

import requests

from config.settings import WebConfig


@dataclass
class CleanupResult:
    module: str
    prefix: str
    enabled: bool
    status_code: int | None = None
    message: str = ""


class WebApiClient:
    """Small API client for automation-owned test data.

    The client is intentionally inert unless LMS_API_BASE_URL and LMS_API_TOKEN
    are configured. Dev teams can expose compatible cleanup endpoints without
    changing UI tests.
    """

    def __init__(self, config: WebConfig | None = None):
        self.config = config or WebConfig()
        self.base_url = (self.config.api_base_url or "").rstrip("/")
        self.token = self.config.api_token

    @property
    def enabled(self):
        return bool(self.base_url and self.token)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def cleanup_by_prefix(self, module: str, prefix: str = "AUTO_WEB") -> CleanupResult:
        if not self.enabled:
            return CleanupResult(
                module=module,
                prefix=prefix,
                enabled=False,
                message="LMS_API_BASE_URL/LMS_API_TOKEN not configured.",
            )

        endpoint = f"{self.base_url}/automation/cleanup/{module}"
        response = requests.delete(
            endpoint,
            headers=self._headers(),
            params={"prefix": prefix},
            timeout=30,
        )
        return CleanupResult(
            module=module,
            prefix=prefix,
            enabled=True,
            status_code=response.status_code,
            message=response.text[:500],
        )

    def seed(self, fixture_name: str):
        if not self.enabled:
            return CleanupResult(
                module=fixture_name,
                prefix="",
                enabled=False,
                message="LMS_API_BASE_URL/LMS_API_TOKEN not configured.",
            )

        endpoint = f"{self.base_url}/automation/seed"
        response = requests.post(
            endpoint,
            headers=self._headers(),
            json={"fixture": fixture_name},
            timeout=30,
        )
        return CleanupResult(
            module=fixture_name,
            prefix="",
            enabled=True,
            status_code=response.status_code,
            message=response.text[:500],
        )
