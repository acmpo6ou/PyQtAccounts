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

import pyfakefs.fake_filesystem_unittest as fs_unit
from unittest.mock import Mock
import pytest
import os.path
import os
import sys

fs_unit.Patcher.SKIPNAMES = [pytest]

from tests.base import UnitTest
from setup import *

RUN_SH_TEXT = ('export PYTHONPATH="$PYTHONPATH:./"\n'
               'cd .\n'
               'python3 ./PyQtAccounts.py')

EXPECTED_RUN_SH_TEXT = (
    'export PYTHONPATH="$PYTHONPATH:/home/accounts/PyQtAccounts/"\n'
    'cd /home/accounts/PyQtAccounts/\n'
    'python3 ./PyQtAccounts.py'
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
    def test_content(self):
        page = FinishPage()
        self.assertEqual(page.title.text(), '<h4>Finish</h4>')
        self.assertEqual(page.text.text(), 'Успішно установлено PyQtAccounts!')

    def test_init_page(self):
        page = FinishPage()
        page._parent = Mock()
        page._parent.initPage = InitPage()
        initPage = page._parent.initPage

        self.monkeypatch.setenv('HOME', '/home/accounts')
        with fs_unit.Patcher() as p:
            p.fs.create_dir('/home/accounts/PyQtAccounts')
            p.fs.create_dir('/home/accounts/Desktop')
            p.fs.create_dir('/home/accounts/.local/share/applications/')

            initPage.folder = '/home/accounts'
            p.fs.create_file('/home/accounts/PyQtAccounts/run.sh', contents=RUN_SH_TEXT)

            initPage.desktopCheckbox.setChecked(True)
            initPage.menuCheckbox.setChecked(True)

            page.initializePage()

            self.assertEqual(EXPECTED_RUN_SH_TEXT,
                             open('/home/accounts/PyQtAccounts/run.sh').read())
            self.assertEqual(EXPECTED_SHORTCUT_TEXT,
                             open('/home/accounts/Desktop/PyQtAccounts.desktop').read())
            self.assertEqual(EXPECTED_SHORTCUT_TEXT, open(
                '/home/accounts/.local/share/applications/PyQtAccounts.desktop').read())
