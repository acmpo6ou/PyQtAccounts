#!/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtTest import QTest
import unittest
import pytest
import sys

sys.path.append('.')

from .base import win
from PyQtAccounts import *

class CreateDbTest(unittest.TestCase):
    def create_db_show(self):
        pass

    @pytest.fixture(autouse=True)
    def window(self, win):
        self.window = win

    def test_create_db_ctrl_n(self):
        QTest.keyClicks(self.window, 'n', Qt.ControlModifier)
        self.create_db_show()

    def test_create_db_click(self):
        self.window.dbs.panel.addButton.click()
        self.create_db_show()

    def test_create_db_menu(self):
        file = self.window.menuBar().actions()[0] # first is `File` submenu
        new_db = file.menu().actions()[0] # first action is `New database...`
        new_db.trigger()
        self.create_db_show()