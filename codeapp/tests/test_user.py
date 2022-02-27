import logging
from unittest.mock import patch

from flask import url_for

from .utils import TestCase


class TestUser(TestCase):

    username = "default@chalmers.se"
    password = "testing"

    def test_login_render(self) -> None:
        response = self.client.get(url_for("bp.login"))
        self.assert200(response)
        self.assert_html(response)

    def test_register_render(self) -> None:
        response = self.client.get(url_for("bp.register"))
        self.assert200(response)
        self.assert_html(response)

    def test_incorrect_email(self) -> None:
        response = self.client.post(
            url_for("bp.login"),
            data={"email": "xyz@chalmers.se", "password": "123456"},
            follow_redirects=True,
        )
        self.assert200(response)
        self.assertTemplateUsed("login.html")
        self.assertIn("Please check email", response.data.decode())
        self.assert_html(response)

    def test_incorrect_password(self) -> None:
        response = self.client.post(
            url_for("bp.login"),
            data={"email": TestUser.username, "password": "123456"},
            follow_redirects=True,
        )
        self.assert200(response)
        self.assertTemplateUsed("login.html")
        self.assertIn("Please check email", response.data.decode())
        self.assert_html(response)

    def test_correct_login(self) -> None:
        response = self.client.post(
            url_for("bp.login"),
            data={"email": TestUser.username, "password": TestUser.password},
            follow_redirects=True,
        )
        self.assertTemplateUsed("home.html")
        self.assertMessageFlashed("Welcome!", "success")
        self.assert_html(response)

    def test_correct_login_redirect_next(self) -> None:
        response = self.client.post(
            url_for("bp.login", next="/profile"),
            data={"email": TestUser.username, "password": TestUser.password},
            follow_redirects=True,
        )
        self.assertTemplateUsed("profile.html")
        self.assertMessageFlashed("Welcome!", "success")
        self.assert_html(response)

    def test_logout(self) -> None:
        # first performs the login
        self.test_correct_login()

        # then tests the logout
        response = self.client.get(url_for("bp.logout"), follow_redirects=True)
        self.assertTemplateUsed("login.html")
        self.assertMessageFlashed("Logout successful!", "success")
        self.assert_html(response)

    def test_correct_login_redirect_home(self) -> None:
        # first performs the login
        self.test_correct_login()

        # then tests the logout
        response = self.client.get(url_for("bp.login"), follow_redirects=True)
        self.assertTemplateUsed("home.html")
        self.assert_html(response)

    def test_profile_not_logged(self) -> None:
        response = self.client.get(url_for("bp.profile"), follow_redirects=True)
        self.assertTemplateUsed("login.html")
        self.assertIn("Please log in to access this page.", response.data.decode())
        self.assert_html(response)

    def test_profile_logged_in(self) -> None:
        # first performs the login
        self.test_correct_login()

        response = self.client.get(url_for("bp.profile"), follow_redirects=True)
        self.assertTemplateUsed("profile.html")
        self.assertIn("User ID", response.data.decode())
        self.assert_html(response)

    def test_update_profile_render(self) -> None:
        # first logs in
        self.test_correct_login()

        response = self.client.get(url_for("bp.update_profile"))
        self.assertTemplateUsed("update_profile.html")
        self.assert_html(response)

    def test_update_profile_data_success(self) -> None:
        # first logs in
        self.test_correct_login()

        response = self.client.post(
            url_for("bp.update_profile"),
            data={"name": "Default User Updated", "submit_profile": True},
            follow_redirects=True,
        )
        self.assertTemplateUsed("profile.html")
        self.assertMessageFlashed("Profile updated successfully!", "success")
        self.assertIn("Default User Updated", response.data.decode())
        self.assert_html(response)

        # returning it to the initial condition
        response = self.client.post(
            url_for("bp.update_profile"),
            data={"name": "Default User", "submit_profile": True},
            follow_redirects=True,
        )
        self.assertMessageFlashed("Profile updated successfully!", "success")

    def test_update_profile_data_exception(self) -> None:
        # first logs in
        self.test_correct_login()
        # in this test, we need to patch the db.session
        # to simulate the database throwing an exception
        with patch(
            "codeapp.routes.db.session.commit",
            side_effect=ValueError("Mock error"),
            autospec=True,
            spec_set=True,
        ) as mock_commit:
            # mocks an error when calling the commit() method
            # mock.commit.
            response = self.client.post(
                url_for("bp.update_profile"),
                data={"name": "Default User Updated", "submit_profile": True},
                follow_redirects=True,
            )
            mock_commit.assert_called_once()
            self.assertTemplateUsed("update_profile.html")
            self.assertIn("There was an error", response.data.decode())
            self.assert_html(response)

    def test_update_profile_password_success(self) -> None:
        # first logs in
        self.test_correct_login()

        response = self.client.post(
            url_for("bp.update_profile"),
            data={
                "current_password": TestUser.password,
                "new_password": "testingupdated",
                "confirm_password": "testingupdated",
                "submit_password": True,
            },
            follow_redirects=True,
        )
        TestUser.password = "testingupdated"
        self.assertTemplateUsed("login.html")
        self.assertIn("Password updated successfully!", response.data.decode())
        self.assert_html(response)

        # first logs in
        self.test_correct_login()

        # returning it to the initial condition
        response = self.client.post(
            url_for("bp.update_profile"),
            data={
                "current_password": "testingupdated",
                "new_password": "testing",
                "confirm_password": "testing",
                "submit_password": True,
            },
            follow_redirects=True,
        )
        self.assertIn("Password updated successfully!", response.data.decode())
        TestUser.password = "testing"

    def test_update_profile_password_wrong_password(self) -> None:
        # first logs in
        self.test_correct_login()

        response = self.client.post(
            url_for("bp.update_profile"),
            data={
                "current_password": TestUser.password + "xyz",
                "new_password": "testingupdated",
                "confirm_password": "testingupdated",
                "submit_password": True,
            },
            follow_redirects=True,
        )
        self.assertTemplateUsed("update_profile.html")
        self.assertIn("Your current password did not match!", response.data.decode())
        self.assert_html(response)

    def test_update_profile_password_exception(self) -> None:
        # first logs in
        self.test_correct_login()
        # in this test, we need to patch the db.session
        # to simulate the database throwing an exception
        with patch(
            "codeapp.routes.db.session.commit",
            side_effect=ValueError("Mock error"),
            autospec=True,
            spec_set=True,
        ) as mock_commit:
            # mocks an error when calling the commit() method
            # mock.commit.
            response = self.client.post(
                url_for("bp.update_profile"),
                data={
                    "current_password": "testing",
                    "new_password": "testingupdated",
                    "confirm_password": "testingupdated",
                    "submit_password": True,
                },
                follow_redirects=True,
            )
            mock_commit.assert_called_once()
            self.assertTemplateUsed("update_profile.html")
            self.assertIn("There was an error", response.data.decode())
            self.assert_html(response)

    def test_sign_up_logged_in(self) -> None:
        # first performs the login
        self.test_correct_login()

        _ = self.client.get(
            url_for("bp.register"),
            follow_redirects=True,
        )
        self.assertTemplateUsed("home.html")

    def test_sign_up_wrong_passwords(self) -> None:
        response = self.client.post(
            url_for("bp.register"),
            data={
                "name": "Testing User",
                "email": "xyz@chalmers.se",
                "password": "testing",
                "confirm_password": "justtest",
            },
            follow_redirects=True,
        )
        self.assertTemplateUsed("register.html")
        self.assertIn("Field must be equal to password.", response.data.decode())
        self.assert_html(response)

    def test_sign_up_existing_email(self) -> None:
        response = self.client.post(
            url_for("bp.register"),
            data={
                "name": "Testing User",
                "email": "default@chalmers.se",
                "password": "testing",
                "confirm_password": "justtest",
            },
            follow_redirects=True,
        )
        self.assertTemplateUsed("register.html")
        self.assertIn("This email is already registered.", response.data.decode())
        self.assert_html(response)

    def test_sign_up_success(self) -> None:
        with patch(
            "codeapp.routes.db.session.add",
            autospec=True,
            spec_set=True,
        ) as mock_add, patch(
            "codeapp.routes.db.session.commit",
            autospec=True,
            spec_set=True,
        ) as mock_commit:
            response = self.client.post(
                url_for("bp.register"),
                data={
                    "name": "Testing User",
                    "email": "newtesting@chalmers.se",
                    "password": "testing",
                    "confirm_password": "testing",
                },
                follow_redirects=True,
            )

            # checks calls to the session
            mock_add.assert_called_once()  # db.session.add()
            mock_commit.assert_called_once()  # db.session.commit()

            # redirects to login upon success
            self.assertTemplateUsed("login.html")
            self.assertIn("User successfully created.", response.data.decode())
            self.assert_html(response)

    def test_sign_up_exception(self) -> None:
        # in this test, we need to patch the db.session
        # to simulate the database throwing an exception
        with patch(
            "codeapp.routes.db.session.add",
            autospec=True,
            spec_set=True,
        ) as mock_add, patch(
            "codeapp.routes.db.session.commit",
            side_effect=ValueError("Mock error"),
            autospec=True,
            spec_set=True,
        ) as mock_commit:
            # mocks an error when calling the commit() method
            # mock.commit.
            response = self.client.post(
                url_for("bp.register"),
                data={
                    "name": "Testing User",
                    "email": "sign_up_exception@chalmers.se",
                    "password": "testing",
                    "confirm_password": "testing",
                },
                follow_redirects=True,
            )
            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            self.assertTemplateUsed("register.html")
            self.assertIn("There was an error", response.data.decode())
            self.assert_html(response)


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
