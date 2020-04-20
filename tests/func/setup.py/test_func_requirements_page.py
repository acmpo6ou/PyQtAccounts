#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh B.
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

import pyfakefs.fake_filesystem_unittest as fs_unit
from unittest.mock import Mock
import os
import setup
import pytest

from tests.base import UnitTest, SetupMixin
from setup import *


class RequirementsPageTest(UnitTest, SetupMixin):
    def test_install_no_pip(self):
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
        self.assertTrue(page.errors.visibility)
        self.assertEqual(page.errors.toPlainText(), 'Встановіть пакет pip3!')

    def test_install_button(self):
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
        self.assertEqual(page.errors.toPlainText(), '')
        self.assertFalse(page.errors.visibility)

        # install button is disabled
        self.assertFalse(page.installButton.isEnabled())

        # install label and progress are shown
        self.assertTrue(page.installLabel.visibility)
        self.assertTrue(page.installProgress.visibility)

        # some time pass and progress bar moves to 50%
        QTest.qWait(150)
        self.assertEqual(page.installProgress.value(), 50)

        # finally it shows 100% and everything is installed without any errors
        QTest.qWait(150)
        self.assertEqual(page.installProgress.value(), 100)
        self.assertEqual(page.errors.toPlainText(), '')
        self.assertFalse(page.errors.visibility)

        # install label says that everything is installed successfully
        self.assertEqual(page.installLabel.text(), '<p style="color: #37FF91;">Встановлено!</p>')

        # tips are hidden
        self.assertFalse(page.reqsTips.visibility)

    def test_errors_during_installation(self):
        # Tom wants to install PyQtAccounts
        # He hasn't installed some pip dependencies
        self.test_reqs = Reqs()
        self.test_reqs.to_install = ['cryptography', 'gitpython']
        self.test_reqs.installed.remove('cryptography')
        self.test_reqs.installed.remove('gitpython')

        # installation will be unsuccessful
        self.monkeypatch.setattr('os.system', lambda command: True)

        # He presses install button
        page = RequirementsPage(reqs=self.test_reqs)
        page.installButton.click()

        # Some errors appears during installation.
        QTest.qWait(100)
        INSTALL_ERRORS_TEXT = (
            'Не вдалося встановити cryptography\n'
            'Не вдалося встановити gitpython\n'
        )
        self.assertEqual(page.errors.toPlainText(), INSTALL_ERRORS_TEXT)
        self.assertTrue(page.errors.visibility)
