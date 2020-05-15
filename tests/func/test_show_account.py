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

from subprocess import Popen, PIPE, STDOUT
import unittest
import pytest
import os

from tests.base import AccsTest, init_accounts_folder, init_src_folder
from core.utils import *
from PyQtAccounts import *


class ShowAccTest(AccsTest):
    def setUp(self):
        super().setUp()
        self.form = self.accs.forms['show']
        self.list = self.accs.list

        init_src_folder(self.monkeypatch)
        self.copyDatabase('database')

    def test_show_account(self):
        # Lea wants to take a look at her account, so she clicks on it in the list
        self.list.selected(Index('habr'))

        # Show form appears
        self.checkOnlyVisible(self.form)

        # And it has all information about account
        self.assertEqual('Акаунт: habr', self.form.account.text())
        self.assertEqual("Ім'я: Lea", self.form.name.text())
        self.assertEqual('E-mail: spheromancer@habr.com', self.form.email.text())
        self.assertEqual('Пароль: habr_password', self.form.password.text())
        self.assertEqual('Дата: 19.05.1990', self.form.date.text())
        self.assertEqual('Коментарій: Habr account.', self.form.comment.toPlainText())

    def test_copy_email_and_password(self):
        # Bob wants to copy e-mail and password of his account, so he chose one in the list
        self.list.selected(Index('gmail'))

        # He then goes to menu: File -> Copy
        file = self.win.menuBar().actions()[0]  # first is `File` submenu
        copy = file.menu().actions()[2]         # third action is `Copy`
        copy.trigger()

        # Password copied to clipboard
        clipboard = QGuiApplication.clipboard()
        self.assertEqual(clipboard.text(), '$z#5G_UG~K;I9U9$')  # those symbols are password

        # E-mail is copied to mouse clipboard by xclip tool
        xclip = Popen(['xclip', '-o'], stdout=PIPE, stderr=STDOUT)
        mouseboard = xclip.communicate()[0].decode()
        self.assertEqual(mouseboard, 'bobgreen@gmail.com\n')
