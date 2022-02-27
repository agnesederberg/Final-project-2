import logging

from .utils import TestCase


class TestCreate(TestCase):
    """
    This class must implement the test cases related to the create/insert use case.
    Implement as many methods as needed to cover 100% of the code.
    """

    def test_render(self) -> None:
        """
        This test tests the rendering of the page, and the creation of the route.
        A code snippet is provided below.
        """
        # add the import:
        # from flask import url_for
        # response = self.client.get(url_for("bp.<function name>"))
        # self.assert200(response)
        # self.assertTemplateUsed("<template name>.html")
        # self.assert_html(response)

    def test_incorrectly_filled_form(self) -> None:
        """
        This function tests that the form is working correctly when provided with
        invalid data.
        """
        # response = self.client.post(
        #     url_for("bp.<function name>"),
        #     data={<data here in the form of a dictionary>},
        #     follow_redirects=True,
        # )
        # self.assert200(response)
        # self.assertTemplateUsed("<template name>.html")
        # self.assertIn("<expected error message>", response.data.decode())
        # self.assert_html(response)

    def test_correctly_filled_form(self) -> None:
        """
        This function tests that the form is working correctly when provided with
        valid data.
        """
        # response = self.client.post(
        #     url_for("bp.<function name>"),
        #     data={<data here in the form of a dictionary>},
        #     follow_redirects=True,
        # )
        # self.assert200(response)
        # self.assertTemplateUsed("<template name>.html")
        # self.assertIn("<expected error message>", response.data.decode())
        # self.assertRedirects(
        #     response,
        #     url_for("bp.<function where the user should be redirected to>")
        # )
        # self.assert_html(response)

    def test_form_exception(self) -> None:
        """
        This function tests that the form is capable of handling
        exceptions coming from the database.
        The exception is generated by mocking the session object.
        """
        # add the import:
        # from unittest.mock import patch
        # with patch(
        #     "codeapp.routes.db.session.commit",
        #     side_effect=ValueError("Mock error"),
        #     autospec=True,
        #     spec_set=True,
        # ) as mock_commit:
        #     response = self.client.post(
        #         url_for("bp.<function name>"),
        #         data={<data here in the form of a dictionary>},
        #         follow_redirects=True,
        #     )
        #     # we expect the session commit to be called once
        #     mock_commit.assert_called_once()

        #     self.assert200(response)
        #     self.assertTemplateUsed("<template name>.html")
        #     self.assertIn("<expected error message>", response.data.decode())
        #     self.assert_html(response)


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
