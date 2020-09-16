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
    """
    This test class provides all functional tests for open database form.
    """
    def setUp(self):
        """
        Here we reassign some widely used variables. 
        """
        super().setUp()
        self.form = self.dbs.forms['open']
        self.list = self.dbs.list
        self.pass_input = self.form.passField.passInput

    def test_form_show(self):
        """
        Here we test whether open database form appears when we chose database
        in the database list also this test checks content of the form.
        """
        # Bob wants to open his database, so he clicks at the `crypt` on the database list
        self.list.selected(Index('crypt'))

        # open database form appears
        self.checkOnlyVisible(self.form)

        # There is title that says `Відкрити базу данних crypt`
        self.assertIn(
            'crypt', self.form.title.text(),
            'Title of open database form does not contains name of'
            'selected database!')

    def test_form_doesnt_show_if_db_already_opened(self):
        """
        Here we test that open database form does not appears when database that
        we select from list is already opened.
        """
        # Ross opened database
        self.list.selected(Index('database'))
        self.pass_input.setText('some_password')
        self.form.openButton.click()

        # Then he chose same database in the list again
        self.list.selected(Index('database'))

        # The message appears saying that he already opened this database
        self.checkOnlyVisible(self.dbs.tips['already-open'])

    def test_password_and_open_validation(self):
        """
        Here we test password validation.
        """
        # Tom wants to open his database called `database`
        self.list.selected(Index('database'))

        # He accidentally types wrong password and hits Enter
        QTest.keyClicks(self.pass_input, 'password')
        QTest.keyClick(self.pass_input, Qt.Key_Enter)

        # The error message appears saying that the password is incorrect
        error = self.form.incorrectPass
        self.assertTrue(
            error.visibility,
            'The error message does not appears when password of the'
            'open database form is incorrect!')

        # Tom then corrects password and now presses `open` button
        self.pass_input.setText('some_password')
        self.form.openButton.click()

        # The error disappears
        self.assertFalse(
            error.visibility,
            'The error message about incorrect password of the open'
            'database form does not disappears when password is'
            'corrected!')

        # Database window appears
        win = self.window.windows[
            1]  # first is main window, second is database one
        self.assertTrue(
            win.visibility,
            'Database window does not appears when user presses '
            'open button of open database form!')

        # It has all needed properties
        self.assertTrue(isinstance(win, DbWindow),
                        'Created window is not a database window!')
        self.assertTrue(win.ask)
        self.assertEqual(win.password, b'some_password',
                         'Password of created database window is incorrect!')
        self.assertEqual('database', win.windowTitle(),
                         'Title of created database window is incorrect!')
        self.assertEqual('database', win.name,
                         'Name of created database window is incorrect!')
        self.assertEqual(openDatabase('database', b'some_password'), win.db,
                         'Database of created database window is incorrect!')
