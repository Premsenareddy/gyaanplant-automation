from pydantic import BaseModel

class AndroidConfig(BaseModel):
    platformName: str = "Android"
    platformVersion: str = "14"          # Use Android 14
    deviceName: str = "Pixel14"          # Your new AVD name
    automationName: str = "UiAutomator2"

    app: str = "/Users/premsenareddy/gyaanplant_automation/app/gyaanplant.apk"
    appWaitActivity: str = "*"

    APP_PACKAGE: str = "com.example.gyaanplant_learning_app"
    APP_ACTIVITY: str = ".MainActivity"

