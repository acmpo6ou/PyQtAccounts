#!/usr/bin/env python3

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
import unittest
import pytest
import sys

sys.path.append('.')

from .base import BaseTest
from utils import *
from PyQtAccounts import *


class OpenDbTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.form = self.dbs.forms['open']
        self.list = self.dbs.list
        self.pass_input = self.form.passField.passInput

    def test_form_show(self):
        # Bob wants to open his database, so he clicks at the `crypt` on the database list
        self.list.selected(Index('crypt'))

        # open database form appears
        self.checkOnlyVisible(self.form, self.dbs)

        # There is title that says `Відкрити базу данних crypt`
        self.assertIn('crypt', self.form.title.text())

    def test_password_validation(self):
        # Tom wants to open his database called `database`
        self.list.selected(Index('database'))

        # He types accidentally types wrong password and hits Enter
        QTest.keyClicks(self.pass_input, 'password')
        QTest.keyClick(self.pass_input, Qt.Key_Enter)

        # The error message appears saying that the password is incorrect
        error = self.form.incorrectPass
        self.assertTrue(error.visibility)

        # Tom then corrects password and again hits Enter
        self.pass_input.setText('some_password')
        QTest.keyClick(self.pass_input, Qt.Key_Enter)

        # The error disappears
        self.assertFalse(error.visibility)

        # Database window appears
        win = self.window.windows[1]  # first is main window, second is database one
        self.assertTrue(win.visibility)
