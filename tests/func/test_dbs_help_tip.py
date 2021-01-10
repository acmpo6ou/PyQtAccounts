#!/usr/bin/env python3

#  Copyright (c) 2020-2021. Kolvakh Bohdan
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
from PyQt5.QtWidgets import *
import unittest
import pytest
import os
import glob

from tests.base import DbsTest, SettingsMixin, init_src_folder
import core.utils
from core.const import *
from PyQtAccounts import *


class HelpTipTest(SettingsMixin, DbsTest):
    """
    This test class tests help tip of main window.
    """
    def setUp(self):
        """
        Here we do some setup.
        """
        DbsTest.setUp(self)  # this test is about databases
        SettingsMixin.setUp(self)  # help tip depends on settings

    def openDatabase(self):
        """
        We use this method to open `database` database.
        """
        self.dbs.list.selected(Index('database'))
        self.open_form.passField.passInput.setText('some_password')
        self.open_form.openButton.click()

    def test_no_dbs(self):
        """
        This test tests help tip when user has no databases.
        """
        # Ross opens up PyQtAccounts, he has no database yet
        self.monkeypatch.setattr(glob, 'glob', lambda path: [])
        window = Window()

        # There is help tip saying how he can create new database
        tip = window.dbs.tips['help']
        self.assertEqual(
            tip.text(), HELP_TIP_DB,
            'Help tip in main window has incorrect value when user'
            'has no databases!')

    def test_has_dbs(self):
        """
        This test tests help tip when user has databases.
        """
        # Emily opens up PyQtAccounts, she has some databases
        window = Window()

        # There is help tip saying that she need to chose database
        tip = window.dbs.tips['help']
        self.assertEqual(
            tip.text(), "Виберіть базу данних",
            'Help tip in main window has incorrect value when user'
            'has databases!')

    def test_delete_last_database(self):
        """
        Here we test how help tip will change when user deletes last database.
        """
        # Tom has one database called `database`
        window = Window()
        self.dbs = window.dbs
        self.open_form = window.dbs.forms['open']
        init_src_folder(self.monkeypatch)
        self.copyDatabase('database')

        # help tip says that he should chose database
        tip = window.dbs.tips['help']
        self.assertEqual(
            tip.text(), "Виберіть базу данних",
            'Help tip in main window has incorrect value when user'
            'has databases!')

        # Tom than opens his database
        self.openDatabase()

        # then he presses edit button on the panel
        self.dbs.panel.editButton.click()

        # and then he deletes his last database
        self.monkeypatch.setattr(
            QMessageBox, 'warning',
            self.mess(
                'Увага!',
                'Ви певні що хочете видалити базу данних <i><b>database</b></i>',
                QMessageBox.Yes))
        self.dbs.forms['edit'].deleteButton.click()

        # help tip message changes, telling Tom how he can create new database
        self.assertEqual(
            tip.text(), HELP_TIP_DB,
            'Help tip in main window has incorrect value when user'
            'has deleted his last database!')

    def test_delete_database_not_last(self):
        """
        Here we test how help tip will change when user deletes database and he
        has some remaining databases.
        """
        # Tom has two databases called `database` and `main`
        window = Window()
        self.dbs = window.dbs
        self.open_form = window.dbs.forms['open']
        init_src_folder(self.monkeypatch)
        self.copyDatabase('database')
        self.copyDatabase('main')

        # help tip says that he should chose database
        tip = window.dbs.tips['help']
        self.assertEqual(
            tip.text(), "Виберіть базу данних",
            'Help tip in main window has incorrect value when user'
            'has databases!')

        # Tom than opens his `database`
        self.openDatabase()

        # then he presses edit button on the panel
        self.dbs.panel.editButton.click()

        # and then he deletes his `database` which isn't last
        self.monkeypatch.setattr(
            QMessageBox, 'warning',
            self.mess(
                'Увага!',
                'Ви певні що хочете видалити базу данних <i><b>database</b></i>',
                QMessageBox.Yes))
        self.dbs.forms['edit'].deleteButton.click()

        # everything is OK and message of help tip hasn't changed
        self.assertEqual(
            tip.text(), "Виберіть базу данних",
            'Help tip in main window has incorrect value when user'
            'has databases!')
