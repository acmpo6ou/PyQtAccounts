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