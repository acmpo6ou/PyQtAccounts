#!/usr/bin/env python3

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import unittest.mock
import pytest
import sys

sys.path.append('.')

from .base import BaseTest
from utils import *
from PyQtAccounts import *


class ImportExportTest(BaseTest):
    def setUp(self):
        self.settings = QSettings('PyTools', 'PyQtAccounts')
        self.old_is_main_db = self.settings.value('advanced/is_main_db', False, type=bool)
        self.old_main_db = self.settings.value('advanced/main_db', '', type=str)
        
        # Any database should be selected
        self.settings.setValue('advanced/is_main_db', False)
        super().setUp()

        self.exportWarning = self.dbs.tips['export']

    def tearDown(self):
        self.settings.setValue('advanced/is_main_db', self.old_is_main_db)
        self.settings.setValue('advanced/main_db', self.old_main_db)

    def test_import_success(self):
        # Emily wants to import database so she goes to menu File -> Import database...
        file = self.window.menuBar().actions()[0]  # first is `File` submenu
        import_db = file.menu().actions()[1]       # second action is `Import database...`

        # File dialog appears and she chose her tar file
        self.monkeypatch.setattr(QFileDialog, 'getOpenFileName', lambda *args, **kwargs: (
            '../tests/func/src/import_database.tar',))

        # Success message appears, Emily presses `Ok` button
        self.monkeypatch.setattr(QMessageBox, 'information',
                                 lambda *args, **kwargs: QMessageBox.Ok)
        import_db.trigger()

        # Database appears in the list and on the disk
        self.checkDbInList('import_database')
        self.assertIn('import_database', getDbList())

    def test_import_fail(self):
        # Tom wants to import database
        file = self.window.menuBar().actions()[0]  # first is `File` submenu
        import_db = file.menu().actions()[1]       # second action is `Import database...`

        # File dialog appears and he chose his tar file
        self.monkeypatch.setattr(QFileDialog, 'getOpenFileName', lambda *args, **kwargs: (
            '../tests/func/src/corrupted_few_files.tar',))

        # Error message appears saying that his file is corrupted, so Tom presses `Ok`
        self.monkeypatch.setattr(QMessageBox, 'critical',
                                 lambda *args, **kwargs: QMessageBox.Ok)
        import_db.trigger()

        # He then tries to import another database
        self.monkeypatch.setattr(QFileDialog, 'getOpenFileName', lambda *args, **kwargs: (
            '../tests/func/src/corrupted_many_files.tar',))

        # Another error appears with the same message
        import_db.trigger()

    def test_export_warning(self):
        # Bob wants to export his database, so he goes to menu File -> Export database...
        file = self.window.menuBar().actions()[0]  # first is `File` submenu
        export_db = file.menu().actions()[2]       # second action is `Export database...`
        export_db.trigger()

        # Warning message appears saying that he needs to chose database first
        self.checkOnlyVisible(self.exportWarning)
