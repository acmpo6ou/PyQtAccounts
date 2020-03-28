#!/usr/bin/env python3

import unittest
import sys

sys.path.append('.')

from PyQtAccounts import *


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.window = Window()
        self.dbs = self.window.dbs

    def tearDown(self):
        del self.window

    def checkOnlyVisible(self, elem, dbs):
        for form in dbs.forms:
            if dbs.forms[form] == elem:
                self.assertTrue(dbs.forms[form].visibility)
                continue
            self.assertFalse(dbs.forms[form].visibility)

        for tip in dbs.tips:
            if dbs.tips[tip] == elem:
                self.assertTrue(dbs.tips[tip].visibility)
                continue
            self.assertFalse(dbs.tips[tip].visibility)
