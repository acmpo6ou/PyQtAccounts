#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh Bogdan
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

from tests.base import UnitTest
from core.forms import CreateForm


class FormsCreateTest(UnitTest):
    """
    This class tests `create` abstract method of CreateForm.
    """
    def test_create_method_not_implemented(self):
        # here we create subclass of CreateForm
        class MyForm(CreateForm):
            def __init__(self):
                pass

        # and here we instantiate it
        form = MyForm()

        # then we try to call `create` method which must be implemented in MyForm class but it's
        # not, so NotImplementedError occurs
        self.assertRaises(NotImplementedError, form.create)
