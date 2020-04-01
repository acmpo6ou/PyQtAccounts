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
from string import *
import unittest
import pytest
import os

from tests.base import FuncTest
from core.utils import *
from PyQtAccounts import *


class Test(FuncTest):
    def setUp(self):
        super().setUp()
        self.dbs.panel.addButton.click()
        self.form = self.dbs.forms['create']
        self.form.generateButton.click()
        self.dialog = self.form.dialog
        self.gen = self.dialog.buttonGenerate
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput

    def checkPassEqual(self):
        # Passwords in fields must always be equal
        pass1 = self.pass_input.text()
        pass2 = self.pass_repeat_input.text()
        self.assertEqual(pass1, pass2)

    def checkHasOneOf(self, str, symbols):
        for s in symbols:
            if s in str:
                break
        else:
            assert AssertionError(f"No {symbols} in {str}!")

    def checkNotHasOneOf(self, str, symbols):
        try:
            self.checkHasOneOf(str, symbols)
        except AssertionError:
            pass
        else:
            assert AssertionError(f"Found one of {symbols} in {str}!")

    def test_length(self):
        # Toon wants to generate password, he left everything by defaults and presses generate
        self.gen.click()

        # Password appears in both password fields and it has length 16 by default
        self.assertEqual(len(self.pass_input.text()), 16)
        self.checkPassEqual()

        # Tom then changes length to 32 and presses generate
        self.dialog.symNum.setValue(32)
        self.gen.click()

        # Password appears in both password fields and it has length 32 as well
        self.assertEqual(len(self.pass_input.text()), 32)
        self.checkPassEqual()

    def check_symbols(self, flag, symbols):
        self.gen.click()
        self.checkHasOneOf(self.pass_input.text(), symbols)
        self.checkPassEqual()

        flag.setChecked(False)
        self.checkNotHasOneOf(self.pass_input.text(), symbols)
        self.checkPassEqual()

    def test_symbols(self):
        dialog = self.dialog
        flags = (dialog.digitsFlag, dialog.lowerFlag, dialog.upperFlag, dialog.punctuationFlag)
        symbols = (digits, ascii_lowercase, ascii_uppercase, punctuation)

        for flag, syms in zip(flags, symbols):
            self.check_symbols(flag, syms)
