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

from tests.base import AccsTest, FuncTest
from core.utils import *
from PyQtAccounts import *


class CloseWhenDatabaseOpenedTest(AccsTest):
    def test_close_when_database_opened_Yes(self):
        self.monkeypatch.setattr(QMessageBox, 'question', self.mess(
            'Увага!',
            'Ви певні що хочете вийти?',
            button=QMessageBox.Yes
        ))
        self.window.close()
        self.assertEqual(len(self.window.windows), 1)

    def test_close_when_database_opened_No(self):
        self.monkeypatch.setattr(QMessageBox, 'question', self.mess(
            'Увага!',
            'Ви певні що хочете вийти?',
            button=QMessageBox.No
        ))
        self.window.close()
        self.assertEqual(len(self.window.windows), 2)


class CloseTest(FuncTest):
    def test_close_when_no_database_opened(self):
        self.monkeypatch.setattr(QMessageBox, 'question', self.mess_showed)
        self.window.close()
        self.assertFalse(self.window.visibility)

    def test_destroy_window(self):
        self.window.destroy = True
        self.monkeypatch.setattr(QMessageBox, 'question', self.mess_showed)
        self.window.close()
        self.assertFalse(self.window.visibility)

    def close_from_menu(self):
        # First is `File` submenu, last is `Quit` action
        self.monkeypatch.setattr(QMessageBox, 'question', self.mess_showed)
        self.menu(0, -1).trigger()
        self.assertFalse(self.window.visibility)
