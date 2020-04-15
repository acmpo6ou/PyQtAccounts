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
from unittest.mock import Mock
import pytest
import time
import os

from tests.base import SetupFuncTest, SetupMixin
from setup import *


class InstallationWizardTest(SetupFuncTest, SetupMixin):
    def tearDown(self):
        super().tearDown()
        self.wizard.hide()

    def test_pages(self):
        self.wizard = InstallationWizard()
        self.next = self.wizard.button(QWizard.NextButton)

        # Bob wants to install PyQtAccounts, so he launches setup.py
        self.wizard.show()

        # He sees welcome page
        self.assertIsInstance(self.wizard.currentPage(), WelcomePage)

        # Bob presses `Next` button then
        self.next.click()

        # Next is requirements page
        self.assertIsInstance(self.wizard.currentPage(), RequirementsPage)

        # Everything is installed so he presses `Next`
        self.next.click()

        # Next is initialization page
        self.assertIsInstance(self.wizard.currentPage(), InitPage)
