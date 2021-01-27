#!/usr/bin/env python3

#  Copyright (c) 2020-2021. Bohdan Kolvakh
#  This file is part of PyQtAccounts.
#
#  PyQtAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyQtAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.
#
#  PyQtAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyQtAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.

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
import shutil
import sys

from tests.base import DbsTest, SettingsMixin
from core.utils import *
from PyQtAccounts import *


class SettingsTest(SettingsMixin, DbsTest):
    """
    This test class provides all functional tests for PyQtAccounts settings.
    """
    def setUp(self):
        """
        Here we setup DbsTest because this is a functional test about main
        window and also we setup SettingsMixin because this test is about
        settings, and SettingsMixin initializes in-memory file system.
        """
        DbsTest.setUp(self)
        SettingsMixin.setUp(self)

    def test_settings_show_menu(self):
        """
        Here we test whether settings show properly when we access them through
        menu.
        """
        # here we can't use self.menu() as it operates on self.window attribute
        # which we don't define
        window = Window()
        edit = window.menuBar().actions()[1]  # second is `Edit` submenu
        pref = edit.menu().actions()[0]
        pref.trigger()
        self.assertTrue(
            window.settings.visibility,
            "Settings aren't showed when user goes to "
            "menu: Edit -> Preferences!")

    def test_is_main_db_True(self):
        """
        Here we test main database feature of PyQtAccounts.
        """
        # Bob uses main database feature of PyQtAccounts, he has it turned on
        # and `main` is the main database.
        self.settings.setValue('advanced/is_main_db', True)
        self.settings.setValue('advanced/main_db', 'main')

        # He opens PyQtAccounts and see form for opening his `main` database.
        # And the title of this form says `Відкрити базу данних main`
        window = Window()
        self.assertIn(
            'main', window.dbs.forms['open'].title.text(),
            "The title of open database form is incorrect when user has main database"
            "feature turned on and he launches PyQtAccounts, it doesn't "
            "contain name of main database!")

        # Checkbox in settings is also checked
        self.assertTrue(
            window.settings.mainDbLayout.checkbox.isChecked(),
            "The checkbox in settings that represents main database feature"
            "isn't checked when user has this feature turned on!")

        # And combobox have `main` as current database
        self.assertEqual(
            'main', window.settings.mainDbLayout.dbs.currentText(),
            "Main database in combobox is incorrect - must be `main`!")

    def test_is_main_db_not_set(self):
        """
        Here we test main database feature of PyQtAccounts when it isn't set
        (i.e. we test its default settings). 
        """
        # Tom doesn't know about main database feature of PyQtAccounts yet.
        # He has it turned off by default.
        self.settings.remove('advanced/is_main_db')
        self.settings.remove('advanced/main_db')

        # He opens PyQtAccounts and there is no form for opening any database.
        # Title of open database form is empty.
        window = Window()
        self.assertEqual(
            '<b></b>', window.dbs.forms['open'].title.text(),
            "The title of open database form is incorrect when user has main database"
            "feature unset (i.e. by default turned off), title contains name "
            "of main database!")

        # Checkbox in settings is also unchecked
        self.assertFalse(
            window.settings.mainDbLayout.checkbox.isChecked(),
            "The checkbox in settings that represents main database feature"
            " is checked when user has main database feature unset"
            "(i.e. turned off).")

        # And combobox have `main` as current database
        self.assertEqual(
            'main', window.settings.mainDbLayout.dbs.currentText(),
            "Combobox must have `main` as main database when user"
            "hasn't defined main database feature.")

    def test_is_main_db_False(self):
        """
        Here we test main database feature of PyQtAccounts when it is turned
        off.
        """
        # Ross doesn't use main database feature of PyQtAccounts.
        # He turned it off by himself.
        # also it was time when he used it with `crypt` as main database
        self.settings.setValue('advanced/is_main_db', False)
        self.settings.setValue('advanced/main_db', 'crypt')

        # He opens PyQtAccounts and there is no form for opening any database.
        # Title of open database form is empty.
        window = Window()
        self.assertEqual(
            '<b></b>', window.dbs.forms['open'].title.text(),
            "The title of open database form is incorrect when user has main"
            " database feature turned off, title must be empty!")

        # Checkbox in settings is also unchecked
        self.assertFalse(
            window.settings.mainDbLayout.checkbox.isChecked(),
            "The checkbox in settings that represents main database feature"
            " is checked when user has this feature turned off!")

        # And combobox have `crypt` as current database
        self.assertEqual(
            'crypt', window.settings.mainDbLayout.dbs.currentText(),
            "Combobox must have `crypt` as main database even when user"
            " has this feature turned off but used it with `crypt` in the past!"
        )
