#!/usr/bin/env python3

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import unittest
import pytest
import sys
import os

sys.path.append('.')

from tests.base import FuncTest
from core.utils import *
from PyQtAccounts import *


class EditDbTest(FuncTest):
    def setUp(self):
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

        # pre-saving database
        self.salt = open('src/database.bin', 'rb').read()
        self.db = open('src/database.db', 'rb').read()

    def tearDown(self):
        # restoring database
        open('src/database.bin', 'wb').write(self.salt)
        open('src/database.db', 'wb').write(self.db)

        # cleaning up
        try:
            os.remove('src/another_database.bin')
            os.remove('src/another_database.db')
        except Exception:
            pass

    def openDatabase(self, name='database', password='some_password'):
        self.list.selected(Index(name))
        self.open_pass_input.setText(password)
        self.open_form.openButton.click()

    def test_edit_db_warning(self):
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
        # Lea wants to edit database, so she opens one
        self.openDatabase()

        # Then she presses edit button
        self.editButton.click()

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

        # Database name changes in the list
        self.checkDbInList('another_database')

        # And there is no longer `database` in the list
        self.checkDbNotInList('database')

        # Tom tries then to open `another_database`
        self.openDatabase('another_database', 'another_password')

        # There is no errors
        self.checkOnlyVisible(self.help)

        # database renamed on the disk
        self.assertIn('another_database', getDbList())

        # Database window appears
        win = self.window.windows[1]  # first is main window, second is database one
        self.assertTrue(win.visibility)

    def test_delete_db(self):
        # Bob wants to delete database, so he opens it up and presses edit button
        self.openDatabase()
        self.editButton.click()

        # Then he presses delete button
        # Suddenly Bob changes his mind and presses `No` button in warning dialog that appears
        self.monkeypatch.setattr(QMessageBox, "warning",
            self.mess('Увага!',
                      'Ви певні що хочете видалити базу данних <i><b>database</b></i>',
                      QMessageBox.No))
        self.form.deleteButton.click()

        # Everything is fine database still in the list and exists on the disk
        self.checkDbInList('database')
        self.assertIn('database', getDbList())

        # Then he decided to delete database
        self.monkeypatch.setattr(QMessageBox, "warning",
            self.mess('Увага!',
                      'Ви певні що хочете видалити базу данних <i><b>database</b></i>',
                      QMessageBox.Yes))
        self.form.deleteButton.click()

        # And there in no longer database in the list, neither on the disk
        self.checkDbNotInList('database')
        self.assertNotIn('database', getDbList())

        # Edit form disappears
        self.checkOnlyVisible(self.help)
