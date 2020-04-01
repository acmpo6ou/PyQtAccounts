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
import unittest
import pytest
import sys

from tests.base import DbsTest
from core.utils import *
from PyQtAccounts import *
from core.getaki import openDatabase


class OpenDbTest(DbsTest):
    def setUp(self):
        super().setUp()
        self.form = self.dbs.forms['open']
        self.list = self.dbs.list
        self.pass_input = self.form.passField.passInput

    def test_form_show(self):
        # Bob wants to open his database, so he clicks at the `crypt` on the database list
        self.list.selected(Index('crypt'))

        # open database form appears
        self.checkOnlyVisible(self.form)

        # There is title that says `Відкрити базу данних crypt`
        self.assertIn('crypt', self.form.title.text())

    def test_form_doesnt_show_if_db_already_opened(self):
        # Ross opened database
        self.list.selected(Index('database'))
        self.pass_input.setText('some_password')
        self.form.openButton.click()

        # Then he chose same database in the list again
        self.list.selected(Index('database'))

        # The message appears saying that he already opened this database
        self.checkOnlyVisible(self.dbs.tips['already-open'])

    def test_password_and_open_validation(self):
        # Tom wants to open his database called `database`
        self.list.selected(Index('database'))

        # He accidentally types wrong password and hits Enter
        QTest.keyClicks(self.pass_input, 'password')
        QTest.keyClick(self.pass_input, Qt.Key_Enter)

        # The error message appears saying that the password is incorrect
        error = self.form.incorrectPass
        self.assertTrue(error.visibility)

        # Tom then corrects password and now presses `open` button
        self.pass_input.setText('some_password')
        self.form.openButton.click()

        # The error disappears
        self.assertFalse(error.visibility)

        # Database window appears
        win = self.window.windows[1]  # first is main window, second is database one
        self.assertTrue(win.visibility)

        # It has all needed properties
        self.assertTrue(isinstance(win, DbWindow))
        self.assertTrue(win.ask)
        self.assertEqual(win.password, b'some_password')
        self.assertEqual('database', win.windowTitle())
        self.assertEqual('database', win.name)
        self.assertEqual(openDatabase('database', b'some_password'), win.db)
