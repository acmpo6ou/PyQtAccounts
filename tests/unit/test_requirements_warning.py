#!/usr/bin/env python3

#  Copyright (c) 2020-2021. Bohdan Kolvakh
#  This file is part of PyQtAccounts.
#
#  PyQtAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyQtAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.
#
#  PyQtAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyQtAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.

# PyQtAccounts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PyQtAccounts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import unittest
import pytest
import os

from tests.base import UnitTest
from core.const import *
import PyQtAccounts


class ReqsWarningsTest(UnitTest):
    """
    This class tests Reqs class from setup.py module and warinigs that must
    appear if user has not installed some of dependencies.
    """

    def test_system_reqs(self):
        """
        This test tests system requirements (i.e. those that we can't install
        without root privileges).
        """
        # here we overide `exec` method of WarningWindow to prevent it from
        # appearing.
        PyQtAccounts.WarningWindow.exec = lambda *args: PyQtAccounts.QMessageBox.Ok

        def mock_system(command):
            """
            This is test double of os.system function.
            """
            # here we check does command argument is right, it must be
            # some-thing like this: `which <dependency name>`.
            # So first we crop `which ` and then we check whether the rest
            # is a system dependency.
            req = command.replace("which ", "")
            assert (
                req in PyQtAccounts.sys_reqs
            ), "Requirement in os.system call is not a system requirement!"

            # here we check requirement that is passed to our fake
            # os.system
            if req == "git":
                # if it is `git` then we return nonzero exit code to simulate
                # error in 'which' command that checks whether requirement is
                # installed or not, so PyQtAccounts will think that we don't
                # have `git` installed.
                return True
            else:
                # else if it is not `git` we return zero
                # exit code to simulate that no errors were occur in
                # `which` command
                return False

        # Lea hasn't install `git` which is a PyQtAccounts system dependency
        self.monkeypatch.setattr("os.system", mock_system)

        # So she launches the program, main function returns a WarningWindow
        # instance that appeared during programs lifetime.

        msg = PyQtAccounts.main()

        # Warning message appears saying that she needs to install `git` to
        # make program work
        self.assertEqual(
            "Увага!",
            msg.windowTitle(),
            "Title of requirements warning message is incorrect!",
        )
        print(repr(msg.text()))
        self.assertEqual(
            (
                "\n                "
                "<h3>Не всі пакети встановлено!</h3>"
                "\n                "
                "<p>Пакет git не встановлено, без певних пакетів PyQtAccounts "
                "буде працювати \n                некоректно!</p>\n"
                "                <p>Встановіть git такою командою:</p>\n"
                "                <p>sudo apt install git</p>\n                "
            ),
            msg.text(),
            "Requirements warning message is incorrect!",
        )

    def test_pip_reqs(self):
        """
        This test tests pip requirements warnings. Those that popup when user
        hasn't installed some of pip dependencies.
        """
        # here we override `exec` method of ErrorWindow to prevent it from
        # appearing
        PyQtAccounts.ErrorWindow.exec = lambda *args: PyQtAccounts.QMessageBox.Ok

        def mock_pip():
            raise ImportError("No module named cryptography!")

        # Toon hasn't installed cryptography which is a PyQtAccounts pip
        # dependency
        self.monkeypatch.setattr("PyQtAccounts.Window", mock_pip)

        # So he launches the program, main function returns an ErrorWindow
        # instance that appeared during programs lifetime.
        msg = PyQtAccounts.main()

        # Error message appears saying that he hasn't installed `cryptography`
        self.assertEqual(
            "Помилка!", msg.windowTitle(), "Title of error message is incorrect!"
        )
        mess = (
            "<p>Здається не всі бібліотеки встановлені.</p>"
            f"<p>Переконайтеся що ви встановили бібліотеку cryptography.</p>"
            "<p>Якщо ні, спробуйте ввести в термінал цю кофманду:</p>"
            f"<p><b>pip3 install cryptography</b></p>"
        )
        self.assertEqual(mess, msg.text(), "Error message is incorrect!")
        self.assertEqual(
            "No module named cryptography!",
            msg.detailedText(),
            "Detailed text of error message is incorrect!",
        )
