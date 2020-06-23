#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh Bogdan
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
import os

from tests.base import AccsTest, init_accounts_folder, init_src_folder
from core.utils import *
from PyQtAccounts import *


class DbSaveTest(AccsTest):
    """
    This test class provides all functional tests for database window save
    operation.
    """
    def setUp(self):
        """
        Here we reassign some widely used variables and initialize in-memory
        file system.
        """
        # here we open database using setUp method from AccsTest superclass
        super().setUp('import_database', 'import_database')

        self.form = self.accs.forms['edit']
        self.list = self.accs.list
        self.saveButton = self.form.createButton
        self.editButton = self.accs.panel.editButton
        self.name = self.form.nameInput
        self.email = self.form.emailInput

        # and here we initialize in-memory file system
        init_src_folder(self.monkeypatch)
        self.copyDatabase('import_database')

    def openDatabase(self):
        """
        This method opens and returns database window.
        """
        window = Window()
        dbs = window.dbs
        form = dbs.forms['open']
        _list = dbs.list
        pass_input = form.passField.passInput
        _list.selected(Index('import_database'))
        pass_input.setText('import_database')
        form.openButton.click()
        win = window.windows[1]
        return win

    def test_save_after_edit(self):
        """
        Here we test saving of database through menu of database window.
        """
        # Ross wants to edit his account, so he chose it in the list and presses edit button
        self.list.selected(Index('firefox'))
        self.editButton.click()

        # He change account nickname and presses save button of edit form
        self.name.setText('Ross Geller')
        self.saveButton.click()

        # Ross then goes to menu: File -> Save
        self.account_menu(0, 1).trigger()

        # Database is saved now, so he closes the database window, and there is no messages
        self.win.close()
        self.assertNotIn(
            self.win, self.window.windows,
            "User closed the window but it still in windows list!")
        self.window.close()
        del self.window

        # Ross then opens database again to check is everything saved
        win = self.openDatabase()
        accs = win.accs

        # He chose his account at the list
        accs.list.selected(Index('firefox'))

        # And he sees his name changed at the account show form
        self.assertEqual(
            "Ім'я: Ross Geller", accs.forms['show'].name.text(),
            'Name of account is not changed after database was'
            'saved!')

    def test_save_message_Yes(self):
        """
        Here we test closing of database window when there are unsaved changes
        and user presses `Yes` at confirmation dialog.
        """
        # Lea wants to edit her account, so she chose it in the list
        self.list.selected(Index('firefox'))
        self.editButton.click()

        # She change her e-mail to `spam@python.org` and presses save button
        self.email.setText('spam@python.org')
        self.saveButton.click()

        # But then Lea changed her mind and closes database window
        # Message appears asking her about unsaved changes
        # Lea presses `Yes`
        self.monkeypatch.setattr(
            QMessageBox, 'question',
            self.mess('Увага!', 'Ви певні що хочете вийти?\n'
                      'Усі незбережені зміни буде втрачено!\n'
                      'Натисніть Ctrl+S аби зберегти зміни.',
                      button=QMessageBox.Yes))
        self.win.close()

        # Database window is closed now and Lea closes PyQtAccounts
        self.assertNotIn(
            self.win, self.window.windows,
            'Database window is closed but it is still in windows'
            'list!')
        self.window.close()
        del self.window

        # She then opens database again to check that changes aren't saved
        win = self.openDatabase()
        accs = win.accs

        # She chose her account in the list
        accs.list.selected(Index('firefox'))

        # And sees that her e-mail is such as it was
        self.assertEqual(
            "E-mail: firefox@gmail.com", accs.forms['show'].email.text(),
            "Database window was closed discarding all changes but"
            "changes are saved!")

    def test_save_message_No(self):
        """
        Here we test closing of database window when there are unsaved changes
        and user presses `No` at confirmation dialog.
        """
        # Lea wants to edit her account again, so she chose it in the list
        self.list.selected(Index('firefox'))
        self.editButton.click()

        # She change her e-mail to `spam@python.org` and presses save button
        self.email.setText('spam@python.org')
        self.saveButton.click()

        # But then Lea changed her mind and closes database window
        # Message appears asking her about unsaved changes
        # Lea presses `No`
        self.monkeypatch.setattr(
            QMessageBox, 'question',
            self.mess('Увага!', 'Ви певні що хочете вийти?\n'
                      'Усі незбережені зміни буде втрачено!\n'
                      'Натисніть Ctrl+S аби зберегти зміни.',
                      button=QMessageBox.No))
        self.win.close()

        # Database window is still opened
        self.assertIn(
            self.win, self.window.windows,
            "Database window isn't closed but it is no loner in "
            "windows list after user tries to close database window when "
            "there are unsaved changes and user presses `No` at "
            "confirmation dialog!")

        # Lea then change her e-mail back to `firefox@gmail.com` as it was and saves it
        self.email.setText('firefox@gmail.com')
        self.saveButton.click()

        # Then she closes database window and there is now messages
        self.monkeypatch.setattr(QMessageBox, 'question', self.mess_showed)
