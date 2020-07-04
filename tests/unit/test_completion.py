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

from unittest.mock import Mock
import pytest
import os

from tests.base import AccsTest


class CompletionTest(AccsTest):
    def setUp(self):
        """
        Here we reassign some widely used variables.
        """
        super().setUp()

        self.form = self.accs.forms['create']
        self.addButton = self.accs.panel.addButton
        self.createButton = self.form.createButton

        self.account_name = self.form.accountInput
        self.name = self.form.nameInput
        self.email = self.form.emailInput
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput

    def test_completion(self):
        """
        Here we test how completion of create account form works.
        """
        # Emily wants to create account, so she opens up create account form.
        self.addButton.click()

        # The form appears
        self.checkOnlyVisible(self.form)

        # and email field has an e-mail completion
        c = self.email.completer()
        self.assertIsNotNone(c, "E-mail field doesn't has its completer!")
        print(c.model().stringList())

        # and it has all emails of database
        expected_emails = {
            'bobgreen@gmail.com', 'spheromancer@habr.com', 'tom@gmail.com'
        }
        self.assertEqual(
            expected_emails, set(c.model().stringList()),
            "Email completer of create account form is incorrect!")

        # and name field has a name completion
        c = self.name.completer()
        self.assertIsNotNone(c, "Name field doesn't has its completer!")
        print(c.model().stringList())

        # and it has all names of database
        expected_names = {'Bob', 'Lea', 'Tom'}
        self.assertEqual(
            expected_names, set(c.model().stringList()),
            "Name completer of create account form is incorrect!")

        # and accountname field has an account name completion
        c = self.account_name.completer()
        self.assertIsNotNone(c,
                             "Account name field doesn't has its completer!")
        print(c.model().stringList())

        # and it has all accountnames of database
        expected_accountnames = {'gmail', 'mega', 'habr'}
        self.assertEqual(
            expected_accountnames, set(c.model().stringList()),
            "Account name completer of create account form is incorrect!")

    def test_completion_updates(self):
        """
        Here we test that completion updates when user creates new account.
        """
        # Tony has some accounts in his database and he want to create another
        # account
        self.addButton.click()

        # so he inputs name, password, email and account name
        self.name.setText('Tony Stark')
        self.account_name.setText('google')
        self.email.setText('google@gmail.com')
        self.pass_input.setText('core')
        self.pass_repeat_input.setText('core')

        # and presses create button
        self.createButton.click()

        # he opens create form again
        self.addButton.click()

        # and all fields has their completion updated:
        # emails
        c = self.email.completer()
        expected_emails = {
            'bobgreen@gmail.com', 'spheromancer@habr.com', 'tom@gmail.com',
            'google@gmail.com'
        }
        self.assertEqual(
            expected_emails, set(c.model().stringList()),
            "Email completer of create account form isn't updated after "
            "creating new account!")

        # names
        c = self.name.completer()
        expected_names = {'Bob', 'Lea', 'Tom', 'Tony Stark'}
        self.assertEqual(
            expected_names, set(c.model().stringList()),
            "Name completer of create account form isn't updated after "
            "creating new account!")

        # account names
        c = self.account_name.completer()
        expected_accountnames = {'gmail', 'mega', 'habr', 'google'}
        self.assertEqual(
            expected_accountnames, set(c.model().stringList()),
            "Account name completer of create account form isn't updated after "
            "creating new account!")
