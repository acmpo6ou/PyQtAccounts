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

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import unittest
import pytest
import os

from tests.base import UnitTest
from PyQtAccounts import *


class InitWarningTest(UnitTest):
    """
    This test class tests warning that appears when user hasn't initialized
    PyQtAccounts. In that case program will crash on startup, so we first show
    appropriate warning to inform user.
    """
    def test_init_warning(self):
        """
        This test tests whether warning appears when user hasn't initialized
        PyQtAccounts.
        """
        # Bob doesn't know about initialization of PyQtAccounts yet.
        # He has download zip file from github and there is no .git directory in that archive
        self.monkeypatch.setattr('os.listdir', lambda path: [])

        # Bob launches PyQtAccounts
        WarningWindow.exec = lambda *args: QMessageBox.Ok
        msg = main()

        # Warning message appears saying that he need to initialize program
        # by downloading setup.py installation wizard from github repository
        self.assertEqual(msg.windowTitle(), 'Увага!',
                         'Warning message title is incorrect!')
        self.assertEqual(
            msg.text(),
            '''
            <h3>Програму не ініціалізовано!</h3>
            <p>Завантажте файл <b><i>setup.py</i></b> з нашого github репозиторія.</p>
            <p>Запустіть його і пройдіть всі кроки інсталяції.</p>
            <p>Ініціалізація потрібна, аби система оновлення PyQtAccounts працювала.</p>
            <p>Система оновлення автоматично перевіряє, завантажує і встановлює оновлення.</p>
            ''', 'Warning message is incorrect!')

    def test_no_init_warning(self):
        """
        This test tests that warning does not appear when user has PyQtAccounts
        initialized.
        """
        # Tom has installed PyQtAccounts using setup.py installation wizard
        # So there is .git directory in program directory
        self.monkeypatch.setattr('os.listdir', lambda path: ['.git'])

        # Tom launches PyQtAccounts
        msg = main()

        # There is no messages about initialization
        self.assertIsNone(msg, 'Initialization message is shown but should not'
                               ' appear!')
