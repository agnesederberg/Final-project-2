import logging

import pytest
from selenium.webdriver.common.keys import Keys

from .utils import FunctionalTestCase

logger = logging.getLogger("functional")
logger.setLevel(logging.DEBUG)


class TestFunctional(FunctionalTestCase):
    @pytest.mark.order(1)
    def test_server_is_up_and_running(self) -> None:
        # establish intent
        logger.info("John wants to check if the project website is up and running.")

        # introduce, execute, wait
        logger.info("John opens the web browser and tries to access the project.")
        self.browser.get(self.get_server_url())
        self.wait()
        self.wait_for_system(_id="navbar_brand")

        # introduce, execute, wait
        logger.info("Once the page loads, it is possible to see the title `Skeleton`")
        self.assertIn("Skeleton", self.browser.title)
        logger.info("John is happy and closes the browser")

    # tests for use cases where the user is not logged in go here

    # end of your tests here

    @pytest.mark.order(20)
    def test_about_page(self) -> None:
        # establish intent
        logger.info(
            "John wants to check if the `about` page of the project is working."
        )

        # introduce, execute, wait
        logger.info("John opens the web browser and tries to access the project.")
        self.browser.get(self.get_server_url() + "/about")
        self.wait()
        self.wait_for_system(_id="about_header")

        # introduce, execute, wait
        logger.info("Once the page loads, it is possible to see the page title `About`")
        self.assertIn("About", self.browser.page_source)
        logger.info("John is happy and closes the browser")

    @pytest.mark.order(21)
    def test_register_page(self) -> None:
        # establish intent
        logger.info("John wants to register on the website.")

        # introduce, execute, wait
        logger.info("John clicks on the `Register` link.")
        self.browser.get(self.get_server_url())
        register_link = self.browser.find_element_by_id("register")
        register_link.click()
        self.wait_for_system(_id="register_form")
        self.wait()

        # introduce, execute, wait
        logger.info("John fills in the information.")

        name_field = self.browser.find_element_by_name("name")
        name_field.send_keys("New Functional Test User")
        self.sleep()

        email_field = self.browser.find_element_by_name("email")
        email_field.send_keys("newfunctional@chalmers.se")
        self.sleep()

        password_field = self.browser.find_element_by_name("password")
        password_field.send_keys("functionalpass")
        self.sleep()

        confirm_field = self.browser.find_element_by_name("confirm_password")
        confirm_field.send_keys("functionalpass")
        self.sleep()

        # introduce, execute, wait
        logger.info("John types `Enter` to submit the form.")
        confirm_field.send_keys(Keys.RETURN)
        self.sleep()
        self.wait_for_system(_id="form_login")

        # introduce, execute, wait
        logger.info("John checks if a success message appears on the webpage.")
        self.assertIn("User successfully created", self.browser.page_source)
        logger.info("John is happy!")
        self.wait()
        self.wait_for_system(_id="form_login")

    @pytest.mark.order(22)
    def test_login_page(self) -> None:
        # establish intent
        logger.info("John now wants to log in using the newly created log in.")

        # introduce, execute, wait
        logger.info("John opens the log in page.")
        self.browser.get(self.get_server_url())
        register_link = self.browser.find_element_by_id("login")
        register_link.click()

        # introduce, execute, wait
        logger.info("John fills in the email and password registered before.")
        email_field = self.browser.find_element_by_name("email")
        email_field.send_keys("newfunctional@chalmers.se")
        self.sleep()

        password_field = self.browser.find_element_by_name("password")
        password_field.send_keys("functionalpass")
        self.sleep()

        remember_field = self.browser.find_element_by_name("remember")
        remember_field.click()
        self.sleep()

        # introduce, execute, wait
        logger.info("John types `Enter` to submit the form.")
        password_field.send_keys(Keys.RETURN)
        self.sleep()
        self.wait_for_system(_id="homepage_header")

        # introduce, execute, wait
        logger.info("John checks if he is redirected to the home page.")
        self.assertIn("Home page", self.browser.page_source)
        self.assertIn("New Functional Test", self.browser.page_source)
        logger.info("John is happy and leaves the website!")
        self.wait()

    # tests of use case where the user is logged in go here

    # end of your tests here

    @pytest.mark.order(41)
    def test_profile_page(self) -> None:
        # establish intent
        logger.info("John wants to check if his profile is correct.")

        # introduce, execute, wait
        logger.info("John clicks in the `Profile` link")
        register_link = self.browser.find_element_by_id("profile")
        register_link.click()
        self.wait_for_system(_id="profile_header")

        # introduce, execute, wait
        self.assertIn("New Functional Test", self.browser.page_source)
        self.assertIn("newfunctional@chalmers.se", self.browser.page_source)
        self.wait()

    @pytest.mark.order(42)
    def test_update_profile(self) -> None:
        # establish intent
        logger.info("John wants to update his name.")

        # introduce, execute, wait
        logger.info("John clicks on the `update_profile` button.")
        update_link = self.browser.find_element_by_id("update_profile")
        update_link.click()
        self.wait_for_system(_id="profile_form")

        # introduce, execute, wait
        self.assertIn("Update profile", self.browser.page_source)
        name_field = self.browser.find_element_by_name("name")
        self.sleep()
        name_field.clear()
        self.sleep()
        name_field.send_keys("John Doe")
        self.sleep()

        name_field.send_keys(Keys.RETURN)
        self.sleep(2)
        self.wait_for_system(_id="profile_header")

        # introduce, execute, wait
        logger.info("John checks if the change was successful.")
        self.assertIn("Profile updated successfully", self.browser.page_source)
        self.assertIn("John Doe", self.browser.page_source)

        self.wait()

    @pytest.mark.order("last")
    def test_logout(self) -> None:
        # establish intent
        logger.info("John wants to log out.")

        # introduce, execute, wait
        logout_link = self.browser.find_element_by_id("logout")
        logout_link.click()
        self.sleep()
        self.wait_for_system(_id="form_login")

        logger.info("John checks if success message is shown.")
        self.assertIn("Logout successful", self.browser.page_source)

        logger.info(
            "John finishes his interaction with the system and closes the browser."
        )
        self.wait()


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
