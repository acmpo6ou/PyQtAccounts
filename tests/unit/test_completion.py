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

        self.account_name = self.form.accountInput
        self.name = self.form.nameInput
        self.email = self.form.emailInput

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

        # and it has all emails of database
        self.assertTrue(
            c.model().findItems('bobgreen@gmail.com'),
            "Not enough e-mails in email completer of create account form!")
        self.assertTrue(
            c.model().findItems('spheromancer@habr.com'),
            "Not enough e-mails in email completer of create account form!")
        self.assertTrue(
            c.model().findItems('tom@gmail.com'),
            "Not enough e-mails in email completer of create account form!")
