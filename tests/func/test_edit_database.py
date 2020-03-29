#!/usr/bin/env python3

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
import unittest
import pytest
import sys
import os

sys.path.append('.')

from .base import BaseTest
from utils import *
from PyQtAccounts import *


class EditDbTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.form = self.dbs.forms['edit']
        self.list = self.dbs.list

        self.open_form = self.dbs.forms['open']
        self.open_pass_input = self.open_form.passField.passInput

        self.name = self.form.nameInput
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput
        self.saveButton = self.form.createButton

        self.help = self.dbs.tips['help']

    def openDatabase(self, name='database', password='some_password'):
        self.list.selected(Index(name))
        self.open_pass_input.setText(password)
        self.open_form.openButton.click()

    def test_edit_db_warning(self):
        # Toon wants to edit database so he chose one from the list and presses edit button
        self.list.selected(Index('database'))
        self.dbs.panel.editButton.click()

        # The error message appears saying that he can't edit database until he opens it
        self.checkOnlyVisible(self.dbs.tips['edit-w'], self.dbs)

        # So Toon opens database
        self.openDatabase()

        # There is no errors
        self.checkOnlyVisible(self.help, self.dbs)

        # and then he tries again
        self.dbs.panel.editButton.click()

        # Edit database form appears
        self.checkOnlyVisible(self.form, self.dbs)

    def test_name_validation(self):
        # Lea wants to edit database, so she opens one
        self.openDatabase()

        # Then she presses edit button
        self.dbs.panel.editButton.click()

        # In the name and password fields she sees database name and password appropriately
        self.assertEqual('database', self.name.text())
        self.assertEqual('some_password', self.pass_input.text())
        self.assertEqual('some_password', self.pass_repeat_input.text())

        # Lea changes database name to `another_database` then
        self.name.setText('another_database')

        # Everything is fine, she changes it back to `database`
        self.name.setText('database')

        # And there is no errors
        self.assertFalse(self.form.nameError.visibility)
        self.assertFalse(self.form.nameFilledError.visibility)

        # Save button is still enabled
        self.assertTrue(self.saveButton.isEnabled())

    def test_save_button(self):
        # pre-saving database
        salt = open('../src/database.bin', 'rb').read()
        db = open('../src/database.db', 'rb').read()

        # Tom wants to edit database
        self.openDatabase()

        # He changes the name and password
        self.name.setText('another_database')
        self.pass_input.setText('another_password')
        self.pass_repeat_input.setText('another_password')

        # And presses the save button
        self.saveButton.click()

        # Edit database form disappears
        self.checkOnlyVisible(self.help, self.dbs)

        # Database name changes in the list
        self.checkDbInList('another_database')

        # And there is no longer `database` in the list
        self.checkDbNotInList('database')

        # Tom tries then to open `another_database`
        self.openDatabase('another_database', 'another_password')

        # There is no errors
        self.checkOnlyVisible(self.help, self.dbs)

        # database renamed on the disk
        self.assertIn('another_database', getDbList())

        # Database window appears
        win = self.window.windows[1]  # first is main window, second is database one
        self.assertTrue(win.visibility)

        # restoring database
        open('../src/database.bin', 'wb').write(salt)
        open('../src/database.db', 'wb').write(db)

        # cleaning up
        os.remove('../src/another_database.bin')
        os.remove('../src/another_database.db')
