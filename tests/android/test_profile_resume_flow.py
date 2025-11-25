# tests/android/test_profile_resume_flow.py

from pages.android.profile_page import ProfilePage
from pages.android.settings_page import SettingsPage
from pages.android.my_profile_page import MyProfilePage
from pages.android.my_resume_page import MyResumePage

def test_update_profile_and_export_resume(android_driver):
    profile = ProfilePage(android_driver)
    settings = SettingsPage(android_driver)
    my_profile = MyProfilePage(android_driver)
    my_resume = MyResumePage(android_driver)

    # Open Settings from Profile tab
    profile.open_settings()

    # Update profile info
    settings.open_my_profile()

    my_profile.update_fullname("Abraham QA")
    my_profile.update_mobile("9876543210")
    my_profile.update_email("abraham.qa@gmail.com")
    my_profile.save()

    # Now resume
    settings.open_my_resume()

    my_resume.click_edit()
    my_resume.update_address("Dubai, UAE")
    my_resume.update_dob("1990-05-15")
    my_resume.save_resume()

    # Export (file dialog expected)
    my_resume.export_resume()

