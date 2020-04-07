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
import unittest
import pytest
import os

from tests.base import UnitTest
from core.const import *
from PyQtAccounts import *


class ReqsWarningsTest(UnitTest):
    def test_system_reqs(self):
        def mock_system(sys_req):
            WarningWindow.exec = lambda self: QMessageBox.Ok
            def wrap(command):
                req = command.replace('which ', '')
                assert req in sys_reqs
                if req == sys_req:
                    return True
                else:
                    return False
            return wrap

        for req in sys_reqs:
            # Lea hasn't install any of PyQtAccounts dependencies
            self.monkeypatch.setattr('os.system', mock_system(req))

            # So she launches the program
            msg = main()

            # Warning message appears saying that she needs to install some dependencies
            self.assertEqual('Увага!', msg.windowTitle())
            self.assertEqual('''
                <h3>Не всі пакети встановлено!</h3>
                <p>Пакет {0} не встановлено, без певних пакетів PyQtAccounts буде працювати 
                некоректно!</p>
                <p>Встановіть {0} такою командою:</p>
                <p>sudo apt install {0}</p>
                '''.format(req), msg.text())
