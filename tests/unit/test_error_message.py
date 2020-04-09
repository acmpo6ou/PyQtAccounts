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
import core.const
import PyQtAccounts


class ErrorMsgTest(UnitTest):
    def test_error_message(self):
        PyQtAccounts.ErrorWindow.exec = lambda *args: PyQtAccounts.QMessageBox.Ok
        # There is an error in the program
        def mock_Window():
            raise Exception('Error message!')
        self.monkeypatch.setattr('PyQtAccounts.Window', mock_Window)

        # Emily launches PyQtAccounts
        msg = PyQtAccounts.main()

        # The error message appears saying that program must shutdown itself due to the error
        self.assertEqual('Помилка!', msg.windowTitle())
        self.assertEqual('Вибачте програма повинна припинити роботу через помилку.',
                         msg.text())
        self.assertEqual('Error message!', msg.detailedText())