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
from string import *
import unittest
import pytest
import os

from tests.base import DbsTest
from core.utils import *
from PyQtAccounts import *


class TestPassGenerationDialog(DbsTest):
    """
    This test class provides all functional tests for password generation
    dialog.
    """
    def setUp(self):
        """
        Here we reassign some widely used variables.
        """
        super().setUp()
        self.dbs.panel.addButton.click()
        self.form = self.dbs.forms['create']
        self.form.generateButton.click()
        self.dialog = self.form.dialog
        self.gen = self.dialog.buttonGenerate
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput

    def checkPassEqual(self):
        """
        We use this method to check that passwords in to fields are equal.
        """
        # Passwords in fields must always be equal
        pass1 = self.pass_input.text()
        pass2 = self.pass_repeat_input.text()
        self.assertEqual(pass1, pass2, 'Passwords in fields are differ!')

    def checkHasOneOf(self, string, symbols):
        """
        We use this method to check that given `string` has characters from
        `symbols`. It is useful when we want to check for example that generated 
        password has digits when user checked checkbox that represents 
        whether to include digits or not.
        """
        # here we iterate trough all characters of `symbols`
        for s in symbols:
            # and some of them is in `string` then we break and everything is OK.
            if s in string:
                break
        else:
            raise AssertionError(f"No {symbols} in {string}!")

    def checkNotHasOneOf(self, string, symbols):
        """
        We use this method to check that given `string` has no characters from
        `symbols`. It is useful when we want to check for example that generated 
        password has no digits when user unchecked checkbox that represents 
        whether to include digits or not.
        """
        # here we use checkHasOneOf method to check that `string` contains no `symbols`
        try:
            self.checkHasOneOf(string, symbols)
        except AssertionError:
            # if it is then AssertionError will be raised and this is OK.
            pass
        else:
            # in other way when no AssertionError was raised it means that `string`
            # contains some of `symbols` so we show error message
            raise AssertionError(f"Found one of {symbols} in {string}!")

    def test_length(self):
        """
        Here we test that length of generated password is equal to the specified
        in length spinbox of generate password dialog.
        """
        # Toon wants to generate password, he left everything by defaults and presses generate
        self.gen.click()

        # Password appears in both password fields and it has length 16 by default
        self.assertEqual(
            len(self.pass_input.text()), 16,
            'Length of generated password and length specified in'
            'spinbox of generate password dialog are differ!')
        self.checkPassEqual()

        # Tom then changes length to 32 and presses generate
        self.dialog.symNum.setValue(32)
        self.gen.click()

        # Password appears in both password fields and it has length 32 as well
        self.assertEqual(
            len(self.pass_input.text()), 32,
            'Length of generated password and length specified in'
            'spinbox of generate password dialog are differ!')
        self.checkPassEqual()

    def check_symbols(self, flag, symbols):
        """
        Here we check that generated password does or does not contains symbols
        such as digits, punctuation, lower and upper ascii letters accordingly
        to flag of generate password dialog.
        :param flag:
        flag using which we want to check password
        :param symbols:
        symbols that are associated with flag
        """
        # here we simulate click on generate button of generate password dialog
        self.gen.click()
        # then we check that it has at least one of characters from symbols
        self.checkHasOneOf(self.pass_input.text(), symbols)
        # and then we check that passwords in both password fields are equal
        self.checkPassEqual()

        # then we uncheck checkbox associated with given flag
        flag.setChecked(False)
        # here we press generate button again
        self.gen.click()
        # and here we check that password has no characters of `symbols` because
        # we unchecked checkbox and generated password must not contain any characters
        # that are associated with the flag
        self.checkNotHasOneOf(self.pass_input.text(), symbols)
        # here we again check that passwords are equal in both fields
        self.checkPassEqual()

    def test_symbols(self):
        """
        Here we use check_symbols method to check generate
        password dialog behavior when certain checkboxes are checked or
        unchecked.
        """
        # here we obtain dialog instance
        dialog = self.dialog

        # and here we create lists of flags (i.e. checkboxes) and symbols
        # associated with them
        flags = (dialog.digitsFlag, dialog.lowerFlag, dialog.upperFlag,
                 dialog.punctuationFlag)
        symbols = (digits, ascii_lowercase, ascii_uppercase, punctuation)

        # finally we use check_symbols method to check dialog behavior when
        # certain checkboxes are checked or unchecked
        for flag, syms in zip(flags, symbols):
            # here we need to make all flags checked at the start of testing
            # next flag because we make all this in
            # loop and check_symbols method unchecks every flag so at the end we
            # will have all flags unchecked and it will case error which will crash test
            for f in flags:
                f.setChecked(True)
            self.check_symbols(flag, syms)
