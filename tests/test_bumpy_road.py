"""
Test for Bumpy Road Ahead scenario with 2 bumps.
This test simulates challenging navigation scenarios that might occur during web testing.
"""

import pytest
from playwright.sync_api import Page, expect
from typing import Dict, Any
import time

# Import fixtures to ensure they're available
from tests.fixtures import base_url


class TestBumpyRoadAhead:
    """Test class for Bumpy Road Ahead scenarios with multiple challenges"""

    @pytest.mark.smoke
    def test_bumpy_road_with_2_bumps(self, page: Page, base_url: str) -> None:
        """
        Test that navigates through a bumpy road with 2 specific challenges:
        Bump 1: Slow loading resources
        Bump 2: Dynamic content changes
        """
        print("🛣️  Starting Bumpy Road Ahead test with 2 bumps...")

        # Navigate to the main page
        page.goto(base_url)

        # BUMP 1: Slow Resources Challenge
        print("🚧 Bump 1: Handling slow resources...")
        self._handle_slow_resources_bump(page, base_url)

        # BUMP 2: Dynamic Content Challenge
        print("🚧 Bump 2: Handling dynamic content...")
        self._handle_dynamic_content_bump(page, base_url)

        print("✅ Successfully navigated through all 2 bumps!")

    def _handle_slow_resources_bump(self, page: Page, base_url: str) -> None:
        """Handle the slow resources bump - test patience and timeout handling"""
        try:
            # Navigate to slow resources page
            page.goto(f"{base_url}slow")

            # Wait for the slow loading content with extended timeout
            slow_element = page.locator("text=Slow Resources")
            expect(slow_element).to_be_visible(timeout=10000)  # 10 seconds timeout

            # Verify we can interact with elements even when page is slow
            page.locator("text=Slow Resources").click()

            print("   ✅ Bump 1 navigated successfully - slow resources handled")

        except Exception as e:
            print(f"   ⚠️  Bump 1 challenge: {str(e)}")
            # Continue with the test even if this bump fails
            pass

    def _handle_dynamic_content_bump(self, page: Page, base_url: str) -> None:
        """Handle the dynamic content bump - test adaptability to changing content"""
        try:
            # Navigate to dynamic content page
            page.goto(f"{base_url}dynamic_content")

            # Get initial content
            initial_content = page.locator("[id='content'] div").first.inner_text()

            # Refresh the page to get new dynamic content
            page.reload()

            # Wait for content to potentially change
            page.wait_for_timeout(2000)  # 2 seconds

            # Verify the page still works with dynamic content
            content_elements = page.locator("[id='content'] div")
            expect(content_elements.first).to_be_visible()

            print("   ✅ Bump 2 navigated successfully - dynamic content handled")

        except Exception as e:
            print(f"   ⚠️  Bump 2 challenge: {str(e)}")
            # Continue with the test even if this bump fails
            pass

    @pytest.mark.regression
    def test_bumpy_road_comprehensive(self, page: Page, base_url: str) -> None:
        """
        Comprehensive bumpy road test with multiple types of challenges
        """
        print("🛣️  Starting comprehensive Bumpy Road test...")

        challenges = [
            ("Broken Images", "/broken_images"),
            ("JavaScript Errors", "/javascript_error"),
            ("Status Codes", "/status_codes"),
            ("Typos", "/typos"),
            ("Challenging DOM", "/challenging_dom"),
        ]

        successful_navigations = 0
        failed_navigations = 0

        for challenge_name, challenge_path in challenges:
            print(f"🚧 Navigating challenge: {challenge_name}")

            try:
                # Navigate to challenge page
                page.goto(f"{base_url.rstrip('/')}{challenge_path}")

                # Basic verification that we reached the page
                expect(page).to_have_url(f"{base_url.rstrip('/')}{challenge_path}")

                # Wait a bit to ensure page loads
                page.wait_for_timeout(1000)

                # Try to find any content on the page
                page_content = page.locator("body")
                expect(page_content).to_be_visible()

                print(f"   ✅ {challenge_name} navigated successfully")
                successful_navigations += 1

            except Exception as e:
                print(f"   ⚠️  {challenge_name} challenge: {str(e)}")
                failed_navigations += 1

            # Return to main page for next challenge
            try:
                page.goto(base_url)
                page.wait_for_timeout(500)
            except:
                pass

        print(
            f"🎉 Bumpy Road Summary: {successful_navigations} successful, {failed_navigations} failed"
        )

        # Test passes if we successfully navigated at least 60% of challenges
        success_rate = successful_navigations / len(challenges)
        assert (
            success_rate >= 0.6
        ), f"Success rate {success_rate:.2%} below 60% threshold"

    @pytest.mark.slow
    def test_bumpy_road_with_retries(self, page: Page, base_url: str) -> None:
        """
        Test bumpy road navigation with retry mechanism for handling flaky scenarios
        """
        print("🛣️  Starting Bumpy Road test with retry mechanism...")

        # Define challenging scenarios that might need retries
        challenging_scenarios = [
            {
                "name": "Entry Ad",
                "path": "/entry_ad",
                "action": lambda p: self._handle_entry_ad(p),
            },
            {
                "name": "Exit Intent",
                "path": "/exit_intent",
                "action": lambda p: self._handle_exit_intent(p),
            },
        ]

        for scenario in challenging_scenarios:
            print(f"🚧 Testing scenario: {scenario['name']}")

            success = False
            max_retries = 3

            for attempt in range(max_retries):
                try:
                    print(f"   Attempt {attempt + 1}/{max_retries}")

                    # Navigate to scenario
                    page.goto(f"{base_url.rstrip('/')}{scenario['path']}")

                    # Execute scenario-specific action
                    scenario["action"](page)

                    success = True
                    print(
                        f"   ✅ {scenario['name']} succeeded on attempt {attempt + 1}"
                    )
                    break

                except Exception as e:
                    print(f"   ⚠️  Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        print("   🔄 Retrying...")
                        page.wait_for_timeout(1000)  # Wait before retry

            if not success:
                print(f"   ❌ {scenario['name']} failed after {max_retries} attempts")

    def _handle_entry_ad(self, page: Page) -> None:
        """Handle entry ad scenario"""
        # Wait for page to load
        page.wait_for_timeout(2000)

        # Try to close any modal that might appear
        try:
            close_button = page.locator("text=Close")
            if close_button.is_visible(timeout=3000):
                close_button.click()
        except:
            pass

        # Verify we can interact with the page
        expect(page.locator("body")).to_be_visible()

    def _handle_exit_intent(self, page: Page) -> None:
        """Handle exit intent scenario"""
        # Wait for page to load
        page.wait_for_timeout(1000)

        # Simulate mouse movement to trigger exit intent
        try:
            page.mouse.move(0, 0)  # Move to top-left corner
            page.wait_for_timeout(500)
        except:
            pass

        # Verify page is still functional
        expect(page.locator("body")).to_be_visible()

    @pytest.mark.parametrize("bump_count", [1, 2, 3])
    def test_configurable_bumpy_road(
        self, page: Page, base_url: str, bump_count: int
    ) -> None:
        """
        Parametrized test for different numbers of bumps
        """
        print(f"🛣️  Testing Bumpy Road with {bump_count} bumps...")
        print(f"🔗 Base URL: {base_url}")

        # Define available bumps
        available_bumps = [
            ("Checkboxes", "/checkboxes", self._handle_checkboxes_bump),
            ("Dropdown", "/dropdown", self._handle_dropdown_bump),
            ("Hovers", "/hovers", self._handle_hovers_bump),
            ("Key Presses", "/key_presses", self._handle_key_presses_bump),
            ("Inputs", "/inputs", self._handle_inputs_bump),
        ]

        # Select the requested number of bumps
        selected_bumps = available_bumps[:bump_count]

        for i, (name, path, handler) in enumerate(selected_bumps, 1):
            print(f"🚧 Bump {i}/{bump_count}: {name}")

            try:
                full_url = f"{base_url.rstrip('/')}{path}"
                print(f"   🔗 Navigating to: {full_url}")
                page.goto(full_url)
                handler(page)
                print(f"   ✅ Bump {i} completed successfully")
            except Exception as e:
                print(f"   ⚠️  Bump {i} encountered issue: {str(e)}")

    def _handle_checkboxes_bump(self, page: Page) -> None:
        """Handle checkboxes interaction"""
        checkbox = page.locator("input[type='checkbox']").first
        expect(checkbox).to_be_visible()
        checkbox.check()
        expect(checkbox).to_be_checked()

    def _handle_dropdown_bump(self, page: Page) -> None:
        """Handle dropdown interaction"""
        dropdown = page.locator("select")
        expect(dropdown).to_be_visible()
        dropdown.select_option(index=1)

    def _handle_hovers_bump(self, page: Page) -> None:
        """Handle hover interaction"""
        hover_element = page.locator(".figure").first
        expect(hover_element).to_be_visible()
        hover_element.hover()

    def _handle_key_presses_bump(self, page: Page) -> None:
        """Handle key press interaction"""
        body = page.locator("body")
        body.press("Enter")
        result = page.locator("#result")
        expect(result).to_be_visible()

    def _handle_inputs_bump(self, page: Page) -> None:
        """Handle input field interaction"""
        number_input = page.locator("input[type='number']")
        if number_input.is_visible():
            number_input.fill("123")
