# Run all tests
test:
	pytest

# Smoke test (App launch)
smoke:
	pytest tests/android/test_smoke_launch.py

# Login flow
login:
	pytest tests/android/test_login_flow.py

# Profile + Resume flow
profile:
	pytest tests/android/test_profile_resume_flow.py

