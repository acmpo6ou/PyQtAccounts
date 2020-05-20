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

'''
This module provides all unit tests that about PasswordField class.
'''

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import unittest
import pytest
import os

from tests.base import UnitTest
from core.widgets import PasswordField


class PasswordFieldTest(UnitTest):
    """
    This class contains all unit tests for PasswordFieldTest class.
    """
    def test_show_hide(self):
        """
        This test tests toggle password visibility button.
        """
        # here we create password field specifying placeholder (`enter password`)
        field = PasswordField('enter password')
        showButton = field.showButton  # password visibility toggle button
        passInput = field.passInput    # password field itself

        # Bob has password field that says `enter password`, also when Bob
        # types something in that field password is invisible
        self.assertEqual('enter password', passInput.placeholderText(),
                         'Password field placeholder is incorrect!')
        self.assertEqual(QLineEdit.Password, passInput.echoMode(),
                         "Password must be invisible!")

        # Bob then toggles password visibility pressing special button near the
        # field
        showButton.click()
        # password is visible now
        self.assertEqual(QLineEdit.Normal, passInput.echoMode(),
                         'Password must be visible!')

        # Bob then hides password pressing special button near the field again
        showButton.click()
        # password is invisible now
        self.assertEqual(QLineEdit.Password, passInput.echoMode(),
                         'Password must be invisible!')
