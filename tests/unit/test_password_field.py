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
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import unittest
import pytest
import os

from tests.base import UnitTest
from core.widgets import PasswordField


class PasswordFieldTest(UnitTest):
    def test_show_hide(self):
        field = PasswordField('enter password')
        showButton = field.showButton
        passInput = field.passInput

        self.assertEqual('enter password', passInput.placeholderText())
        self.assertEqual(QLineEdit.Password, passInput.echoMode())

        showButton.click()
        self.assertEqual(QLineEdit.Normal, passInput.echoMode())

        showButton.click()
        self.assertEqual(QLineEdit.Password, passInput.echoMode())
