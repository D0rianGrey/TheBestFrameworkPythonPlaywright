# Playwright Python Tests for The Internet

This project contains simple Playwright tests written in Python for testing the website https://the-internet.herokuapp.com.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

## Running Tests

### Run all tests (with visible browser):
```bash
pytest
```

### Run tests in headless mode:
```bash
pytest --headless
```

### Run specific test:
```bash
pytest test_the_internet.py::test_open_the_internet_website
```

### Run tests on different browsers:
```bash
pytest --browser firefox
pytest --browser webkit
pytest --browser chromium
```

### Run tests by markers:
```bash
pytest -m smoke                    # Только smoke tests
pytest -m "smoke or regression"    # Smoke или regression
pytest -m "not slow"              # Исключить медленные тесты
pytest -m auth                     # Только authentication тесты
```

### Run specific test patterns:
```bash
pytest test_advanced_pytest.py::test_homepage_loads
pytest test_advanced_pytest.py::TestAuthentication
pytest -k "auth"                   # Все тесты содержащие "auth"
```

### Parametrized and rerun options:
```bash
pytest --reruns 3                  # Перезапуск упавших тестов
pytest --html=report.html          # HTML отчет
pytest -v --tb=short              # Подробный вывод
```

### Debug mode:
```bash
PWDEBUG=1 pytest -s
```

### Type checking:
```bash
mypy test_the_internet.py test_advanced_pytest.py
```

## Test Files

- `test_simple.py` - Basic test file containing:
  - `test_open_the_internet_website()` - Basic test that opens the website and verifies loading
  - `test_check_page_elements()` - Test that verifies specific elements on the homepage
  - `test_navigate_to_ab_testing_page()` - Test that navigates to A/B Testing page

- `test_with_fixtures.py` - **Demonstration of separated fixtures usage**:
  - `test_using_navigation_helper()` - Shows navigation_helper fixture usage
  - `test_using_element_checker()` - Shows element_checker fixture usage  
  - `test_parametrized_with_fixtures()` - Parametrized tests with fixtures
  - `TestFixturesIntegration` - Class showing multiple fixtures integration

- `tests/test_advanced_pytest.py` - Advanced pytest features demonstration:
  - **Markers**: @pytest.mark.smoke, @pytest.mark.regression, @pytest.mark.slow
  - **Parametrization**: @pytest.mark.parametrize for data-driven tests
  - **Test Classes**: TestAuthentication, TestDynamicContent for grouping
  - **Skip/XFail**: @pytest.mark.skip, @pytest.mark.xfail examples

- `fixtures.py` - **🎯 Separated fixtures file containing**:
  - `base_url` - Base URL for testing (session scope)
  - `test_data` - Test data dictionary with links and auth data
  - `page_with_base_url` - Page fixture pre-navigated to base URL
  - `navigation_helper` - Helper class for site navigation
  - `element_checker` - Helper class for element verification
  - `test_config` - Global test configuration (viewport, timeouts, etc.)
  - `test_setup_teardown` - Automatic setup/teardown for each test

- `conftest.py` - Global pytest configuration:
  - Custom marker registration
  - Global browser context settings
  - Automatic marker assignment
  - HTML report customization

## Configuration

- `pytest.ini` - Pytest configuration with default settings
- `mypy.ini` - MyPy configuration for type checking
- `requirements.txt` - Python dependencies 