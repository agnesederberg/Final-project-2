import logging

from .utils import TestCase


class TestDetail(TestCase):
    """
    This class must implement the test cases related to the detail use case.
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

    def test_detail(self) -> None:
        """
        Example of test method.
        Put below the code for the test.
        """


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
