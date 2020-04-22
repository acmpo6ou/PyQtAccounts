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

from unittest.mock import Mock
import pytest
import os.path
import os
import sys
import shutil

from tests.base import UnitTest, init_accounts_folder
from setup import *

EXPECTED_RUN_SH_TEXT = (
    '#!/bin/bash\n\n'
    'cd /home/accounts/PyQtAccounts/\n'
    'export PYTHONPATH="$PYTHONPATH:/home/accounts/PyQtAccounts/"\n'
    'python3 PyQtAccounts.py'
)

EXPECTED_SHORTCUT_TEXT = (
    '[Desktop Entry]\n'
    'Name=PyQtAccounts\n'
    'Type=Application\n'
    'Comment=Simple account database manager.\n'
    'Terminal=false\n'
    'Icon=/home/accounts/PyQtAccounts/img/icon.svg\n'
    'Exec=/bin/bash /home/accounts/PyQtAccounts/run.sh \n'
)


class FinishPageTest(UnitTest):
    def setUp(self):
        self.page = FinishPage()
        self.page._parent = Mock()
        self.page._parent.initPage = InitPage()

        self.initPage = self.page._parent.initPage
        self.initPage.folder = '/home/accounts'

        init_accounts_folder()
        os.mkdir('/home/accounts/PyQtAccounts')
        os.mkdir('/home/accounts/Desktop')
        os.makedirs('/home/accounts/.local/share/applications/', exist_ok=True)

    def tearDown(self):
        if os.path.exists('/dev/shm/accounts'):
            shutil.rmtree('/dev/shm/accounts')

    def test_content(self):
        page = FinishPage()
        self.assertEqual(page.title.text(), '<h4>Finish</h4>')
        self.assertEqual(page.text.text(), 'Успішно установлено PyQtAccounts!')

    def test_init_page_menu_and_desktop(self):
        # Checkboxes of init page for menu and desktop shortcuts are checked by default
        self.page.initializePage()

        self.assertEqual(EXPECTED_RUN_SH_TEXT,
                         open('/home/accounts/PyQtAccounts/run.sh').read())
        self.assertEqual(EXPECTED_SHORTCUT_TEXT,
                         open('/home/accounts/Desktop/PyQtAccounts.desktop').read())
        self.assertEqual(EXPECTED_SHORTCUT_TEXT, open(
            '/home/accounts/.local/share/applications/PyQtAccounts.desktop').read())

    def test_init_page_menu_no_desktop(self):
        # Checkboxes of init page for menu and desktop shortcuts are checked by default
        self.initPage.desktopCheckbox.setChecked(False)
        self.page.initializePage()

        self.assertEqual(EXPECTED_RUN_SH_TEXT,
                         open('/home/accounts/PyQtAccounts/run.sh').read())

        self.assertFalse(os.path.exists('/home/accounts/Desktop/PyQtAccounts.desktop'))

        self.assertEqual(EXPECTED_SHORTCUT_TEXT, open(
            '/home/accounts/.local/share/applications/PyQtAccounts.desktop').read())

    def test_init_page_desktop_no_menu(self):
        # Checkboxes of init page for menu and desktop shortcuts are checked by default
        self.initPage.menuCheckbox.setChecked(False)
        self.page.initializePage()

        self.assertEqual(EXPECTED_RUN_SH_TEXT,
                         open('/home/accounts/PyQtAccounts/run.sh').read())
        self.assertEqual(EXPECTED_SHORTCUT_TEXT,
                         open('/home/accounts/Desktop/PyQtAccounts.desktop').read())
        self.assertFalse(os.path.exists(
            '/home/accounts/.local/share/applications/PyQtAccounts.desktop'))
