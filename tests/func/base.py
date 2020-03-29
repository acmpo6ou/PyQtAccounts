#!/usr/bin/env python3

import unittest
import pytest
import sys

sys.path.append('.')

from PyQtAccounts import *


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.window = Window()
        self.dbs = self.window.dbs

    def tearDown(self):
        self.window.destroy = True
        self.window.close()

    def checkOnlyVisible(self, elem):
        self.check_only_visible(elem, self.dbs)

    def check_only_visible(self, elem, parent):
        for form in parent.forms:
            if parent.forms[form] == elem:
                self.assertTrue(parent.forms[form].visibility)
                continue
            self.assertFalse(parent.forms[form].visibility)

        for tip in parent.tips:
            if parent.tips[tip] == elem:
                self.assertTrue(parent.tips[tip].visibility)
                continue
            self.assertFalse(parent.tips[tip].visibility)

    def checkDbInList(self, name):
        model = self.dbs.list.model
        for i in range(model.rowCount()):
            index = model.item(i)
            if index.text() == name:
                break
        else:
            raise AssertionError(f'Database {name} not in the list!')

    def checkDbNotInList(self, name):
        try:
            self.checkDbInList(name)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"Database {name} in the list, but it shouldn't be!")

    @pytest.fixture(autouse=True)
    def monkeypatching(self, monkeypatch):
        self.monkeypatch = monkeypatch
