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

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pyfakefs.fake_filesystem_unittest as fs_unit
from unittest.mock import Mock
import pytest
import os

from tests.base import SetupFuncTest, SetupMixin
from setup import *

INSTALL_ERRORS_TEXT = (
    'Не вдалося встановити cryptography\n'
    'Не вдалося встановити gitpython\n'
)


class RequirementsPageTest(SetupFuncTest, SetupMixin):
    def tearDown(self):
        super().tearDown()
        self.wizard.hide()

    def test_install_no_pip(self):
        # Toon wants to install PyQtAccounts
        # He hasn't installed pip and some of dependencies
        self.patchReqs(['gitpython', 'pyshortcuts'], ['pip3'])

        # So far he proceed to requirements page
        self.wizard = InstallationWizard()
        self.wizard.show()
        self.next = self.wizard.button(QWizard.NextButton)
        self.next.click()

        # next button is unavailable until Toon installs all dependencies
        self.assertFalse(self.next.isEnabled())

        # and he presses install button
        page = self.wizard.currentPage()
        page.installButton.click()

        # The error appears saying that he need to install pip first
        self.assertTrue(page.errors.visibility)
        self.assertEqual(page.errors.toPlainText(), 'Встановіть пакет pip3!')

    def test_install_button(self):
        # Tom wants to install PyQtAccounts
        # He hasn't installed some pip dependencies
        self.to_install = ['cryptography', 'gitpython']
        self.patchReqs(self.to_install)

        # So he proceed to the requirements page
        self.wizard = InstallationWizard()
        self.next = self.wizard.button(QWizard.NextButton)
        self.wizard.show()
        self.next.click()

        # installation will be successful
        self.monkeypatch.setattr('os.system', self.mock_system(False))

        # He presses install button
        page = self.wizard.currentPage()
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
        to_install = ['cryptography', 'gitpython']
        self.patchReqs(to_install)

        # So he proceed to the requirements page
        self.wizard = InstallationWizard()
        self.next = self.wizard.button(QWizard.NextButton)
        self.wizard.show()
        self.next.click()

        # installation will be unsuccessful
        self.monkeypatch.setattr('os.system', self.mock_system(True))

        # He presses install button
        page = self.wizard.currentPage()
        page.installButton.click()

        # Some errors appearing during installation.
        QTest.qWait(300)
        print(repr(page.errors.toPlainText()))
        self.assertEqual(page.errors.toPlainText(), INSTALL_ERRORS_TEXT)
        self.assertTrue(page.errors.visibility)

        # Next button is still disabled
        self.assertFalse(self.next.isEnabled())
