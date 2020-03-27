#!/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtTest import QTest
import unittest
import pytest
import pyautogui
import sys

sys.path.append('.')

from PyQtAccounts import *

class CreateDbTest(unittest.TestCase):
    '''
    Testing does create database form appears wheather we click on the `+` button
    or through Menu -> File -> New database... or Ctrl+N key sequences
    '''
    def test_create_db_ctrl_n(self):
        window = Window()
        pyautogui.hotkey("ctrl", "n")
        QTest.qWait(100)
        self.assertTrue(window.dbs.forms['create'].vis)

    def test_create_db_click(self):
        window = Window()
        window.dbs.panel.addButton.click()
        self.assertTrue(window.dbs.forms['create'].vis)

    def test_create_db_menu(self):
        window = Window()
        file = window.menuBar().actions()[0]  # first is `File` submenu
        new_db = file.menu().actions()[0]     # first action is `New database...`
        new_db.trigger()
        self.assertTrue(window.dbs.forms['create'].vis)

    def test_valid_db_name(self):
        # Bob has two databases called `main` and `crypt`.
        # He wants to create new one:
        window = Window()
        window.dbs.panel.addButton.click()

        # He starts typing `cry` at the name input.
        _input = window.dbs.forms['create'].nameInput
        QTest.keyClicks(_input, 'cry')

        # There is now errors appearing
        error = window.dbs.forms['create'].nameError
        self.assertFalse(error.vis)

        # He then types `pt` at the name input, so the name in the input (`crypt`)
        # is the same as the name of database he already has
        QTest.keyClicks(_input, 'pt')

        # The error message appears saying that the database with such name already exists.
        self.assertTrue(error.vis)

        # Then Bob types `2` to change name from `crypt` to `crypt2`
        QTest.keyClick(_input, '2')

        # The error message disappears
        self.assertFalse(error.vis)

    def test_valid_password(self):
        # Tom wants to create new database
        window = Window()
        window.dbs.panel.addButton.click()

        # First he types name
        _input = window.dbs.forms['create'].nameInput
        QTest.keyClicks(_input, 'somedb')

        # Then he types password to first password input
        pass_input = window.dbs.forms['create'].passField.passInput
        QTest.keyClicks(pass_input, 'password123')

        # The error message appears saying that both passwords aren't equal,
        # because first input is filled and the second is not
        error = window.dbs.forms['create'].passEqError
        self.assertTrue(error.vis)

        # Tom then filles second password field with the same password
        pass_repeat_input = window.dbs.forms['create'].passRepeatField.passInput
        QTest.keyClicks(pass_repeat_input, 'password123')

        # The error disappears
        self.assertFalse(error.vis)

        # He then erase both password fields
        pass_input.setText('')
        pass_repeat_input.setText('')

        # Another error appears saying that he needs to fill password fields
        pass_error = window.dbs.forms['create'].passFilledError
        self.assertTrue(pass_error.vis)

        # Tom filles them again
        QTest.keyClicks(pass_input, 'password123')
        QTest.keyClicks(pass_repeat_input, 'password123')

        # End there is no errors
        self.assertFalse(error.vis)
        self.assertFalse(pass_error.vis)
