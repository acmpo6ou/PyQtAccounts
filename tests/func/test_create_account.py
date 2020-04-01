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
import pyautogui
from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
import unittest
import pytest
import os

from tests.base import AccsTest
from core.utils import *
from PyQtAccounts import *


class Test(AccsTest):
    def setUp(self):
        super().setUp()
        self.form = self.accs.forms['create']

    def test_create_account_ctrl_n(self):
        pyautogui.hotkey("ctrl", "n")
        QTest.qWait(100)
        self.checkOnlyVisible(self.form)

    def test_create_account_click(self):
        self.accs.panel.addButton.click()
        self.checkOnlyVisible(self.form)

    def test_create_account_menu(self):
        file = self.win.menuBar().actions()[0]  # first is `File` submenu
        new_db = file.menu().actions()[0]  # first action is `New account...`
        new_db.trigger()
        self.checkOnlyVisible(self.form)
