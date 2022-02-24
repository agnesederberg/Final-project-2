import logging

from flask import url_for

from .utils import TestCase


class TestHomePage(TestCase):
    def test_home_page(self) -> None:
        response = self.client.get(url_for("bp.home"))
        self.assert200(response)
        self.assertTemplateUsed("home.html")
        self.assertIn("Home", response.data.decode())
        self.assert_html(response)

    def test_about_page(self) -> None:
        response = self.client.get(url_for("bp.about"))
        self.assert200(response)
        self.assertTemplateUsed("about.html")
        self.assertIn("About", response.data.decode())
        self.assert_html(response)


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
