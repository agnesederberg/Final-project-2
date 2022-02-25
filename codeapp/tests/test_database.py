import inspect
import logging
from dataclasses import fields, is_dataclass

from sqlalchemy import func, select

from codeapp import db, models

from .utils import TestCase


class TestDatabase(TestCase):
    """
    This class tests if the database is correctly modeled according
    to the course guidelines.
    """

    @classmethod
    def is_camel_case(cls, s: str) -> bool:
        return s != s.lower() and s != s.upper() and "_" not in s

    def test_database_number_tables(self) -> None:
        """
        This method tests if the number of tables is at least 4,
        excluding the association tables.
        """
        num_classes = 0
        for name, obj in inspect.getmembers(models):
            if is_dataclass(obj):
                # test for the name
                assert TestDatabase.is_camel_case(
                    name
                ), f"Class name of class `{name}` does not seem correct."
                assert obj.__tablename__ == obj.__tablename__.lower(), (
                    f"The table name `{obj.__tablename__}` should "
                    "be in lowercase letters."
                )
                column_names = []
                for field in fields(obj):
                    assert (
                        field.name == field.name.lower()
                    ), f"Column `{field.name}` should be in lowercase letters."
                    column_names.append(field.name)
                assert "id" in column_names, (
                    f"Table `{name}` must have a column `id`. "
                    f"At the moment it has only {column_names}."
                )
                num_classes += 1

        assert num_classes >= 4, f"At the moment, you have only {num_classes}. "
        "You must have at least 4 database tables."

    def test_database_rows(self) -> None:
        """
        This method tests if each table has at least 5 rows.
        5 rows is the minimum accepted.
        """
        for name, obj in inspect.getmembers(models):
            if is_dataclass(obj):
                count = db.session.execute(select(func.count(obj.id))).scalar()
                assert count >= 5, (
                    f"Table `{name}` must have at least 5 rows. "
                    f"At the moment it has only {count} row(s)."
                )


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
