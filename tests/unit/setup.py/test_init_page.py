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
import os

from tests.base import UnitTest
from setup import *


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
