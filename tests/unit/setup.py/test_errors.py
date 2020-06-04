#!/usr/bin/env python3

# Copyright (c) 2020 Kolvah Bogdan
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
from setup import *


class ErrorsTest(UnitTest):
    """
    This class tests Errors class from setup.py module.
    """
    def test_errors(self):
        """
        This test tests color, mode, content and visibility of freshly created Errors widget.
        """
        errors = Errors()
        self.assertEqual(errors.toPlainText(), '', 'Errors content must be empty!')
        self.assertEqual(errors.textColor(), QColor('#f26666'), 'Errors must have red color!')
        self.assertTrue(errors.isReadOnly(), 'Errors must be read only!')
        self.assertFalse(errors.visibility, 'Errors must be hidden when created!')
