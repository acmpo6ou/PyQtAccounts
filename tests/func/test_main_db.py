#!/usr/bin/env python3

from PyQt5.QtCore import *
import unittest
import sys

sys.path.append('.')

from PyQtAccounts import *


class MainDbTest(unittest.TestCase):
    def setUp(self):
        self.settings = QSettings('PyTools', 'PyQtAccounts')
        self.old_is_main_db = self.settings.value('advanced/is_main_db', False, type=bool)
        self.old_main_db = self.settings.value('advanced/main_db', '', type=str)

    def tearDown(self):
        self.settings.setValue('advanced/is_main_db', self.old_is_main_db)
        self.settings.setValue('advanced/main_db', self.old_main_db)

    def test_is_main_db_True(self):
        # Bob uses main database feature of PyQtAccounts, he has it turned on
        # and `main` is the main database.
        self.settings.setValue('advanced/is_main_db', True)
        self.settings.setValue('advanced/main_db', 'main')

        # He opens PyQtAccounts and see form for opening his `main` database.
        # And the title of this form says `Відкрити базу данних main`
        window = Window()
        self.assertIn('main', window.dbs.forms['open'].title.text())

    def test_is_main_db_not_set(self):
        # Tom doesn't know about main database feature of PyQtAccounts yet.
        # He has it turned off by default.
        self.settings.remove('advanced/is_main_db')
        self.settings.remove('advanced/main_db')

        # He opens PyQtAccounts and there is no form for opening any database.
        # Title of open database form is empty.
        window = Window()
        self.assertEqual('<b></b>', window.dbs.forms['open'].title.text())

    def test_is_main_db_False(self):
        # Ross doesn't use main database feature of PyQtAccounts.
        # He turned it off by himself.
        self.settings.setValue('advanced/is_main_db', False)
        self.settings.setValue('advanced/main_db', 'main')

        # He opens PyQtAccounts and there is no form for opening any database.
        # Title of open database form is empty.
        window = Window()
        self.assertEqual('<b></b>', window.dbs.forms['open'].title.text())