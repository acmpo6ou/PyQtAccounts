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
import unittest
import pytest
import os
import glob

from tests.base import DbsTest
import core.utils
from core.const import *
from PyQtAccounts import *


class HelpTipTest(DbsTest):
    def setUp(self):
        os.environ['TESTING'] = 'True'
        self.settings = QSettings('PyToolsTest', 'PyQtAccounts')
        self.old_is_main_db = self.settings.value('advanced/is_main_db', False, type=bool)
        self.old_main_db = self.settings.value('advanced/main_db', '', type=str)

    def tearDown(self):
        self.settings.setValue('advanced/is_main_db', self.old_is_main_db)
        self.settings.setValue('advanced/main_db', self.old_main_db)

    def test_no_dbs(self):
        # Ross opens up PyQtAccounts, he has no database yet
        self.monkeypatch.setattr(glob, 'glob', lambda path: [])
        window = Window()

        # There is help tip saying how he can create new database
        tip = window.dbs.tips['help']
        self.assertEqual(tip.text(), HELP_TIP_DB)

    def test_has_dbs(self):
        # Emily opens up PyQtAccounts, she has some databases
        window = Window()

        # There is help tip saying that she need to chose database
        tip = window.dbs.tips['help']
        self.assertEqual(tip.text(), "Виберіть базу данних")
