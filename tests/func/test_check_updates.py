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
from PyQt5.QtCore import *
from unittest.mock import Mock
import pytest
import os

from tests.base import FuncTest
from core.utils import *
from core.updates import *
from PyQtAccounts import *


class Test(FuncTest):
    def setUp(self):
        super().setUp()

    def test_check_no_updates(self):
        def mock_run(self):
            self.result.emit(False, [])
        self.monkeypatch.setattr(Updating, 'run', mock_run)
        self.monkeypatch.setattr(QMessageBox, 'information',
                                 self.mess('Оновлення', "Немає оновленнь."))

        updates = self.window.menuBar().actions()[2]  # third is `Updates` submenu
        check = updates.menu().actions()[0]
        check.trigger()
