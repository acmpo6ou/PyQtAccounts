#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh Bohdan
# This file is part of PyQtAccounts.

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
import time

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from unittest.mock import Mock
import os
import setup
import pytest

from tests.base import UnitTest, SetupMixin
from setup import *


class RequirementsPageTest(UnitTest, SetupMixin):
    """
    This class provides all functional tests for RequirementsPage.
    """
    def test_install_no_pip(self):
        """
        Here we test how installation goes when we have no pip installed (i.e.
        program must show error).
        """
        # Toon wants to install PyQtAccounts
        # He hasn't installed pip and some of dependencies
        self.test_reqs = Reqs()
        self.test_reqs.to_install = ['cryptography', 'gitpython']
        self.test_reqs.cant_install = ['pip3']
        self.test_reqs.installed.remove('pyshortcuts')
        self.test_reqs.installed.remove('gitpython')
        self.test_reqs.installed.remove('pip3')

        # and he presses install button
        page = RequirementsPage(reqs=self.test_reqs)
        page.installButton.click()

        # The error appears saying that he need to install pip first
        self.assertTrue(
            page.errors.visibility,
            "Error message isn't displayed when user wants to "
            "install unsatisfied dependencies and has no pip installed!")
        self.assertEqual(
            page.errors.toPlainText(), 'Встановіть пакет pip3!',
            "Error message is incorrect when user wants to "
            "install unsatisfied dependencies and has no pip installed!")

    def test_install_button(self):
        """
        Here we test what happens when user presses install button and
        everything is OK.
        """
        # Tom wants to install PyQtAccounts
        # He hasn't installed some pip dependencies
        self.test_reqs = Reqs()
        self.test_reqs.to_install = ['cryptography', 'gitpython']
        self.test_reqs.installed.remove('cryptography')
        self.test_reqs.installed.remove('gitpython')

        # installation will be successful
        os.system = self.mock_system(False)

        # He presses install button
        page = RequirementsPage(reqs=self.test_reqs)
        page.installButton.click()

        # He has pip3 installed so errors are cleared and hidden
        self.assertEqual(
            page.errors.toPlainText(), '',
            "Error message must be empty when user wants to "
            "install unsatisfied dependencies and HAS pip installed!")
        self.assertFalse(
            page.errors.visibility,
            "Error message is displayed when user wants to "
            "install unsatisfied dependencies and HAS pip installed!")

        # install button is disabled
        self.assertFalse(
            page.installButton.isEnabled(),
            "Install button is enabled during installation, must "
            "be disabled to avoid creating many threads that will install pip"
            "dependencies at the same time and that will crash program!")

        # install label and progress are shown
        self.assertTrue(page.installLabel.visibility,
                        "Install label isn't displayed during installation!")
        self.assertTrue(
            page.installProgress.visibility,
            "Install progressbar doesn't displayed during installation!")

        # some time pass and progress bar moves to 50%
        QTest.qWait(150)
        self.assertEqual(
            page.installProgress.value(), 50,
            "Progress bar doesn't update to 50% when ½ of installation"
            "process is done!")

        # finally it shows 100% and everything is installed without any errors
        QTest.qWait(150)
        self.assertEqual(
            page.installProgress.value(), 100,
            "Progress bar doesn't update to 100% when installation "
            "process has finished!")
        self.assertEqual(
            page.errors.toPlainText(), '',
            "Error text must be empty when installation is"
            "successful!")
        self.assertFalse(
            page.errors.visibility,
            "Error must be hidden when installation is successful!")

        # install label says that everything is installed successfully
        self.assertEqual(
            page.installLabel.text(),
            '<p style="color: #37FF91;">Встановлено!</p>',
            "Install label must show successful message when"
            "installation has finished successfully!")

        # tips are hidden
        self.assertFalse(
            page.reqsTips.visibility,
            "Tips must be hidden when installation has finished"
            "successfully!")

    def test_errors_during_installation(self):
        """
        Here we test what happens when there are errors during installation.
        """
        # Tom wants to install PyQtAccounts
        # He hasn't installed some pip dependencies
        self.test_reqs = Reqs()
        self.test_reqs.to_install = ['cryptography', 'gitpython']
        self.test_reqs.installed.remove('cryptography')
        self.test_reqs.installed.remove('gitpython')

        # installation will be unsuccessful, so os.system will return nonzero
        # exit code
        self.monkeypatch.setattr('os.system', lambda command: True)

        # He presses install button
        page = RequirementsPage(reqs=self.test_reqs)
        page.installButton.click()

        # Some errors appears during installation.
        def errors_visible():
            assert page.errors.visibility,\
                    "Error message doesn't displayed when there are errors" \
                    "during installation!"

        self.qbot.waitUntil(errors_visible)

        INSTALL_ERRORS_TEXT = ('Не вдалося встановити cryptography\n'
                               'Не вдалося встановити gitpython\n')
        self.assertEqual(
            page.errors.toPlainText(), INSTALL_ERRORS_TEXT,
            "Error message is incorrect when there are errors"
            "during installation!")
