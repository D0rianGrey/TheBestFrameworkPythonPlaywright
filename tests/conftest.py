import pytest
from typing import Dict, Any


def pytest_configure(config: pytest.Config) -> None:
    """Конфигурация pytest - регистрируем кастомные маркеры"""
    config.addinivalue_line("markers", "smoke: quick smoke tests for basic functionality")
    config.addinivalue_line("markers", "regression: comprehensive regression test suite")  
    config.addinivalue_line("markers", "slow: slow running tests (> 30 seconds)")
    config.addinivalue_line("markers", "flaky: potentially unstable tests")
    config.addinivalue_line("markers", "auth: authentication related tests")
    config.addinivalue_line("markers", "ui: user interface tests")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict[str, Any]) -> Dict[str, Any]:
    """Глобальные настройки браузерного контекста для всех тестов"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Test Automation Bot)",
        "locale": "en-US",
        "timezone_id": "America/New_York"
    }


# base_url фикстура перенесена в fixtures.py


def pytest_collection_modifyitems(config: pytest.Config, items: list) -> None:
    """Модификация собранных тестов - добавляем маркеры автоматически"""
    for item in items:
        # Автоматически добавляем маркер 'ui' для всех тестов
        item.add_marker(pytest.mark.ui)
        
        # Добавляем маркер 'slow' для тестов содержащих 'slow' в названии
        if "slow" in item.name.lower():
            item.add_marker(pytest.mark.slow)
            
        # Добавляем маркер 'auth' для тестов в классе TestAuthentication
        if item.cls and "Authentication" in item.cls.__name__:
            item.add_marker(pytest.mark.auth)


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells) -> None:
    """Кастомизация заголовков HTML отчета"""
    cells.insert(2, "<th>Description</th>")


@pytest.hookimpl(optionalhook=True) 
def pytest_html_results_table_row(report, cells) -> None:
    """Кастомизация строк HTML отчета"""
    cells.insert(2, f"<td>{getattr(report, 'description', '')}</td>") 