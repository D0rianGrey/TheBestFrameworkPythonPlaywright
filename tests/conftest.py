import pytest
from typing import Dict, Any
import os
import sys
from pathlib import Path
from playwright.sync_api import Browser, BrowserContext, Page

# Добавляем корневую директорию проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_manager import get_config


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


def pytest_addoption(parser):
    """Добавляем опции командной строки"""
    parser.addoption(
        "--remote-browser",
        action="store",
        default=None,
        help="URL удаленного браузера (например: ws://192.168.195.104:9222)"
    )
    parser.addoption(
        "--browser-name",
        action="store", 
        default="chromium",
        help="Имя браузера: chromium, firefox, webkit"
    )
    parser.addoption(
        "--test-mode",
        action="store",
        choices=["local", "remote"],
        default=None,
        help="Режим тестирования: local или remote"
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig):
    """Аргументы для запуска браузера"""
    # Проверяем командную строку
    remote_url = pytestconfig.getoption("--remote-browser")
    test_mode = pytestconfig.getoption("--test-mode")
    
    # Устанавливаем режим из командной строки если передан
    if test_mode:
        os.environ['TEST_MODE'] = test_mode
    
    config = get_config()
    
    # Показываем текущую конфигурацию
    print(f"\n🔧 Test Configuration:")
    print(f"   Mode: {config.get_test_mode()}")
    if config.is_remote_mode():
        print(f"   Remote URL: {config.get_remote_url()}")
    
    if remote_url or config.is_remote_mode():
        # Для удаленного режима возвращаем пустой dict
        # Подключение к удаленному браузеру будет через browser fixture
        return {}
    else:
        # Для локального режима используем стандартные аргументы
        local_settings = config.config['local_settings']
        return {
            "headless": local_settings.get('headless', False),
            "slow_mo": local_settings.get('slow_mo', 100)
        }


@pytest.fixture(scope="session")
def browser(browser_type, browser_type_launch_args, pytestconfig):
    """Кастомная фикстура браузера с поддержкой удаленного подключения"""
    # Проверяем командную строку и конфигурацию
    remote_url = pytestconfig.getoption("--remote-browser")
    config = get_config()
    
    if remote_url:
        # Прямое указание URL удаленного браузера
        print(f"   Connecting to remote browser: {remote_url}")
        # Для CDP подключения используем connect_over_cdp
        if remote_url.startswith('ws://') and '/devtools/' in remote_url:
            browser = browser_type.connect_over_cdp(remote_url)
        else:
            browser = browser_type.connect(ws_endpoint=remote_url)
    elif config.is_remote_mode():
        # Используем конфигурацию для удаленного подключения
        remote_ws_url = config.get_remote_url()
        print(f"   Connecting to remote browser: {remote_ws_url}")
        # Для CDP подключения используем connect_over_cdp
        if remote_ws_url.startswith('ws://') and '/devtools/' in remote_ws_url:
            browser = browser_type.connect_over_cdp(remote_ws_url)
        else:
            browser = browser_type.connect(ws_endpoint=remote_ws_url)
    else:
        # Локальный режим - стандартный запуск
        browser = browser_type.launch(**browser_type_launch_args)
    
    yield browser
    # Для удаленного браузера не закрываем browser
    if not (remote_url or config.is_remote_mode()):
        browser.close()


@pytest.fixture(scope="session") 
def context_args():
    """Аргументы для контекста браузера"""
    config = get_config()
    context_args = config.get_context_args()
    
    # Добавляем user agent
    context_args["user_agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    return context_args


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Автоматическая настройка тестового окружения"""
    # Можно добавить логирование, настройки прокси и т.д.
    print("\n🔧 Setting up test environment...")
    yield
    print("🧹 Cleaning up test environment...") 