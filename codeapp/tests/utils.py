import logging
import os
import sys
import time
import unittest
from subprocess import PIPE, Popen
from typing import Optional

import flask_testing
import requests
from bs4 import BeautifulSoup
from flask import Flask
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from werkzeug.test import TestResponse

from codeapp import create_app as ca


class TestCase(flask_testing.TestCase):
    # the URL below is for the general service
    # url = "https://validator.w3.org/nu/?out=json"

    # the URL below is for the service deployed at Chalmers
    url = "https://onu2.s2.chalmers.se/nu/?out=json"

    @classmethod
    def setUpClass(cls) -> None:
        env = os.environ.copy()
        env["APP_SETTINGS"] = "codeapp.config.TestingConfig"
        env["FLASK_ENV"] = "testing"
        cls._configured_port = int(os.environ.get("LIVESERVER_PORT", 5005))
        cls._process = Popen(  # pylint: disable=consider-using-with
            [
                sys.executable,
                "manage.py",
                "initdb",
            ],
            env=env,
            stdout=PIPE,
            stderr=PIPE,
        )
        cls._process.wait()
        assert (
            cls._process.returncode == 0
        ), "The database was not correctly initialized!"

    def create_app(self) -> Flask:
        os.environ["FLASK_ENV"] = "testing"
        app = ca("codeapp.config.TestingConfig")
        return app

    def assert_html(self, response: TestResponse) -> BeautifulSoup:
        html_to_test = response.data.decode("UTF-8")
        response_html = requests.post(
            self.url,
            headers={"Content-Type": "text/html; charset=UTF-8"},
            data=html_to_test,
        )
        message = ""
        has_error = False

        if response_html.json()["messages"]:
            has_error = True
            for key, value in response_html.json().items():
                if not isinstance(value, list):
                    message += key + " |-> " + value + "\n"
                else:
                    error_number = 1
                    html_split = html_to_test.split("\n")
                    for i in value:
                        message += "\n"
                        if "type" in i:
                            if i["type"] == "error":
                                message += f"\tError {error_number}:" + "\n"
                            elif i["type"] == "warning":
                                message += f"\tWarning {error_number}:" + "\n"
                            else:
                                message += f"""\t{i["type"]} {error_number}:\n"""
                            if error_number == 1:
                                message += (
                                    "\t\tThis is probably the one to look for first!"
                                    + "\n"
                                )

                            message += "\t\tMessage: " + i["message"] + "\n"

                            initial_line = max(0, i["lastLine"] - 3)
                            end_line = min(len(html_split) - 1, i["lastLine"] + 2)

                            message += (
                                f"""\t\tLine with problem: {i["lastLine"] - 1}\n"""
                            )
                            message += "\t\tCheck the code below:\n"

                            for j in range(initial_line, end_line):
                                mark = ""
                                if j + 1 == i["lastLine"]:
                                    mark = ">>"
                                message += f"""\t\t{j}: {mark}\t{html_split[j]}\n"""
                            error_number += 1
                        else:
                            for k2, v2 in i.items():
                                message += "\t" + str(k2) + " -> " + str(v2) + "\n\n"
        if has_error:
            raise ValueError(f"HTML error:\n{message}")
        soup = BeautifulSoup(html_to_test, "html.parser")
        return soup


class LiveTestCase(unittest.TestCase):
    _configured_port: int
    _process: Popen  # type: ignore

    @classmethod
    def setUpClass(cls) -> None:
        env = os.environ.copy()
        env["APP_SETTINGS"] = "codeapp.config.TestingConfig"
        env["FLASK_ENV"] = "testing"
        cls._configured_port = int(os.environ.get("LIVESERVER_PORT", 5005))
        cls._process = Popen(  # pylint: disable=consider-using-with
            [
                sys.executable,
                "manage.py",
                "initdb",
            ],
            env=env,
            stdout=PIPE,
            stderr=PIPE,
        )
        cls._process.wait()
        assert (
            cls._process.returncode == 0
        ), "The database was not correctly initialized!"
        cls._process = Popen(  # pylint: disable=consider-using-with
            [
                sys.executable,
                "manage.py",
                "run",
                f"--port={cls._configured_port}",
                "--host=localhost",
            ],
            env=env,
            stdout=PIPE,
            stderr=PIPE,
        )
        # waiting for server to start
        while True:
            time.sleep(1)
            if cls._process.stderr is not None:
                line = cls._process.stderr.readline()
                print(line.decode())
                if "Running" in line.decode():
                    break
                if "Address already in use" in line.decode():
                    raise ValueError(
                        f"Address `{cls.get_server_url()}` already in use. "
                        "Please stop any other server instance."
                    )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._process.terminate()

    @classmethod
    def get_server_url(cls) -> str:
        return f"http://localhost:{cls._configured_port}"


class FunctionalTestCase(LiveTestCase):
    wait_before_proceed: bool = False
    sleep_time: int = 1
    browser: webdriver.Firefox

    @classmethod
    def setUpClass(cls) -> None:
        LiveTestCase.setUpClass()
        cls.browser = webdriver.Firefox(log_path="./logs/geckodriver.log")
        _value = os.getenv("WAIT")
        if _value:
            cls.wait_before_proceed = bool(_value)
        else:
            cls.wait_before_proceed = False
        cls.browser.switch_to.window(cls.browser.current_window_handle)

    def wait(self) -> None:
        if self.wait_before_proceed:
            input("Press any key to proceed...")

    def sleep(self, sleep_time: Optional[int] = None) -> None:
        if self.wait_before_proceed:
            if sleep_time is None:
                sleep_time = self.sleep_time
            time.sleep(sleep_time)

    def wait_for_system(
        self, _id: Optional[str] = None, name: Optional[str] = None
    ) -> None:
        start_time = time.time()
        max_wait: int = 4
        while True:
            try:
                if _id is not None:
                    self.browser.find_element_by_id(_id)
                    return
                if name is not None:
                    self.browser.find_element_by_name(name)
                    return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > max_wait:
                    raise e
                time.sleep(0.5)

    @classmethod
    def tearDownClass(cls) -> None:
        LiveTestCase.tearDownClass()
        cls.browser.close()


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
