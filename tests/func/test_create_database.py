#!/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtTest import QTest
import unittest
import pytest
import pyautogui
import sys

sys.path.append('.')

from .base import BaseTest
from PyQtAccounts import *

class CreateDbTest(BaseTest):
    '''
    Testing does create database form appears wheather we click on the `+` button
    or through Menu -> File -> New database... or Ctrl+N key sequences
    '''
    def test_create_db_ctrl_n(self):
        pyautogui.hotkey("ctrl", "n")
        QTest.qWait(100)
        self.assertTrue(self.window.dbs.forms['create'].visibility)

    def test_create_db_click(self):
        self.window.dbs.panel.addButton.click()
        self.assertTrue(self.window.dbs.forms['create'].visibility)

    def test_create_db_menu(self):
        file = self.window.menuBar().actions()[0]  # first is `File` submenu
        new_db = file.menu().actions()[0]     # first action is `New database...`
        new_db.trigger()
        self.assertTrue(self.window.dbs.forms['create'].visibility)

    def test_valid_db_name(self):
        # Bob has two databases called `main` and `crypt`.
        # He wants to create new one:
        self.window.dbs.panel.addButton.click()

        # He starts typing `cry` at the name input.
        _input = self.window.dbs.forms['create'].nameInput
        QTest.keyClicks(_input, 'cry')

        # There is now errors appearing
        error = self.window.dbs.forms['create'].nameError
        self.assertFalse(error.visibility)

        # He then types `pt` at the name input, so the name in the input (`crypt`)
        # is the same as the name of database he already has
        QTest.keyClicks(_input, 'pt')

        # The error message appears saying that the database with such name already exists.
        self.assertTrue(error.visibility)

        # Then Bob types `2` to change name from `crypt` to `crypt2`
        QTest.keyClick(_input, '2')

        # The error message disappears
        self.assertFalse(error.visibility)

    def test_valid_password(self):
        # Tom wants to create new database
        self.window.dbs.panel.addButton.click()

        # First he types name
        _input = self.window.dbs.forms['create'].nameInput
        QTest.keyClicks(_input, 'somedb')

        # Then he types password to first password input
        pass_input = self.window.dbs.forms['create'].passField.passInput
        QTest.keyClicks(pass_input, 'password123')

        # The error message appears saying that both passwords aren't equal,
        # because first input is filled and the second is not
        error = self.window.dbs.forms['create'].passEqError
        self.assertTrue(error.visibility)

        # Tom then filles second password field with the same password
        pass_repeat_input = self.window.dbs.forms['create'].passRepeatField.passInput
        QTest.keyClicks(pass_repeat_input, 'password123')

        # The error disappears
        self.assertFalse(error.visibility)

        # He then erase both password fields
        pass_input.setText('')
        pass_repeat_input.setText('')

        # Another error appears saying that he needs to fill password fields
        pass_error = self.window.dbs.forms['create'].passFilledError
        self.assertTrue(pass_error.visibility)

        # Tom fills them again
        QTest.keyClicks(pass_input, 'password123')
        QTest.keyClicks(pass_repeat_input, 'password123')

        # End there is no errors
        self.assertFalse(error.visibility)
        self.assertFalse(pass_error.visibility)

    def test_generate_pass(self):
        # Ross wants to create new database
        self.window.dbs.panel.addButton.click()

        # He doesn't want to invent password by himself
        # So he press the `generate` button
        gen = self.window.dbs.forms['create'].generateButton
        gen.click()

        # The generate password dialog appears
        dialog = self.window.dbs.forms['create'].dialog
        self.assertTrue(dialog.visibility)

        # He lefts everything as it is and press the `generate` button of the dialog
        dialog.buttonGenerate.click()

        # Randomly generated password appears in both password fields of create database form
        pass_input = self.window.dbs.forms['create'].passField.passInput
        pass_repeat_input = self.window.dbs.forms['create'].passRepeatField.passInput

        self.assertIsNot(pass_input.text(), '')
        self.assertIsNot(pass_repeat_input.text(), '')
        self.assertEqual(pass_input.text(), pass_repeat_input.text())
