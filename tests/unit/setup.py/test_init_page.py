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

from tests.base import UnitTest, init_accounts_folder
from setup import *

# this is text of initialization error message
INIT_ERROR = (
    "Помилка ініціалізації!\n"
    "Відсутнє мережеве з'єднання, або відмовлено у доступі"
    " на запис у папку інсталяції."
)


class InitPageTest(UnitTest):
    """
    This test class provides all tests for initialization page.
    """
    def test_page(self):
        """
        This test tests page itself.
        """
        # here we set environment variable to fake in-memory folder and create
        # initialization page
        self.monkeypatch.setenv('HOME', '/home/accounts')
        page = InitPage()

        # here we check some default attributes of init page.
        self.assertIsNone(page._thread, 
                          '_thread must be set to None when constructing instance')
        self.assertEqual(page.folder, '/home/accounts',
                         'folder attribute of InitPage must be set to'
                         '`/home/accounts` by default!')

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

    # @pytest.mark.skip
    def test_init(self):
        # Tom wants to initialize PyQtAccounts in his home directory
        init_accounts_folder()
        page = InitPage()
        self.assertEqual(page.browseLabel.text(), '/home/accounts')

        # Everything seems fine so he presses `Initialize` button
        page.initButton.click()

        # some time passes and initialization is complete
        def is_finished():
            assert page._thread.isFinished()
        self.qbot.waitUntil(is_finished, timeout=3000)

        # Progressbar shows 100% and program initialized with all its folder structure
        self.assertEqual(page.progress.value(), 100)
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/src'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/core'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/COPYING'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/CREDITS'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/change.log'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/setup.py'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/img'))


class FailTest(UnitTest):
    def test_init_fail_when_no_permissions(self):
        page = InitPage()
        page.folder = '/'  # we have no permissions to write in root folder
        page.initButton.click()

        def errors_visible():
            assert page.errors.visibility
        self.qbot.waitUntil(errors_visible)
        self.assertEqual(page.errors.toPlainText(), INIT_ERROR)
