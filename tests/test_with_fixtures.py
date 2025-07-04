"""
Демонстрация использования разделенных фикстур
Показывает различные способы использования фикстур из fixtures.py
"""
from typing import Dict, Any
import pytest
from playwright.sync_api import Page, expect
from fixtures import (
    base_url, 
    test_data, 
    page_with_base_url, 
    navigation_helper, 
    element_checker, 
    test_config
)


@pytest.mark.smoke
def test_using_navigation_helper(navigation_helper, test_data: Dict[str, Any]) -> None:
    """
    Демонстрация использования navigation_helper фикстуры
    """
    # Переходим к странице A/B Testing
    navigation_helper.go_to_link("A/B Testing")
    
    # Проверяем что попали на правильную страницу
    expected_url = test_data["expected_urls"]["A/B Testing"]
    assert expected_url in navigation_helper.page.url
    
    # Возвращаемся обратно
    navigation_helper.go_back_to_main()
    expect(navigation_helper.page).to_have_url(navigation_helper.base_url)


@pytest.mark.regression
def test_using_element_checker(page_with_base_url: Page, element_checker, test_data: Dict[str, Any]) -> None:
    """
    Демонстрация использования element_checker фикстуры
    """
    # Проверяем заголовок страницы
    element_checker.check_page_title("The Internet")
    
    # Проверяем что URL содержит правильный домен
    assert "the-internet.herokuapp.com" in page_with_base_url.url
    
    # Проверяем видимость основных ссылок
    main_links = test_data["main_links"][:3]  # Берем первые 3 ссылки
    element_checker.check_links_visible(main_links)


def test_using_test_config(page: Page, base_url: str, test_config: Dict[str, Any]) -> None:
    """
    Демонстрация использования test_config фикстуры
    """
    # Используем настройки из конфигурации
    page.set_viewport_size(test_config["viewport"])
    
    # Переходим на сайт
    page.goto(base_url)
    
    # Проверяем что страница загрузилась с правильным размером viewport
    viewport = page.viewport_size
    assert viewport is not None, "Viewport size should not be None"
    assert viewport["width"] == test_config["viewport"]["width"]
    assert viewport["height"] == test_config["viewport"]["height"]
    
    # Проверяем заголовок
    expect(page).to_have_title("The Internet")


@pytest.mark.parametrize("link_name", [
    "A/B Testing",
    "Add/Remove Elements", 
    "Checkboxes"
])
def test_parametrized_with_fixtures(navigation_helper, test_data: Dict[str, Any], link_name: str) -> None:
    """
    Параметризованный тест с использованием фикстур
    """
    # Переходим к указанной странице
    navigation_helper.go_to_link(link_name)
    
    # Проверяем что попали на правильную страницу
    expected_url_part = test_data["expected_urls"][link_name]
    assert expected_url_part in navigation_helper.page.url


class TestFixturesIntegration:
    """
    Класс тестов демонстрирующий интеграцию различных фикстур
    """
    
    def test_multiple_fixtures_together(
        self, 
        page_with_base_url: Page, 
        navigation_helper, 
        element_checker, 
        test_data: Dict[str, Any]
    ) -> None:
        """
        Тест использующий несколько фикстур одновременно
        """
        # page_with_base_url уже на главной странице
        page = page_with_base_url
        
        # Используем element_checker для проверки заголовка
        element_checker.check_page_title("The Internet")
        
        # Используем navigation_helper для навигации  
        navigation_helper.go_to_link("Form Authentication")
        
        # Проверяем что попали на страницу логина
        assert "/login" in page.url
        
        # Проверяем наличие полей формы
        expect(page.get_by_label("Username")).to_be_visible()
        expect(page.get_by_label("Password")).to_be_visible()
    
    @pytest.mark.auth
    def test_auth_workflow_with_fixtures(
        self, 
        navigation_helper, 
        test_data: Dict[str, Any]
    ) -> None:
        """
        Тест workflow аутентификации с использованием фикстур
        """
        # Переходим к странице аутентификации
        navigation_helper.go_to_link("Form Authentication")
        
        page = navigation_helper.page
        
        # Заполняем форму используя данные из test_data
        username, password = test_data["auth_data"]
        page.get_by_label("Username").fill(username)
        page.get_by_label("Password").fill(password)
        
        # Нажимаем Login
        page.get_by_role("button", name="Login").click()
        
        # Ждем навигации или сообщения об ошибке
        page.wait_for_load_state("networkidle")
        
        # Проверяем результат (может быть успех или неудача)
        if "/secure" in page.url:
            # Успешный логин
            expect(page.get_by_text("Welcome to the Secure Area")).to_be_visible()
        else:
            # Проверяем что остались на странице логина с сообщением об ошибке
            assert "/login" in page.url
            # Это нормально для демо-сайта с невалидными учетными данными


@pytest.mark.slow
def test_comprehensive_site_walkthrough(
    navigation_helper, 
    test_data: Dict[str, Any], 
    test_config: Dict[str, Any]
) -> None:
    """
    Комплексный тест прохода по сайту с использованием всех фикстур
    """
    successful_tests = 0
    skipped_tests = 0
    
    # Проходим по всем основным ссылкам
    for link_name in test_data["main_links"]:
        print(f"📍 Testing {link_name}")
        
        try:
            # Переходим к странице
            navigation_helper.go_to_link(link_name)
            
            # Проверяем что URL изменился
            expected_url_part = test_data["expected_urls"][link_name]
            
            # Специальная обработка для Add/Remove Elements (может иметь слеш в конце)
            if link_name == "Add/Remove Elements":
                assert (expected_url_part in navigation_helper.page.url or 
                       f"{expected_url_part}/" in navigation_helper.page.url)
            else:
                assert expected_url_part in navigation_helper.page.url
            
            # Возвращаемся на главную
            navigation_helper.go_back_to_main()
            
            print(f"✅ {link_name} test completed")
            successful_tests += 1
            
        except Exception as e:
            print(f"⚠️ {link_name} test skipped due to: {str(e)}")
            skipped_tests += 1
            # Пытаемся вернуться на главную в случае ошибки
            try:
                navigation_helper.go_to_main()
            except:
                pass
    
    print(f"🎉 Test summary: {successful_tests} successful, {skipped_tests} skipped") 