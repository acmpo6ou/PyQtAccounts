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

from PyQt5.QtCore import *
from PyQt5.QtTest import QTest
import unittest
import sys

from tests.base import DbsTest
from core.utils import *
from PyQtAccounts import *


class SettingsTest(DbsTest):
    def setUp(self):
        os.environ['TESTING'] = 'True'
        self.settings = QSettings('PyToolsTest', 'PyQtAccounts')
        self.old_is_main_db = self.settings.value('advanced/is_main_db', False, type=bool)
        self.old_main_db = self.settings.value('advanced/main_db', '', type=str)

    def tearDown(self):
        self.settings.setValue('advanced/is_main_db', self.old_is_main_db)
        self.settings.setValue('advanced/main_db', self.old_main_db)

    def test_settings_show_menu(self):
        window = Window()
        edit = window.menuBar().actions()[1]  # second is `Edit` submenu
        pref = edit.menu().actions()[0]
        pref.trigger()
        self.assertTrue(window.settings.visibility)

    def test_is_main_db_True(self):
        # Bob uses main database feature of PyQtAccounts, he has it turned on
        # and `main` is the main database.
        self.settings.setValue('advanced/is_main_db', True)
        self.settings.setValue('advanced/main_db', 'main')

        # He opens PyQtAccounts and see form for opening his `main` database.
        # And the title of this form says `Відкрити базу данних main`
        window = Window()
        self.assertIn('main', window.dbs.forms['open'].title.text())

        # Checkbox in settings is also checked
        self.assertTrue(window.settings.mainDbLayout.checkbox.isChecked())

        # And combobox have `main` as current database
        self.assertEqual('main', window.settings.mainDbLayout.dbs.currentText())

    def test_is_main_db_not_set(self):
        # Tom doesn't know about main database feature of PyQtAccounts yet.
        # He has it turned off by default.
        self.settings.remove('advanced/is_main_db')
        self.settings.remove('advanced/main_db')

        # He opens PyQtAccounts and there is no form for opening any database.
        # Title of open database form is empty.
        window = Window()
        self.assertEqual('<b></b>', window.dbs.forms['open'].title.text())

        # Checkbox in settings is also unchecked
        self.assertFalse(window.settings.mainDbLayout.checkbox.isChecked())

        # And combobox have `main` as current database
        self.assertEqual('main', window.settings.mainDbLayout.dbs.currentText())

    def test_is_main_db_False(self):
        # Ross doesn't use main database feature of PyQtAccounts.
        # He turned it off by himself.
        self.settings.setValue('advanced/is_main_db', False)
        self.settings.setValue('advanced/main_db', 'crypt')

        # He opens PyQtAccounts and there is no form for opening any database.
        # Title of open database form is empty.
        window = Window()
        self.assertEqual('<b></b>', window.dbs.forms['open'].title.text())

        # Checkbox in settings is also unchecked
        self.assertFalse(window.settings.mainDbLayout.checkbox.isChecked())

        # And combobox have `crypt` as current database
        self.assertEqual('crypt', window.settings.mainDbLayout.dbs.currentText())
