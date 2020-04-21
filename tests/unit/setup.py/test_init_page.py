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
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtCore


from unittest.mock import Mock
import pytest
import os

from tests.base import UnitTest
from setup import *

INIT_ERROR = ("Помилка ініціалізації!\n"
              "Відсутнє мережеве з'єднання, або відмовлено у доступі"
              " на запис у папку інсталяції.")


class InitPageTest(UnitTest):
    def test_page(self):
        self.monkeypatch.setenv('HOME', '/home/accounts')
        page = InitPage()

        self.assertIsNone(page._thread)
        self.assertEqual(page.folder, '/home/accounts')

        self.assertEqual(page.title.text(), '<h4>Ініціалізація</h4>')
        self.assertEqual(page.initLabel.text(),
                         'Виберіть папку в яку ви хочете встановити PyQtAccounts:')
        self.assertEqual(page.browseLabel.text(), '/home/accounts')

        self.assertTrue(page.menuCheckbox.isChecked())
        self.assertTrue(page.desktopCheckbox.isChecked())

    def test_browse(self):
        def mock_browse(parent, title, folder, dirs_only_flag):
            assert title == 'Installation directory'
            assert folder == os.getenv('HOME')
            assert dirs_only_flag == QFileDialog.ShowDirsOnly
            return '/home/accounts/myprograms'

        self.monkeypatch.setattr(QFileDialog, 'getExistingDirectory', mock_browse)

        page = InitPage()
        page.browseButton.click()

        self.assertEqual(page.folder, '/home/accounts/myprograms')
        self.assertEqual(page.browseLabel.text(), '/home/accounts/myprograms')

    def test_is_complete(self):
        page = InitPage()
        page.progress.setValue(0)
        self.assertFalse(page.isComplete())

        page.progress.setValue(100)
        self.assertTrue(page.isComplete())

    def test_init_already(self):
        self.monkeypatch.setattr('os.listdir', lambda path: ['PyQtAccounts'])
        page = InitPage()
        page.initButton.click()
        self.assertEqual(page.progress.value(), 100)


class FailTest(UnitTest):
    def test_init_fail_when_no_permissions(self):
        page = InitPage()
        thread = Mock()
        Initialize.moveToThread = lambda *args: None
        self.monkeypatch.setattr('PyQt5.QtCore.QThread', lambda *args: thread)

        page.folder = '/'  # we have no permissions to write in root folder
        page.initButton.click()

        QTest.qWait(100)
        self.assertTrue(page.errors.visibility)
        print(repr(page.errors.toPlainText()))
        self.assertEqual(page.errors.toPlainText(), INIT_ERROR)
