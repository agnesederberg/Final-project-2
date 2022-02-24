import logging
from unittest.mock import patch

from flask import url_for

from codeapp import create_app

from .utils import TestCase


class TestSetup(TestCase):
    """
    Class that includes tests related to the setup of the app.
    These tests make sure the configuration is correct for the different app configs.
    """

    def test_routes(self) -> None:
        """
        Method that tests the translation of all the routes in the project.
        This method can be used as a first step towards creating a new route
        by including the desired route here.
        """
        self.assertEqual(url_for("bp.home"), "/")
        url_for("bp.about")
        url_for("bp.register")
        url_for("bp.login")
        url_for("bp.logout")
        url_for("bp.profile")
        url_for("bp.update_profile")

    def test_dev_configuration(self) -> None:
        """
        Method used to test the properties of the `development` configuration.
        Note that a mock is used for the `os.getenv` function to check if it is called.
        """
        with patch("codeapp.os.getenv", autospec=True, spec_set=True) as mock:
            mock.return_value = "codeapp.config.DevelopmentConfig"
            app = create_app()
            mock.assert_called()
            self.assertEqual(app.config["SQLALCHEMY_ECHO"], True)

    def test_prod_configuration(self) -> None:
        """
        Method used to test the `production` configuration.
        Two mocks are used, one for the `os.getenv` function,
        and one for the database URL.
        """
        with patch("codeapp.os.getenv", autospec=True, spec_set=True) as mock, patch(
            "codeapp.config.ProductionConfig.SQLALCHEMY_DATABASE_URI",
            autospec=True,
            spec_set=True,
        ) as mock_config:
            mock.return_value = "codeapp.config.ProductionConfig"
            mock_config.return_value = "sqlite:///site-prod.db"
            app = create_app("codeapp.config.ProductionConfig")
            mock.assert_not_called()
            self.assertEqual(app.config["SQLALCHEMY_ECHO"], False)


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
