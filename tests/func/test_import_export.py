#!/usr/bin/env python3

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import unittest
import pytest
import pyautogui
import sys
import os

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
        self.list = self.dbs.list

    def tearDown(self):
        self.settings.setValue('advanced/is_main_db', self.old_is_main_db)
        self.settings.setValue('advanced/main_db', self.old_main_db)

    def test_import_success(self):
        # Emily wants to import database so she goes to menu File -> Import database...
        file = self.window.menuBar().actions()[0]  # first is `File` submenu
        import_db = file.menu().actions()[1]       # second action is `Import database...`

        # File dialog appears and she chose her tar file
        file_dialog = self.file_dialog(('../tests/func/src/import_database.tar',))
        self.monkeypatch.setattr(QFileDialog, 'getOpenFileName', file_dialog)

        # Success message appears, Emily presses `Ok` button
        success_message = self.mess(
            'Імпорт',
            'Успішно імпортовано базу данних <i><b>import_database</b></i>')
        self.monkeypatch.setattr(QMessageBox, 'information', success_message)
        import_db.trigger()

        # Database appears in the list and on the disk
        self.checkDbInList('import_database')
        self.assertIn('import_database', getDbList())

    def test_import_fail(self):
        # Tom wants to import database
        file = self.window.menuBar().actions()[0]  # first is `File` submenu
        import_db = file.menu().actions()[1]       # second action is `Import database...`

        # File dialog appears and he chose his tar file
        file_dialog = self.file_dialog(('../tests/func/src/corrupted_few_files.tar',))
        self.monkeypatch.setattr(QFileDialog, 'getOpenFileName', file_dialog)

        # Error message appears saying that his file is corrupted, so Tom presses `Ok`
        self.monkeypatch.setattr(QMessageBox, 'critical', self.critical)
        import_db.trigger()

        # He then tries to import another database
        file_dialog = self.file_dialog(('../tests/func/src/corrupted_many_files.tar',))
        self.monkeypatch.setattr(QFileDialog, 'getOpenFileName', file_dialog)

        # Another error appears with the same message
        import_db.trigger()

    def test_export_warning(self):
        # Bob wants to export his database, so he goes to menu File -> Export database...
        file = self.window.menuBar().actions()[0]  # first is `File` submenu
        export_db = file.menu().actions()[2]       # second action is `Export database...`
        export_db.trigger()

        # Warning message appears saying that he needs to chose database first
        self.checkOnlyVisible(self.exportWarning)

    def test_export_success(self):
        # Lea wants to export her database, so she chose one in the list
        self.list.selected(Index('database'))

        # And presses Ctrl+E
        # File dialog appears and she chose path
        file_dialog = self.save_file_dialog('database', ('../tests/func/src/database.tar',))
        self.monkeypatch.setattr(QFileDialog, 'getSaveFileName', file_dialog)

        # Success message appears
        success_message = self.mess(
            'Експорт', 'Успішно експортовано базу данних <i><b>database</b></i>')
        self.monkeypatch.setattr(QMessageBox, 'information', success_message)

        pyautogui.hotkey("ctrl", "e")  # We press Ctrl+E here because of the dialogs
        QTest.qWait(100)

        # And Lea has database.tar on the disk now
        self.assertTrue(os.path.exists('../tests/func/src/database.tar'))

        # clean up
        os.remove('../tests/func/src/database.tar')

    def test_export_fail(self):
        # Toon wants to export his database, so he chose one in the list
        self.list.selected(Index('database'))

        # And presses Ctrl+E
        # File dialog appears and he chose / path
        file_dialog = self.save_file_dialog('database', ('/database.tar',))
        self.monkeypatch.setattr(QFileDialog, 'getSaveFileName', file_dialog)

        # Error message appears saying that export is unsuccessful
        self.monkeypatch.setattr(QMessageBox, 'critical', self.critical)

        pyautogui.hotkey("ctrl", "e")  # We press Ctrl+E here because of the dialogs
        QTest.qWait(100)

        # And there is no database.tar on the disk
        self.assertFalse(os.path.exists('/database.tar'))
