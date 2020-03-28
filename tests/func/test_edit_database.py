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


class EditDbTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.form = self.dbs.forms['edit']
        self.list = self.dbs.list

        self.open_form = self.dbs.forms['open']
        self.open_pass_input = self.open_form.passField.passInput

        self.name = self.form.nameInput
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput

    def test_edit_db_warning(self):
        # Toon wants to edit database so he chose one from the list and presses edit button
        self.list.selected(Index('database'))
        self.dbs.panel.editButton.click()

        # The error message appears saying that he can't edit database until he opens it
        self.checkOnlyVisible(self.dbs.tips['edit-w'], self.dbs)

        # So Toon opens database
        self.list.selected(Index('database'))
        self.open_pass_input.setText('some_password')
        self.open_form.openButton.click()

        # There is no errors
        self.checkOnlyVisible(self.dbs.tips['help'], self.dbs)

        # and then he tries again
        self.dbs.panel.editButton.click()

        # Edit database form appears
        self.checkOnlyVisible(self.form, self.dbs)

    def test_name_validation(self):
        # Lea wants to edit database, so she opens one
        self.list.selected(Index('database'))
        self.open_pass_input.setText('some_password')
        self.open_form.openButton.click()

        # Then she presses edit button
        self.dbs.panel.editButton.click()

        # In the name and password fields she sees database name and password appropriately
        self.assertEqual('database', self.name.text())
        self.assertEqual('some_password', self.pass_input.text())
        self.assertEqual('some_password', self.pass_repeat_input.text())

        # Lea changes database name to `another_database` then
        self.name.setText('another_database')

        # Everything is fine, she changes it back to `database`
        self.name.setText('database')

        # And there is no errors
        self.assertFalse(self.form.nameError.visibility)
        self.assertFalse(self.form.nameFilledError.visibility)

        # Save button is still enabled
        self.assertTrue(self.form.createButton.isEnabled())
