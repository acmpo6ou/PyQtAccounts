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
import pytest
import pyautogui
import sys
import os

sys.path.append('.')

from tests.base import DbsTest
from core.utils import getDbList
from PyQtAccounts import *


class CreateDbTest(DbsTest):
    '''
    Next 3 tests are testing does create database form appears whether we click on the
    `+` button or through Menu -> File -> New database... or Ctrl+N key sequences
    '''

    def setUp(self):
        super().setUp()
        self.form = self.dbs.forms['create']
        self.name = self.form.nameInput
        self.nameError = self.form.nameError
        self.nameFilledError = self.form.nameFilledError
        self.passFilledError = self.form.passFilledError
        self.passEqError = self.form.passEqError
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput
        self.createButton = self.form.createButton

    def test_create_db_ctrl_n(self):
        pyautogui.hotkey("ctrl", "n")
        QTest.qWait(100)
        self.checkOnlyVisible(self.form)

    def test_create_db_click(self):
        self.dbs.panel.addButton.click()
        self.checkOnlyVisible(self.form)

    def test_create_db_menu(self):
        file = self.window.menuBar().actions()[0]  # first is `File` submenu
        new_db = file.menu().actions()[0]  # first action is `New database...`
        new_db.trigger()
        self.checkOnlyVisible(self.form)

    def test_valid_db_name(self):
        # Bob has two databases called `main` and `crypt`.
        # He wants to create new one:
        self.dbs.panel.addButton.click()

        # He starts typing `cry` at the name input.
        QTest.keyClicks(self.name, 'cry')

        # There is now errors appearing
        self.assertFalse(self.nameError.visibility)

        # He then types `pt` at the name input, so the name in the input (`crypt`)
        # is the same as the name of database he already has
        QTest.keyClicks(self.name, 'pt')

        # The error message appears saying that the database with such name already exists.
        self.assertTrue(self.nameError.visibility)

        # Then Bob types `2` to change name from `crypt` to `crypt2`
        QTest.keyClick(self.name, '2')

        # The error message disappears
        self.assertFalse(self.nameError.visibility)

        # He then erases the name input
        self.name.setText('')

        # Another error appears saying that he needs to fill self.name field
        self.assertTrue(self.nameFilledError.visibility)

    def test_name_symbols_validation(self):
        # Toon wants to create database
        self.dbs.panel.addButton.click()

        # He then types `my data/base@!&%` to the name field
        self.name.setText('my data/base@!&%')

        # Also Toon types password and presses create button
        self.pass_input.setText('something')
        self.pass_repeat_input.setText('something')
        self.createButton.click()

        # `mydatabase` appears at the database list, cleaned name without any unallowed symbols
        self.checkDbInList('mydatabase')

        # And it actually on disk at the `src` folder
        self.assertIn('mydatabase', getDbList())

        # clean up
        os.remove('src/mydatabase.db')
        os.remove('src/mydatabase.bin')

    def test_valid_password(self):
        # Tom wants to create new database
        self.dbs.panel.addButton.click()

        # First he types name

        QTest.keyClicks(self.name, 'somedb')

        # Then he types password to first password input
        QTest.keyClicks(self.pass_input, 'password123')

        # The error message appears saying that both passwords aren't equal,
        # because first input is filled and the second is not
        self.assertTrue(self.passEqError.visibility)

        # Tom then fills second password field with the same password
        QTest.keyClicks(self.pass_repeat_input, 'password123')

        # The error disappears
        self.assertFalse(self.passEqError.visibility)

        # He then erase both password fields
        self.pass_input.setText('')
        self.pass_repeat_input.setText('')

        # Another error appears saying that he needs to fill password fields
        self.assertTrue(self.passFilledError.visibility)

        # Tom fills them again
        QTest.keyClicks(self.pass_input, 'password123')
        QTest.keyClicks(self.pass_repeat_input, 'password123')

        # End there is no errors
        self.assertFalse(self.passEqError.visibility)
        self.assertFalse(self.passFilledError.visibility)

    def test_generate_pass(self):
        # Ross wants to create new database
        self.dbs.panel.addButton.click()

        # He doesn't want to invent password by himself
        # So he press the `generate` button
        gen = self.form.generateButton
        gen.click()

        # The generate password dialog appears
        dialog = self.form.dialog
        self.assertTrue(dialog.visibility)

        # He lefts everything as it is and press the `generate` button of the dialog
        dialog.buttonGenerate.click()

        # Randomly generated password appears in both password fields of create database form
        self.assertIsNot(self.pass_input.text(), '')
        self.assertIsNot(self.pass_repeat_input.text(), '')
        self.assertEqual(self.pass_input.text(), self.pass_repeat_input.text())

    def test_create_button_enabled(self):
        # Lea wants to create new database, so she opens up PyQtAccounts
        # and presses the `+` button
        self.dbs.panel.addButton.click()

        # The create database form appears and `create` button is disabled
        create = self.createButton
        self.assertFalse(create.isEnabled())

        # She types database name in the name input

        QTest.keyClicks(self.name, 'somedb')

        # The `create` button is still disabled
        self.assertFalse(create.isEnabled())

        # She then generates password via `generate` button
        gen = self.form.generateButton
        gen.click()
        dialog = self.form.dialog
        dialog.buttonGenerate.click()

        # `create` button enables now
        self.assertTrue(create.isEnabled())

        # Lea then changes name of the database to `main` which is already taken
        self.name.setText('main')

        # `create` button disables
        self.assertFalse(create.isEnabled())

        # She then erases name input
        self.name.setText('')

        # `create` button is still disabled
        self.assertFalse(create.isEnabled())

        # Lea types old name again
        self.name.setText('somedb')

        # `create` button enables now
        self.assertTrue(create.isEnabled())

        # She changes password in the first field to something else
        # so both passwords aren't equal
        self.pass_input.setText('some_password')

        # `create` button disables again
        self.assertFalse(create.isEnabled())

        # Lea then erases all password fields
        self.pass_input.setText('')
        self.pass_repeat_input.setText('')

        # `create` button is still disabled
        self.assertFalse(create.isEnabled())

        # and she generates password again
        self.pass_input.setText('some_password')
        self.pass_repeat_input.setText('some_password')

        # `create` button enables
        self.assertTrue(create.isEnabled())

    def test_cancel_button(self):
        dbs = self.dbs
        # Emily accidentally presses the `+` button
        dbs.panel.addButton.click()

        # She didn't want it so she just presses `cancel` button to hide the create form
        dbs.forms['create'].cancelButton.click()

        # End the form disappears
        tip = dbs.tips['help']
        self.checkOnlyVisible(tip)

    def test_create_button(self):
        # Toon wants to create new database
        self.dbs.panel.addButton.click()

        # He fills name and password fields
        QTest.keyClicks(self.name, 'somedb')
        QTest.keyClicks(self.pass_input, 'some_password')
        QTest.keyClicks(self.pass_repeat_input, 'some_password')

        # Everything is fine so he presses `create` button
        self.createButton.click()

        # The create form disappears
        self.checkOnlyVisible(self.dbs.tips['help'])

        # `somedb` appears at the database list
        self.checkDbInList('somedb')

        # And it actually on disk at the `src` folder
        self.assertIn('somedb', getDbList())

        # clean up
        os.remove('src/somedb.db')
        os.remove('src/somedb.bin')
