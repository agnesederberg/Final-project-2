import logging

from flask import url_for

from codeapp.tests.test_user import TestUser

from .utils import TestCase


class TestSearch(TestCase):
    """
    This class must implement the test cases related to the search use case.
    Implement as many methods as needed to cover 100% of the code.
    """

    def test_render(self) -> None:
        """
        This test tests the rendering of the page, and the creation of the route.
        A code snippet is provided below.
        """
        # response = self.client.get(url_for("bp.<function name>"))
        # self.assert200(response)
        # self.assertTemplateUsed("<template name>.html")
        # self.assert_html(response)

    def test_search(self) -> None:
        # Logging in
        temp = self.client.post(
            url_for("bp.login"),
            data={"email": TestUser.username, "password": TestUser.password},
            follow_redirects=True,
        )

        self.assertTemplateUsed("home.html")
        self.assertMessageFlashed("Welcome!", "success")

        response = self.client.get(
            "folders/1",
            follow_redirects=True,
        )
        self.assert200(response)
        self.assertTemplateUsed("notes.html")
        self.assert_html(response)

        response = self.client.post(
            "folders/1",
            data={
                "submit": "search",
                "search": "Go",
            },
            follow_redirects=True,
        )

        self.assertTemplateUsed("notes.html")
        self.assertIn("Go to the stables before july", response.data.decode())
        self.assert_html(response)

        response = self.client.post(
            "folders/1",
            data={
                "submit": "clearSearch",
            },
            follow_redirects=True,
        )

        self.assertTemplateUsed("notes.html")
        self.assertIn("Go to the stables before july", response.data.decode())
        self.assert_html(response)


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
