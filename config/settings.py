import os
from pathlib import Path
from pydantic import BaseModel

# Calculate the project root relative to this file
PROJECT_ROOT = Path(__file__).resolve().parents[1]

class AndroidConfig(BaseModel):
    platformName: str = os.getenv("ANDROID_PLATFORM_NAME", "Android")
    platformVersion: str = os.getenv("ANDROID_PLATFORM_VERSION", "14")
    deviceName: str = os.getenv("ANDROID_DEVICE_NAME", "Pixel14")
    automationName: str = os.getenv("ANDROID_AUTOMATION_NAME", "UiAutomator2")

    # Dynamically set the app path using PROJECT_ROOT
    app: str = str(PROJECT_ROOT / "app" / "gyaanplant.apk")
    
    appWaitActivity: str = os.getenv("ANDROID_APP_WAIT_ACTIVITY", "*")
    appium_server_url: str = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    no_reset: bool = os.getenv("ANDROID_NO_RESET", "false").lower() in ("1", "true", "yes")
    full_reset: bool = os.getenv("ANDROID_FULL_RESET", "false").lower() in ("1", "true", "yes")
    APP_PACKAGE: str = os.getenv("ANDROID_APP_PACKAGE", "com.example.gyaanplant_learning_app")
    APP_ACTIVITY: str = os.getenv("ANDROID_APP_ACTIVITY", ".MainActivity")


class AndroidTestUser(BaseModel):
    email: str = os.getenv("ANDROID_LMS_EMAIL", os.getenv("LMS_EMAIL", "maxy1@gmail.com"))
    password: str = os.getenv("ANDROID_LMS_PASSWORD", os.getenv("LMS_PASSWORD", "1234"))
    otp: str | None = os.getenv("ANDROID_LMS_OTP")


class WebConfig(BaseModel):
    base_url: str = os.getenv("LMS_BASE_URL", "https://lms.gyaanplant.co.in")
    dashboard_path: str = os.getenv("LMS_DASHBOARD_PATH", "/dashboard")
    browser: str = os.getenv("WEB_BROWSER", "chromium")
    browser_executable_path: str | None = os.getenv("WEB_BROWSER_EXECUTABLE_PATH")
    headless: bool = os.getenv("WEB_HEADLESS", "true").lower() in ("1", "true", "yes")
    timeout_ms: int = int(os.getenv("WEB_TIMEOUT_MS", "30000"))
    slow_mo_ms: int = int(os.getenv("WEB_SLOW_MO_MS", "0"))
