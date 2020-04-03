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
import os

from tests.base import AccsTest
from core.utils import *
from PyQtAccounts import *
from tests.func.test_import_export import ImportExportTest


class DbSaveTest(AccsTest):
    def setUp(self):
        super().setUp('import_database', 'import_database')
        self.form = self.accs.forms['edit']
        self.list = self.accs.list
        self.saveButton = self.form.createButton
        self.editButton = self.accs.panel.editButton
        self.name = self.form.nameInput
        self.showForm = self.accs.forms['show']

        self.db = open('src/import_database.db', 'rb').read()

    def tearDown(self):
        open('src/import_database.db', 'wb').write(self.db)

    def test_save_after_edit(self):
        # Ross wants to edit his account, so he chose it in the list and presses edit button
        self.list.selected(Index('firefox'))
        self.editButton.click()

        # He change account nickname and presses save button of edit form
        self.name.setText('Ross Geller')
        self.saveButton.click()

        # Ross then goes to menu: File -> Save
        file = self.win.menuBar().actions()[0]  # first is `File` submenu
        save = file.menu().actions()[1]         # second action is `Save`
        save.trigger()

        # Database is saved now, so he closes the database window, and there is no messages
        self.win.close()
        self.assertNotIn(self.win, self.window.windows)

        # Ross then opens database again to check is everything saved
        form = self.dbs.forms['open']
        self.list = self.dbs.list
        self.pass_input = form.passField.passInput
        self.list.selected(Index('import_database'))
        self.pass_input.setText('import_database')
        form.openButton.click()
        self.win = self.window.windows[1]
        self.accs = self.win.accs

        # He chose his account at the list
        self.accs.list.selected(Index('firefox'))

        # And he sees his name changed at the account show form
        self.assertEqual("Ім'я: Ross Geller", self.showForm.name.text())
