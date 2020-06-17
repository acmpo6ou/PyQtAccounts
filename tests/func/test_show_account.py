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
from PyQt5.QtCore import *

from subprocess import Popen, PIPE, STDOUT
import unittest
import pytest
import os

from tests.base import AccsTest, init_accounts_folder, init_src_folder
from core.utils import *
from PyQtAccounts import *


class ShowAccTest(AccsTest):
    """
    This test class provides all functional tests for show account form.
    """
    def setUp(self):
        """
        Here we reassign some widely used variables and initialize fake file
        system.
        """
        super().setUp(name='database2')
        self.form = self.accs.forms['show']
        self.list = self.accs.list

        # here we initialize fake file system and copy `database` database in
        # there which we will use during tests
        init_src_folder(self.monkeypatch)
        self.copyDatabase('database')

    def test_show_account(self):
        """
        Here we test show account form.
        """
        # Lea wants to take a look at her account, so she clicks on it in the list
        self.list.selected(Index('habr'))

        # Show form appears
        self.checkOnlyVisible(self.form)

        # And it has all information about account
        self.assertEqual('Акаунт: habr', self.form.account.text(),
                         "Account-name in show account form is incorrect!")
        self.assertEqual("Ім'я: Lea", self.form.name.text(),
                         "Name in show account form is incorrect!")
        self.assertEqual('E-mail: spheromancer@habr.com',
                         self.form.email.text(),
                         "Email in show account form is incorrect!")
        self.assertEqual('Пароль: habr_password', self.form.password.text(),
                         "Password in show account form is incorrect!")
        self.assertEqual('Дата: 19.05.1990', self.form.date.text(),
                         "Date in show account form is incorrect!")
        self.assertEqual('Коментарій: Habr account.',
                         self.form.comment.toPlainText(),
                         "Comment in show account form is incorrect!")
        self.assertEqual(
            f'До мишиного буферу копіюється: e-mail',
            self.form.mouse_copy.text(),
            "Mouse-copy label of show account form is incorrect!")

    def test_copy_email_and_password(self):
        """
        Here we test how copying of email and password in show account form
        works, when e-mail is chosen to be copied to mouseboard.
        """
        # Bob wants to copy e-mail and password of his account, so he chose one in the list
        self.list.selected(Index('gmail'))

        # Note: he has e-mail chosen to be copied to mouseboard

        # He then goes to menu: File -> Copy
        # we can't use self.menu() here because it is applied to main window
        # while we use database one
        file = self.win.menuBar().actions()[0]  # first is `File` submenu
        copy = file.menu().actions()[2]  # third action is `Copy`
        copy.trigger()

        # Password copied to clipboard
        clipboard = QGuiApplication.clipboard()
        self.assertEqual(
            clipboard.text(),
            '$z#5G_UG~K;I9U9$',  # those symbols are password
            "Password isn't copied to clipboard when performed "
            "copy operation in show account form!")

        # E-mail is copied to mouse clipboard by xclip tool
        xclip = Popen(['xclip', '-o'], stdout=PIPE, stderr=STDOUT)
        mouseboard = xclip.communicate()[0].decode()
        self.assertEqual(
            mouseboard, 'bobgreen@gmail.com\n',
            "Email isn't copied to mouse clipboard when performed"
            " copy option in show account form!")

    def test_copy_usename_and_password(self):
        """
        Here we test how copying of username and password in show account form
        works, when username is chosen to be copied to mouseboard.
        """
        # Chris wants to copy username and password of his account, so he chose one in the
        # list
        self.list.selected(Index('stackoverflow'))

        # Note: he has username chosen to be copied to mouseboard

        # He then goes to menu: File -> Copy
        # we can't use self.menu() here because it is applied to main window
        # while we use database one
        file = self.win.menuBar().actions()[0]  # first is `File` submenu
        copy = file.menu().actions()[2]  # third action is `Copy`
        copy.trigger()

        # Password copied to clipboard
        clipboard = QGuiApplication.clipboard()
        self.assertEqual(
            clipboard.text(),
            '930bU~1j.;nLS<Ga',  # those symbols are password
            "Password isn't copied to clipboard when performed "
            "copy operation in show account form!")

        # Username is copied to mouse clipboard by xclip tool
        xclip = Popen(['xclip', '-o'], stdout=PIPE, stderr=STDOUT)
        mouseboard = xclip.communicate()[0].decode()
        self.assertEqual(
            mouseboard, 'Chris Kirkman\n',
            "Username isn't copied to mouse clipboard when performed"
            " copy option in show account form!")
