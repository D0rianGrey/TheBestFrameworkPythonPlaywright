"""
Простые тесты для демонстрации базовой функциональности Playwright
"""
from typing import List
import pytest
from playwright.sync_api import Page, expect
from fixtures import base_url, test_data, page_with_base_url, navigation_helper, element_checker


def test_open_the_internet_website(page_with_base_url: Page) -> None:
    """
    Simple test that opens the-internet.herokuapp.com website
    and verifies that the page loads correctly
    """
    # Page already navigated by fixture
    page = page_with_base_url
    
    # Verify the page title contains "The Internet"
    expect(page).to_have_title("The Internet")
    
    # Verify the main heading is visible
    expect(page.get_by_role("heading", name="Welcome to the-internet")).to_be_visible()
    
    # Verify that the examples list is present
    expect(page.locator("ul")).to_be_visible()
    
    # Verify that at least one example link is present (A/B Testing)
    expect(page.get_by_role("link", name="A/B Testing")).to_be_visible()


def test_check_page_elements(page_with_base_url: Page, test_data: dict, element_checker) -> None:
    """
    Test that checks specific elements on the-internet homepage using fixtures
    """
    page = page_with_base_url
    
    # Check that GitHub link is present (might be hidden)
    github_link = page.get_by_role("link", name="Fork me on GitHub")
    expect(github_link).to_be_attached()  # проверяем что элемент есть в DOM
    
    # Use element_checker fixture to verify main links
    element_checker.check_links_visible(test_data["main_links"])
    
    # Check that "Powered by Elemental Selenium" footer is present
    expect(page.locator("text=Powered by Elemental Selenium")).to_be_visible()


def test_navigate_to_ab_testing_page(navigation_helper, base_url: str) -> None:
    """
    Test that navigates to A/B Testing page using navigation helper fixture
    """
    # Use navigation helper to go to A/B Testing page
    navigation_helper.go_to_link("A/B Testing")
    
    # Verify we're on the A/B Testing page
    expect(navigation_helper.page).to_have_url(f"{base_url}abtest")
    
    # Verify the heading contains "A/B Test"
    heading = navigation_helper.page.get_by_role("heading")
    expect(heading).to_contain_text("A/B Test") 