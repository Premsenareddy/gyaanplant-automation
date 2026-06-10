import os
from pydantic import BaseModel


class WebConfig(BaseModel):
    base_url: str = os.getenv("LMS_BASE_URL", "https://lms.gyaanplant.co.in")
    dashboard_path: str = os.getenv("LMS_DASHBOARD_PATH", "/dashboard")
    browser: str = os.getenv("WEB_BROWSER", "chromium")
    browser_executable_path: str | None = os.getenv("WEB_BROWSER_EXECUTABLE_PATH")
    headless: bool = os.getenv("WEB_HEADLESS", "true").lower() in ("1", "true", "yes")
    timeout_ms: int = int(os.getenv("WEB_TIMEOUT_MS", "30000"))
    slow_mo_ms: int = int(os.getenv("WEB_SLOW_MO_MS", "0"))
    viewport_width: int = int(os.getenv("WEB_VIEWPORT_WIDTH", "1440"))
    viewport_height: int = int(os.getenv("WEB_VIEWPORT_HEIGHT", "1000"))
    test_id_attribute: str = os.getenv("WEB_TEST_ID_ATTRIBUTE", "data-testid")
    trace_mode: str = os.getenv("WEB_TRACE_MODE", "retain-on-failure")
    record_video: bool = os.getenv("WEB_RECORD_VIDEO", "false").lower() in ("1", "true", "yes")
    artifacts_dir: str = os.getenv("WEB_ARTIFACTS_DIR", "reports/web")
