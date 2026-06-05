# GyaanPlant APK Mobile Automation Execution Report

## Summary

Date: 2026-06-02  
Platform: Android emulator `emulator-5554`  
Automation: Python, Pytest, Appium, UiAutomator2  
APK: `app/gyaanplant.apk`  
Suite: `tests/android/test_mobile_happy_paths.py`

## Latest Execution Result

Command:

```bash
ANDROID_DEVICE_NAME=emulator-5554 ANDROID_PLATFORM_VERSION=14 .venv/bin/python -m pytest tests/android/test_mobile_happy_paths.py -v
```

Result:

```text
2 passed, 5 skipped in 250.73s (0:04:10)
```

## Executed Test Cases

| Test ID | Automated Test | Status | Notes |
|---|---|---|---|
| MOB-HP-001 | App launches to expected package/activity | Passed | APK opened as `com.example.gyaanplant_learning_app` |
| MOB-HP-002 | Splash and onboarding reach login/home | Passed | Start, onboarding Next flow, and Login navigation worked |
| MOB-HP-003 | Valid user can login and view Home | Skipped | Default mobile credentials reached password screen but did not reach Home |
| MOB-HP-004 | Bottom navigation tabs are accessible | Skipped | Requires successful mobile login |
| MOB-HP-005 | Settings/support pages are accessible | Skipped | Requires successful mobile login |
| MOB-HP-006 | Courses flow opens an available course | Skipped | Requires successful mobile login |
| MOB-HP-007 | Assessment tab or intro loads | Skipped | Requires successful mobile login |

## Authentication Findings

- Default sample mobile credentials `maxy1@gmail.com / 1234` reached the password screen, but did not transition to Home after Continue.
- Website admin credentials `admin@gyaanplant.com / 12345678` did not follow the password path in the APK. The APK displayed an OTP screen after email submit.
- The framework now supports OTP-based login through `ANDROID_LMS_OTP`.

## Required To Execute Full Post-Login Suite

Provide one of these:

- A valid APK/mobile user email and password that reaches the Home screen.
- An OTP-enabled account plus a current OTP value using `ANDROID_LMS_OTP`.
- A stable test-only OTP bypass or fixed OTP in the QA environment.

Example password-account run:

```bash
ANDROID_DEVICE_NAME=emulator-5554 ANDROID_PLATFORM_VERSION=14 \
ANDROID_LMS_EMAIL=<mobile_user_email> \
ANDROID_LMS_PASSWORD=<mobile_user_password> \
.venv/bin/python -m pytest tests/android/test_mobile_happy_paths.py -v
```

Example OTP-account run:

```bash
ANDROID_DEVICE_NAME=emulator-5554 ANDROID_PLATFORM_VERSION=14 \
ANDROID_LMS_EMAIL=<otp_user_email> \
ANDROID_LMS_OTP=<current_otp> \
.venv/bin/python -m pytest tests/android/test_mobile_happy_paths.py -v
```

## Automation Updates Completed

- Added Android environment-driven config for device, Appium server, reset behavior, credentials, and OTP.
- Added robust BasePage helper methods used by Android POMs.
- Fixed onboarding timeout handling.
- Added login submit retry/center-tap fallback for focus-sensitive APK buttons.
- Added OTP detection and OTP entry support.
- Added auth-aware skips so blocked post-login tests are reported clearly instead of failing as locator errors.
- Added the mobile happy-path test suite and test-case documentation.

