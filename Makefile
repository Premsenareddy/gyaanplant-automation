# Run all tests
test:
	pytest

# Web smoke/regression tests
smoke:
	pytest -m "web and smoke"

# All web tests
web:
	pytest -m web

# Full regression
regression:
	pytest -m "web and regression"
