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

# this constant represents text of run.sh file that PyQtAccounts installation wizard must generate.
EXPECTED_RUN_SH_TEXT = (
    '#!/bin/bash\n\n'
    'cd /home/accounts/PyQtAccounts/\n'
    'export PYTHONPATH="$PYTHONPATH:/home/accounts/PyQtAccounts/"\n'
    'python3 PyQtAccounts.py'
)

# this constant represents text of shortcut of either menu or desktop.
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
    """
    This class provides all tests for FinishPage class of installation wizard.
    """
    def setUp(self):
        # here we create FinishPage instance and fake parent which will contain InitPage instance.
        self.page = FinishPage()
        self.page._parent = Mock()
        self.page._parent.initPage = InitPage()

        # here we assign in-memory folder `/home/accounts` to folder attribute which represents
        # folder where installation wizard will clone PyQtAccounts.
        self.initPage = self.page._parent.initPage
        self.initPage.folder = '/home/accounts'

        # here we initialize in-memory filesystem and create some folders in it such as:
        # folder of program itself, Desktop folder and folder where menu shortcut will be created
        init_accounts_folder()
        os.mkdir('/home/accounts/PyQtAccounts')
        os.mkdir('/home/accounts/Desktop')
        os.makedirs('/home/accounts/.local/share/applications/', exist_ok=True)

    def tearDown(self):
        # here we clean up our in-memory filesystem by deleting accounts folder entirely.
        if os.path.exists('/dev/shm/accounts'):
            shutil.rmtree('/dev/shm/accounts')

    def test_content(self):
        """
        Here we test content of FinishPage: title and success label.
        """
        page = FinishPage()
        self.assertEqual(page.title.text(), '<h4>Finish</h4>', 'Finish page title is incorrect!')
        self.assertEqual(page.text.text(), 'Успішно установлено PyQtAccounts!', 
                         'Finish page message is incorrect!')

    def test_init_page_menu_and_desktop(self):
        # Checkboxes of init page for menu and desktop shortcuts are checked by default
        self.page.initializePage()

        # here we check contents of run.sh and shortcuts (either menu or desktop) that finish
        # page has created
        self.assertEqual(
            EXPECTED_RUN_SH_TEXT,
            open('/home/accounts/PyQtAccounts/run.sh').read(),
            'run.sh file is incorrect!'
        )

        self.assertEqual(EXPECTED_SHORTCUT_TEXT,
                         open('/home/accounts/Desktop/PyQtAccounts.desktop').read(),
                         'Shortcut is incorrect!')
        self.assertEqual(EXPECTED_SHORTCUT_TEXT, open(
            '/home/accounts/.local/share/applications/PyQtAccounts.desktop').read(),
        'Shortcut is incorrect!')

    def test_init_page_menu_no_desktop(self):
        # Checkboxes of init page for menu and desktop shortcuts are checked by default
        self.initPage.desktopCheckbox.setChecked(False)
        self.page.initializePage()

        # here we check contents of run.sh and shortcuts (either menu or desktop) that finish
        # page has created
        self.assertEqual(EXPECTED_RUN_SH_TEXT,
                         open('/home/accounts/PyQtAccounts/run.sh').read(),
                         'run.sh file is incorrect!')

        self.assertFalse(os.path.exists('/home/accounts/Desktop/PyQtAccounts.desktop'),
                         'Desktop shortcut exists but should not be!')

        self.assertEqual(EXPECTED_SHORTCUT_TEXT, open(
            '/home/accounts/.local/share/applications/PyQtAccounts.desktop').read(),
            'Shortcut is incorrect!')


    def test_init_page_desktop_no_menu(self):
        # Checkboxes of init page for menu and desktop shortcuts are checked by default
        self.initPage.menuCheckbox.setChecked(False)
        self.page.initializePage()

        # here we check contents of run.sh and shortcuts (either menu or desktop) that finish
        # page has created
        self.assertEqual(EXPECTED_RUN_SH_TEXT,
                         open('/home/accounts/PyQtAccounts/run.sh').read(),
                         'run.sh file is incorrect!')

        self.assertEqual(EXPECTED_SHORTCUT_TEXT,
                         open('/home/accounts/Desktop/PyQtAccounts.desktop').read(),
                        'Shortcut is incorrect!')

        self.assertFalse(os.path.exists(
            '/home/accounts/.local/share/applications/PyQtAccounts.desktop'),
            'Menu shortcut exists but should not be!'
        )
