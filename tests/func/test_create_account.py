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
import pyautogui
from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
import unittest
import pytest
import os

from tests.base import AccsTest
from core.utils import *
from PyQtAccounts import *


class Test(AccsTest):
    def setUp(self):
        super().setUp()
        self.form = self.accs.forms['create']

        self.account_name = self.form.accountInput
        self.nameError = self.form.nameError
        self.nameFilledError = self.form.nameFilledError
        self.passFilledError = self.form.passFilledError
        self.passEqError = self.form.passEqError
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput
        self.createButton = self.form.createButton

    def checkNameErrors(self):
        self.assertFalse(self.nameError.visibility)
        self.assertFalse(self.nameFilledError.visibility)

    @pytest.mark.skip
    def test_create_account_ctrl_n(self):
        pyautogui.hotkey("ctrl", "n")
        QTest.qWait(500)
        self.checkOnlyVisible(self.form)

    def test_create_account_click(self):
        self.accs.panel.addButton.click()
        self.checkOnlyVisible(self.form)

    def test_create_account_menu(self):
        file = self.win.menuBar().actions()[0]  # first is `File` submenu
        new_db = file.menu().actions()[0]  # first action is `New account...`
        new_db.trigger()
        self.checkOnlyVisible(self.form)

    def test_validate_name(self):
        # Tom wants to create account, for now there is no errors
        self.accs.panel.addButton.click()
        self.checkNameErrors()

        # He starts typing `gma` at the name field
        QTest.keyClicks(self.account_name, 'gma')

        # There is no errors
        self.checkNameErrors()

        # Toon then continue and types `il`
        QTest.keyClicks(self.account_name, 'il')

        # The error message appears saying that account with such name exists
        self.assertTrue(self.nameError.visibility)

        # He then types `2` to account name field
        QTest.keyClicks(self.account_name, '2')

        # The error message disappears
        self.assertFalse(self.nameError.visibility)

        # Toon then erases account name
        self.account_name.setText('')

        # Another error message appears saying that he must feel account name field
        self.assertTrue(self.nameFilledError.visibility)

        # Toon then types `someaccount` to name field
        self.account_name.setText('someaccount')

        # The error message disappears
        self.assertFalse(self.nameFilledError.visibility)

    def test_create_button_enabled(self):
        # Bob wants to create new account, create button disabled
        self.accs.panel.addButton.click()
        self.assertFalse(self.createButton.isEnabled())

        # He fills account name field and create button is still disabled
        self.account_name.setText('someaccount')
        self.assertFalse(self.createButton.isEnabled())

        # He then fills password fields
        self.pass_input.setText('some_password')
        self.pass_repeat_input.setText('some_password')

        # Create button enables now
        self.assertTrue(self.createButton.isEnabled())

        # Bob then erases name field, create button disables
        self.account_name.setText('')
        self.assertFalse(self.createButton.isEnabled())

        # He then types `gmail` at the name field and create button is still disabled
        self.account_name.setText('gmail')
        self.assertFalse(self.createButton.isEnabled())

        # Then Bob changes it to `Gmail`, create button enables
        self.account_name.setText('Gmail')
        self.assertTrue(self.createButton.isEnabled())

        # He then changes password in first field to `pass`
        self.pass_input.setText('pass')

        # Create button disables
        self.assertFalse(self.createButton.isEnabled())

        # Bob then erases both passwords and create button is still disabled
        self.pass_input.setText('')
        self.pass_repeat_input.setText('')
        self.assertFalse(self.createButton.isEnabled())

        # Bob then fills them again
        self.pass_input.setText('pass')
        self.pass_repeat_input.setText('pass')

        # And create button enables now
        self.assertTrue(self.createButton.isEnabled())
