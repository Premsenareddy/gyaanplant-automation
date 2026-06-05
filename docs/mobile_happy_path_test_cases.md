# GyaanPlant APK Mobile Happy Path Test Cases

## Scope

Platform: Android APK  
Automation stack: Python, Pytest, Appium, UiAutomator2  
Pattern: Page Object Model  
APK: `app/gyaanplant.apk`

## Credentials

Tests read mobile credentials from environment variables:

```bash
ANDROID_LMS_EMAIL=<email>
ANDROID_LMS_PASSWORD=<password>
ANDROID_LMS_OTP=<otp>   # only for OTP-based mobile accounts
```

If these are not set, the framework falls back to the existing mobile sample user.
If the APK shows an OTP screen and no OTP is supplied, post-login happy paths are skipped with an explicit auth-data message.

## Happy Path Test Cases

| Test ID | Component | Scenario | Expected Result |
|---|---|---|---|
| MOB-HP-001 | App Launch | Launch APK on Android device/emulator | App opens with expected package and main activity |
| MOB-HP-002 | Splash / Onboarding | Tap splash Start and progress onboarding | User reaches Login or an already-authenticated home state |
| MOB-HP-003 | Login | Login with valid mobile LMS credentials | Home screen loads successfully |
| MOB-HP-004 | Bottom Navigation | Navigate Home, Library, Assessment, Profile tabs | Each tab opens and displays expected labels/content |
| MOB-HP-005 | Profile Support Screens | Open Leaderboard, My Certificates, My Task from profile/settings | Each support screen loads or shows valid empty state |
| MOB-HP-006 | Courses | Open Library and available course card such as Rust | Course details/action screen opens |
| MOB-HP-007 | Assessment | Open Assessment tab | Assessment intro, quiz entry, or assessment screen content is visible |

## Execution Command

```bash
ANDROID_LMS_EMAIL=<email> ANDROID_LMS_PASSWORD=<password> pytest -m android tests/android/test_mobile_happy_paths.py -v
ANDROID_LMS_EMAIL=<email> ANDROID_LMS_OTP=<otp> pytest -m android tests/android/test_mobile_happy_paths.py -v
```

## Notes

- Tests avoid destructive profile edits by default.
- Tests use resilient text-based Appium locators where the APK does not expose stable resource IDs.
- For stronger long-term reliability, add Android accessibility IDs or resource IDs for navigation tabs, forms, and major buttons.
