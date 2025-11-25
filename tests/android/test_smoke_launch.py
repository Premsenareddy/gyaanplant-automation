import time
from config.settings import AndroidConfig


def test_can_launch_gyaanplant(android_driver):
    cfg = AndroidConfig()

    time.sleep(5)

    current_package = android_driver.current_package
    current_activity = android_driver.current_activity

    print(f"\nCurrent Package  : {current_package}")
    print(f"Current Activity : {current_activity}\n")

    assert current_package == cfg.APP_PACKAGE
    assert current_activity == cfg.APP_ACTIVITY

