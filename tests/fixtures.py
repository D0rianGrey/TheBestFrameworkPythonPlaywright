"""
Фикстуры для тестов Playwright
"""
from typing import Dict, List, Generator, Any
import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def base_url() -> str:
    """Базовый URL для тестирования"""
    return "https://the-internet.herokuapp.com/"


@pytest.fixture 
def test_data() -> Dict[str, Any]:
    """Тестовые данные для проверок"""
    return {
        "main_links": [
            "A/B Testing",
            "Add/Remove Elements", 
            "Checkboxes",
            "Form Authentication"
        ],
        "auth_data": ["admin", "admin"],  # username, password
        "expected_urls": {
            "A/B Testing": "/abtest",
            "Add/Remove Elements": "/add_remove_elements", 
            "Basic Auth": "/basic_auth",
            "Checkboxes": "/checkboxes",
            "Form Authentication": "/login"
        }
    }


@pytest.fixture
def page_with_base_url(page: Page, base_url: str) -> Page:
    """Страница с предустановленным базовым URL"""
    page.goto(base_url)
    return page


@pytest.fixture(autouse=True)
def test_setup_teardown(page: Page) -> Generator[None, None, None]:
    """Автоматическая фикстура для setup/teardown каждого теста"""
    # Setup - выполняется перед каждым тестом
    print(f"\n🚀 Starting test on page: {page.url if hasattr(page, 'url') else 'Not navigated yet'}")
    
    yield  # Здесь выполняется тест
    
    # Teardown - выполняется после каждого теста  
    print(f"✅ Test completed on page: {page.url}")


@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """Глобальная конфигурация для тестов"""
    return {
        "timeout": 10000,
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Automated Test Bot)",
        "screenshots_dir": "screenshots",
        "video_dir": "videos"
    }


@pytest.fixture
def navigation_helper(page: Page, base_url: str):
    """Помощник для навигации"""
    class NavigationHelper:
        def __init__(self, page: Page, base_url: str):
            self.page = page
            self.base_url = base_url
            
        def go_to_main(self) -> None:
            """Переход на главную страницу"""
            self.page.goto(self.base_url)
            
        def go_to_link(self, link_name: str) -> None:
            """Переход по ссылке на главной странице"""
            self.go_to_main()
            self.page.get_by_role("link", name=link_name).click()
            
        def go_back_to_main(self) -> None:
            """Возврат на главную страницу"""
            self.page.go_back()
            
    return NavigationHelper(page, base_url)


@pytest.fixture
def element_checker(page: Page):
    """Помощник для проверки элементов"""
    class ElementChecker:
        def __init__(self, page: Page):
            self.page = page
            
        def check_links_visible(self, link_names: List[str]) -> bool:
            """Проверка видимости списка ссылок"""
            from playwright.sync_api import expect
            
            for link_name in link_names:
                expect(self.page.get_by_role("link", name=link_name)).to_be_visible()
            return True
            
        def check_page_title(self, expected_title: str) -> bool:
            """Проверка заголовка страницы"""
            from playwright.sync_api import expect
            
            expect(self.page).to_have_title(expected_title)
            return True
            
        def check_url_contains(self, url_part: str) -> bool:
            """Проверка что URL содержит определенную часть"""
            assert url_part in self.page.url, f"URL '{self.page.url}' does not contain '{url_part}'"
            return True
            
    return ElementChecker(page) 