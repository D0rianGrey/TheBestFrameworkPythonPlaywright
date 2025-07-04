"""
Продвинутые примеры использования pytest с Playwright
Демонстрация маркеров, параметризации, классов тестов
"""
from typing import List, Generator
import pytest
from playwright.sync_api import Page, expect, BrowserContext, Browser
from fixtures import base_url, test_data


# ===============================
# PYTEST MARKERS (Маркеры для группировки)
# ===============================

@pytest.mark.smoke
def test_homepage_loads(page: Page, base_url: str) -> None:
    """Smoke test - быстрая проверка что сайт работает"""
    page.goto(base_url)
    expect(page).to_have_title("The Internet")


@pytest.mark.regression
def test_all_main_links_present(page: Page, base_url: str, test_data: dict) -> None:
    """Regression test - проверка всех основных ссылок"""
    page.goto(base_url)
    
    for link_name in test_data["main_links"]:
        expect(page.get_by_role("link", name=link_name)).to_be_visible()


@pytest.mark.slow
def test_navigation_through_all_pages(page: Page, base_url: str, test_data: dict) -> None:
    """Медленный тест - проходим по всем страницам"""
    page.goto(base_url)
    
    for link_name in test_data["main_links"]:
        # Кликаем по ссылке
        page.get_by_role("link", name=link_name).click()
        
        # Проверяем что попали на новую страницу
        expect(page).not_to_have_url(base_url)
        
        # Возвращаемся назад
        page.go_back()
        expect(page).to_have_url(base_url)


# ===============================
# PARAMETRIZED TESTS (Параметризованные тесты)
# ===============================

@pytest.mark.parametrize("link_name,expected_url_part", [
    ("A/B Testing", "/abtest"),
    ("Add/Remove Elements", "/add_remove_elements/"),
    ("Checkboxes", "/checkboxes"),
    ("Form Authentication", "/login")
])
def test_navigation_parametrized(page: Page, base_url: str, link_name: str, expected_url_part: str) -> None:
    """Параметризованный тест навигации"""
    page.goto(base_url)
    
    page.get_by_role("link", name=link_name).click()
    
    # Убираем слеш из base_url если expected_url_part начинается со слеша
    expected_url = f"{base_url.rstrip('/')}{expected_url_part}"
    expect(page).to_have_url(expected_url)


def test_basic_auth_navigation(page: Page, base_url: str) -> None:
    """Отдельный тест для Basic Auth - требует специальной обработки"""
    page.goto(base_url)
    
    # Кликаем по ссылке Basic Auth
    page.get_by_role("link", name="Basic Auth").click()
    
    # Для Basic Auth ожидаем что браузер покажет диалог аутентификации
    # или перенаправит на страницу с ошибкой, что является нормальным поведением
    # Проверяем что URL изменился (не равен базовому)
    expect(page).not_to_have_url(base_url)


def test_cross_browser_compatibility_manual(playwright) -> None:
    """Кросс-браузерное тестирование (ручной запуск)"""
    # Тестируем только chromium чтобы избежать конфликта с параметризацией playwright плагина
    browser = playwright.chromium.launch()
    page = browser.new_page()
    
    page.goto("https://the-internet.herokuapp.com")
    expect(page).to_have_title("The Internet")
    
    browser.close()


# ===============================
# TEST CLASSES (Группировка тестов в классы)
# ===============================

class TestAuthentication:
    """Группа тестов для аутентификации"""
    
    def test_basic_auth_link_exists(self, page: Page, base_url: str) -> None:
        """Проверка существования ссылки Basic Auth на главной странице"""
        page.goto(base_url)
        # Проверяем что ссылка Basic Auth присутствует на главной странице
        expect(page.get_by_role("link", name="Basic Auth")).to_be_visible()
        
    def test_form_auth_page_elements(self, page: Page, base_url: str) -> None:
        """Проверка элементов формы аутентификации"""
        page.goto(f"{base_url.rstrip('/')}/login")
        
        # Проверяем наличие полей формы
        expect(page.get_by_label("Username")).to_be_visible()
        expect(page.get_by_label("Password")).to_be_visible()
        expect(page.get_by_role("button", name="Login")).to_be_visible()


class TestDynamicContent:
    """Группа тестов для динамического контента"""
    
    @pytest.mark.flaky(reruns=3)  # Повторяем нестабильные тесты
    def test_dynamic_loading(self, page: Page, base_url: str) -> None:
        """Тест динамической загрузки"""
        page.goto(f"{base_url.rstrip('/')}/dynamic_loading")
        expect(page.get_by_text("Dynamically Loaded Page Elements")).to_be_visible()
        
    def test_disappearing_elements(self, page: Page, base_url: str) -> None:
        """Тест исчезающих элементов"""
        page.goto(f"{base_url.rstrip('/')}/disappearing_elements")
        # Элементы могут появляться и исчезать


# ===============================
# SKIP и XFAIL примеры
# ===============================

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature(page: Page) -> None:
    """Тест будущей функциональности"""
    pass


@pytest.mark.xfail(reason="Known issue with this browser")
def test_known_failing_case(page: Page, base_url: str) -> None:
    """Тест который ожидаемо падает"""
    page.goto(base_url)
    expect(page).to_have_title("Wrong Title")  # Этот тест упадет


# ===============================
# CUSTOM MARKERS определены в conftest.py
# =============================== 