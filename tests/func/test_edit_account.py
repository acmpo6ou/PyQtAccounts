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
import unittest
import pytest
import os

from tests.base import AccsTest, init_accounts_folder, init_src_folder
from core.utils import *
from PyQtAccounts import *


class EditAccsTest(AccsTest):
    """
    This test class provides all functional tests for edit account form.
    """
    def setUp(self):
        """
        Here we reassign some widely used variables and initialize in-memory
        file system.
        """
        super().setUp()
        self.form = self.accs.forms['edit']
        self.list = self.accs.list
        self.help = self.accs.tips['help']

        self.editButton = self.accs.panel.editButton
        self.deleteButton = self.form.deleteButton
        self.saveButton = self.form.createButton

        self.account = self.form.accountInput
        self.name = self.form.nameInput
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput
        self.email = self.form.emailInput
        self.date = self.form.dateInput
        self.comment = self.form.commentInput

        # here we initialize in-memory file system because our tests will change
        # databases and sometimes save those changes but we don't want to change
        # our test databases so we use fake file system
        init_src_folder(self.monkeypatch)
        self.copyDatabase('database')

    def test_edit_content(self):
        """
        Here we test editing of account in edit account form.
        """
        # Lea wants to edit her account, so she chose it in the list and presses edit button
        self.list.selected(Index('habr'))
        self.editButton.click()

        # Edit form appears
        self.checkOnlyVisible(self.form)

        # Every field is filled as well
        self.assertEqual(
            self.account.text(), 'habr',
            'account name field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.name.text(), 'Lea',
            'name field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.pass_input.text(), 'habr_password',
            'password field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.pass_repeat_input.text(), 'habr_password',
            'second password field of edit form is filled with incorrect data!'
        )
        self.assertEqual(
            self.email.text(), 'spheromancer@habr.com',
            'email field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.date.text(), '19.05.1990',
            'date field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.comment.toPlainText(), 'Habr account.',
            'comment field of edit form is filled with incorrect data!')

    def test_delete_button(self):
        """
        This test tests delete button of edit account form.
        """
        # Toon wants to delete his account, so he chose it in the list and
        # presses edit button
        self.list.selected(Index('mega'))
        self.editButton.click()

        # He then presses delete button
        # Warning message appears and Toon changes his mind pressing `No`
        self.monkeypatch.setattr(
            QMessageBox, 'warning',
            self.mess('Увага!',
                      'Ви певні що хочете видалити акаунт <i><b>mega</b></i>',
                      QMessageBox.No))
        self.deleteButton.click()

        # account `mega` is still in the list and in the database too
        self.checkAccInList('mega')
        self.assertIn(
            'mega', getAkiList(self.win.db),
            'Account is not in the list when user presses delete '
            'button and then presses `No` in confirmation dialog!')

        # Toon changes his mind again presses delete button and `Yes` in the warning dialog
        self.monkeypatch.setattr(
            QMessageBox, 'warning',
            self.mess('Увага!',
                      'Ви певні що хочете видалити акаунт <i><b>mega</b></i>',
                      QMessageBox.Yes))
        self.deleteButton.click()

        # edit form disappears
        self.checkOnlyVisible(self.help)

        # account `mega` disappears from the list
        self.checkAccNotInList('mega')

        # And it deleted from database too
        self.assertNotIn(
            'mega', getAkiList(self.win.db),
            'Account has not deleted from database after user'
            'presses delete button in edit account form!')

    def test_save_button(self):
        """
        Here we test save button of edit account form.
        """
        # Tom wants to edit database
        self.list.selected(Index('mega'))
        self.editButton.click()

        # He changes name and password
        self.account.setText('stackoverflow')
        self.pass_input.setText('mypass')
        self.pass_repeat_input.setText('mypass')
        self.name.setText('Tom')
        self.email.setText('tom@gmail.com')
        self.date.setDate(QDate(1997, 7, 10))
        self.comment.setText('I love stackoverflow!')

        # Everything is fine so he presses save button
        self.saveButton.click()

        # Edit account form disappears
        self.checkOnlyVisible(self.help)

        # Account name changes in the list and in database
        self.checkAccInList('stackoverflow')
        self.assertIn(
            'stackoverflow', getAkiList(self.win.db),
            'Account name has not changed in account list after '
            'editing it from edit account form!')

        # Also it has all properties as well
        account = self.win.db['stackoverflow']
        self.assertEqual('stackoverflow', account.account,
                         'account name of edited account is incorrect!')
        self.assertEqual(b'mypass', account.password,
                         'password of edited account is incorrect!')
        self.assertEqual('Tom', account.name,
                         'name of edited account is incorrect!')
        self.assertEqual('tom@gmail.com', account.email,
                         'email of edited account is incorrect!')
        self.assertEqual('10.07.1997', account.date,
                         'date of edited account is incorrect!')
        self.assertEqual('I love stackoverflow!', account.comment,
                         'comment of edited account is incorrect!')

        # And there is no longer `mega` in the list neither in database
        self.checkAccNotInList('mega')
        self.assertNotIn(
            'mega', getAkiList(self.win.db),
            'Old replica of edited account is still in the database!')

        # Tom then wants to view edited account
        self.list.selected(Index('stackoverflow'))

        # Show account form appears, and everything is fine
        self.checkOnlyVisible(self.accs.forms['show'])

    def test_no_changes(self):
        """
        Here we test what happens when user didn't change anything and presses
        save button.
        """
