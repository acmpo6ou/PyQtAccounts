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

from tests.base import AccsTest
from core.utils import *
from PyQtAccounts import *


class EditAccsTest(AccsTest):
    def setUp(self):
        super().setUp()
        self.form = self.accs.forms['edit']
        self.list = self.accs.list
        self.editButton = self.accs.panel.editButton

        self.account = self.form.accountInput
        self.name = self.form.nameInput
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput
        self.email = self.form.emailInput
        self.date = self.form.dateInput
        self.comment = self.form.commentInput

    def test_edit_content(self):
        # Lea wants to edit her account, so she chose it in the list and presses edit button
        self.list.selected(Index('habr'))
        self.editButton.click()

        # Edit form appears
        self.checkOnlyVisible(self.form)

        # Every field is filled as well
        self.assertEqual(self.account.text(), 'habr')
        self.assertEqual(self.name.text(), 'Lea')
        self.assertEqual(self.pass_input.text(), 'habr_password')
        self.assertEqual(self.pass_repeat_input.text(), 'habr_password')
        self.assertEqual(self.email.text(), 'spheromancer@habr.com')
        self.assertEqual(self.date.text(), '19.05.1990')
        self.assertEqual(self.comment.toPlainText(), 'Habr account.')
