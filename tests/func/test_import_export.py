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
import shutil

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import unittest
import pytest
import sys
import os

from tests.base import DbsTest, SettingsMixin, init_src_folder
from core.utils import *
import core.const
from PyQtAccounts import *


class ImportExportTest(DbsTest, SettingsMixin):
    """
    This test class provides all functional tests for import and export.
    """
    def setUp(self):
        """
        Here we reassign some widely used variables and do some other setup. 
        """
        # this mixin provides fake settings file that we will use bellow.
        SettingsMixin.setUp(self)

        # Any database shouldn't be selected
        self.settings.setValue('advanced/is_main_db', False)
        super().setUp()

        self.exportWarning = self.dbs.tips['export']
        self.list = self.dbs.list

        # first is `File` submenu, second action is `Import database...`
        self.import_db = self.menu(0, 1)

        init_src_folder(self.monkeypatch)

    def test_import_success(self):
        """
        Here we test import when it is successful.
        """
        # Emily wants to import database so she goes to menu File -> Import database...
        # File dialog appears and she chose her tar file
        file_dialog = self.import_database_dialog(
            ('tests/func/src/import_database.tar', ))
        QFileDialog.getOpenFileName = file_dialog

        # Success message appears, Emily presses `Ok` button
        success_message = self.mess(
            'Імпорт',
            'Успішно імпортовано базу данних <i><b>import_database</b></i>')
        QMessageBox.information = success_message
        self.import_db.trigger()

        # Database appears in the list and on the disk
        self.checkDbInList('import_database')
        self.checkDbOnDisk('import_database')

    def test_import_doesnt_ends_with_tar(self):
        """
        Here we test import when name of chosen by user tar file contains
        no `.tar` extension.
        """
        # Emily wants to import database so she goes to menu File -> Import database...
        # File dialog appears and she chose her tar file which is without extension
        file_dialog = self.import_database_dialog(
            ('tests/func/src/import_database', ))
        QFileDialog.getOpenFileName = file_dialog

        # Success message appears, Emily presses `Ok` button
        success_message = self.mess(
            'Імпорт',
            'Успішно імпортовано базу данних <i><b>import_database</b></i>')
        QMessageBox.information = success_message
        self.import_db.trigger()

        # Database appears in the list and on the disk
        self.checkDbInList('import_database')
        self.checkDbOnDisk('import_database')

    def test_import_fail(self):
        """
        Here we test import when it fails.
        """
        # Tom wants to import database
        # File dialog appears and he chose his tar file
        file_dialog = self.import_database_dialog(
            ('tests/func/src/corrupted_few_files.tar', ))
        QFileDialog.getOpenFileName = file_dialog

        # Error message appears saying that his file is corrupted, so Tom presses `Ok`
        QMessageBox.critical = self.critical
        self.import_db.trigger()

        # He then tries to import another database
        file_dialog = self.import_database_dialog(
            ('tests/func/src/corrupted_many_files.tar', ))
        QFileDialog.getOpenFileName = file_dialog

        # Another error appears with the same message
        self.import_db.trigger()

    def test_export_warning(self):
        """
        Here we test export warning that appears when we try to export database
        without actually chosing one.
        """
        # Bob wants to export his database, so he goes to menu File -> Export database...
        # first is `File` submenu, second action is `Export database...`
        export_db = self.menu(0, 2)
        export_db.trigger()

        # Warning message appears saying that he needs to chose database first
        self.checkOnlyVisible(self.exportWarning)

    def test_export_success(self):
        """
        Here we test export when it is successful.
        """
        # Lea wants to export her database, so she chose one in the list
        self.list.selected(Index('database'))

        # And presses Ctrl+E
        # File dialog appears and she chose path
        file_dialog = self.export_database_dialog(
            'database', ('/home/accounts/database.tar', ))
        QFileDialog.getSaveFileName = file_dialog

        # Success message appears
        success_message = self.mess(
            'Експорт',
            'Успішно експортовано базу данних <i><b>database</b></i>')
        QMessageBox.information = success_message

        # First is `File` submenu, third is `Export database...` action
        self.menu(0, 2).trigger()  # We do it here because of the dialogs

        # And Lea has database.tar on the disk now
        self.assertTrue(
            os.path.exists('/home/accounts/database.tar'),
            'Database tar file hasn\'t created while export '
            'operation is successful!')

    def test_export_fail(self):
        """
        Here we test export when it is fails.
        """
        # Toon wants to export his database, so he chose one in the list
        self.list.selected(Index('database'))

        # And presses Ctrl+E
        # File dialog appears and he chose / path
        file_dialog = self.export_database_dialog('database',
                                                  ('/database.tar', ))
        QFileDialog.getSaveFileName = file_dialog

        # Error message appears saying that export is unsuccessful
        QMessageBox.critical = self.critical

        # First is `File` submenu, third is `Export database...` action
        self.menu(0, 2).trigger()  # We do it here because of the dialogs

        # And there is no database.tar on the disk
        self.assertFalse(os.path.exists('/database.tar'))
