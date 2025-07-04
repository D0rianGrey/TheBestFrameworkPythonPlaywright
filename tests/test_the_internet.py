from typing import List
import pytest
from playwright.sync_api import Page, expect

def test_open_the_internet_website(page: Page) -> None:
    """
    Simple test that opens the-internet.herokuapp.com website
    and verifies that the page loads correctly
    """
    # Navigate to the website
    page.goto("https://the-internet.herokuapp.com")
    
    # Verify the page title contains "The Internet"
    expect(page).to_have_title("The Internet")
    
    # Verify the main heading is visible
    expect(page.get_by_role("heading", name="Welcome to the-internet")).to_be_visible()
    
    # Verify that the examples list is present
    expect(page.locator("ul")).to_be_visible()
    
    # Verify that at least one example link is present (A/B Testing)
    expect(page.get_by_role("link", name="A/B Testing")).to_be_visible()


def test_check_page_elements(page: Page) -> None:
    """
    Test that checks specific elements on the-internet homepage
    """
    # Navigate to the website
    page.goto("https://the-internet.herokuapp.com")
    
    # Check that GitHub link is present (may be hidden, so check if it exists)
    expect(page.get_by_role("link", name="Fork me on GitHub")).to_be_attached()
    
    # Check that some of the example links are present
    example_links: List[str] = [
        "A/B Testing",
        "Add/Remove Elements", 
        "Basic Auth",
        "Checkboxes",
        "Form Authentication"
    ]
    
    for link_name in example_links:
        expect(page.get_by_role("link", name=link_name)).to_be_visible()
    
    # Check that "Powered by Elemental Selenium" footer is present
    expect(page.locator("text=Powered by Elemental Selenium")).to_be_visible()


def test_navigate_to_ab_testing_page(page: Page) -> None:
    """
    Test that navigates to A/B Testing page to verify functionality
    """
    # Navigate to the main website
    page.goto("https://the-internet.herokuapp.com")
    
    # Click on A/B Testing link
    page.get_by_role("link", name="A/B Testing").click()
    
    # Verify we're on the A/B Testing page
    expect(page).to_have_url("https://the-internet.herokuapp.com/abtest")
    
    # Verify the heading contains "A/B Test"
    heading = page.get_by_role("heading")
    expect(heading).to_contain_text("A/B Test") 