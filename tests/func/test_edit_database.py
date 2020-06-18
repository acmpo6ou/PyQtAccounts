#!/usr/bin/env python3

# Copyright (c) 2020 Kolvah Bogdan
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
import shutil

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import unittest
import pytest
import sys
import os

from tests.base import DbsTest, init_src_folder, init_accounts_folder
from core.utils import *
from PyQtAccounts import *


class EditDbTest(DbsTest):
    """
    This test class provides all functional tests for edit database form.
    """
    def setUp(self):
        """
        Here we reassign some widely used variables. 
        """
        super().setUp()
        self.form = self.dbs.forms['edit']
        self.list = self.dbs.list

        self.editButton = self.dbs.panel.editButton

        self.open_form = self.dbs.forms['open']
        self.open_pass_input = self.open_form.passField.passInput

        self.name = self.form.nameInput
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput
        self.saveButton = self.form.createButton
        self.help = self.dbs.tips['help']

    def openDatabase(self, name='database', password='some_password'):
        """
        This method is used for opening database automatically.
        """
        self.list.selected(Index(name))
        self.open_pass_input.setText(password)
        self.open_form.openButton.click()

    def test_edit_db_warning(self):
        """
        Here we test warning that appears when we want to edit database that is
        not opened yet.
        """
        # Toon wants to edit database so he chose one from the list and presses edit button
        self.list.selected(Index('database'))
        self.editButton.click()

        # The error message appears saying that he can't edit database until he opens it
        self.checkOnlyVisible(self.dbs.tips['edit-w'])

        # So Toon opens database
        self.openDatabase()

        # There is no errors
        self.checkOnlyVisible(self.help)

        # and then he tries again
        self.editButton.click()

        # Edit database form appears
        self.checkOnlyVisible(self.form)

    def test_name_validation(self):
        """
        This test tests name validation when we edit database.
        """
        # Lea wants to edit database, so she opens one
        self.openDatabase()

        # Then she presses edit button
        self.editButton.click()

        # In the name and password fields she sees database name and password appropriately
        self.assertEqual(
            'database', self.name.text(),
            'Name field of edit database form is filled with'
            'incorrect data!')
        self.assertEqual(
            'some_password', self.pass_input.text(),
            'Password field of edit database form is filled with'
            'incorrect data!')
        self.assertEqual(
            'some_password', self.pass_repeat_input.text(),
            'Second password field of edit database form is filled with'
            'incorrect data!')

        # Lea changes database name to `another_database` then
        self.name.setText('another_database')

        # Everything is fine, she changes it back to `database`
        self.name.setText('database')

        # And there is no errors
        self.assertFalse(
            self.form.nameError.visibility,
            'Error message appears when user has changed name in name'
            'field to old database name!')
        self.assertFalse(
            self.form.nameFilledError.visibility,
            'Error filled message appears when name field of edit'
            'database form is filled!')

        # Save button is still enabled
        self.assertTrue(
            self.saveButton.isEnabled(),
            'Save button is disabled when user has changed name in name'
            'field to old database name!')

    def test_save_button(self):
        """
        Here we test save button.
        """
        # Tom wants to edit database
        self.openDatabase()
        self.editButton.click()

        # He changes the name and password
        self.name.setText('another_database')
        self.pass_input.setText('another_password')
        self.pass_repeat_input.setText('another_password')

        # And presses the save button
        self.saveButton.click()

        # Edit database form disappears
        self.checkOnlyVisible(self.help)

        # Database name changes in the list to `another_database` and it also
        # exists on disk
        self.checkDbInList('another_database')
        self.checkDbOnDisk('another_database')

        # And there is no longer `database` in the list, nor on the disk
        self.checkDbNotInList('database')
        self.checkDbNotOnDisk('database')

        # Tom tries then to open `another_database`
        self.openDatabase('another_database', 'another_password')

        # There is no errors
        self.checkOnlyVisible(self.help)

        # database renamed on the disk
        self.checkDbOnDisk('another_database')

        # Database window appears
        win = self.window.windows[
            1]  # first is main window, second is database one
        self.assertTrue(win.visibility, 'Database window isn\'t displayed!')

    def test_delete_db(self):
        """
        Here we test delete button of edit database form.
        """
        # we don't realy want to delete our real database so we copy it into the
        # fake file system
        init_src_folder(self.monkeypatch)
        self.copyDatabase('database')
        self.setUp()

        # Bob wants to delete database, so he opens it up and presses edit button
        self.openDatabase()
        self.editButton.click()

        # Then he presses delete button
        # Suddenly Bob changes his mind and presses `No` button of warning dialog that appears
        self.monkeypatch.setattr(
            QMessageBox, "warning",
            self.mess(
                'Увага!', 'Ви певні що хочете видалити базу '
                'данних <i><b>database</b></i>', QMessageBox.No))
        self.form.deleteButton.click()

        # Everything is fine database still in the list and exists on the disk
        QTest.qWait(2000)
        self.checkDbInList('database')
        self.checkDbOnDisk('database')

        # Then he decided to delete database
        self.monkeypatch.setattr(
            QMessageBox, "warning",
            self.mess(
                'Увага!', 'Ви певні що хочете видалити базу данних'
                ' <i><b>database</b></i>', QMessageBox.Yes))
        self.form.deleteButton.click()

        # And there in no longer database in the list, neither on the disk
        self.checkDbNotInList('database')
        self.checkDbNotOnDisk('database')

        # Edit form disappears
        self.checkOnlyVisible(self.help)

    def test_no_change(self):
        """
        Here we test what happens when user doesn't changes any thing.
        """
        # Tom wants to edit database
        self.openDatabase()
        self.editButton.click()

        # Suddenly he changes his mind and presses save button without any
        # change
        self.saveButton.click()

        # Edit database form disappears
        self.checkOnlyVisible(self.help)

        # `database` is still in the list and on the disk
        self.checkDbInList('database')
        self.checkDbOnDisk('database')

        # Then Tom opens `database` again
        self.openDatabase()

        # database window appears and everything is fine
        self.assertTrue(self.window.windows[1])
        self.checkOnlyVisible(self.help)
