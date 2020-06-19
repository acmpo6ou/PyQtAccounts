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

from tests.base import AccsTest
from core.utils import *
from PyQtAccounts import *


class CreateAccTest(AccsTest):
    """
    This test class provides all functional tests about creating accounts.
    """
    def setUp(self):
        """
        Here we reassign some widely used variables. 
        """
        super().setUp()
        self.form = self.accs.forms['create']
        self.help_tip = self.accs.tips['help']

        self.account_name = self.form.accountInput
        self.name = self.form.nameInput
        self.nameError = self.form.nameError
        self.nameFilledError = self.form.nameFilledError

        self.passFilledError = self.form.passFilledError
        self.passEqError = self.form.passEqError
        self.pass_input = self.form.passField.passInput
        self.pass_repeat_input = self.form.passRepeatField.passInput

        self.email = self.form.emailInput
        self.date = self.form.dateInput
        self.comment = self.form.commentInput

        self.createButton = self.form.createButton
        self.cancelButton = self.form.cancelButton

        self.copy_label = self.form.copy_label
        self.username_radio = self.form.username_radio
        self.email_radio = self.form.email_radio

    def checkNameErrors(self):
        """
        This is a method which will check for name errors.
        """
        self.assertFalse(self.nameError.visibility,
                         'Name error is visible when it shouldn\'t be!')
        self.assertFalse(
            self.nameFilledError.visibility,
            'Name filled error is visible when it shouldn\'t be!')

    def test_create_account_click(self):
        """
        This test tests opening of create account form by clicking on `+` button.
        """
        self.accs.panel.addButton.click()
        self.checkOnlyVisible(self.form)

    def test_create_account_menu(self):
        """
        This test tests opening of create account form through menu.
        """
        # Here we obtain menu action to open create account form
        self.account_menu(0, 0).trigger()
        self.checkOnlyVisible(self.form)

    def test_validate_name(self):
        """
        This test tests name validation.
        """
        # Tom wants to create account, for now there is no errors
        self.accs.panel.addButton.click()
        self.checkNameErrors()

        # He starts typing `gma` at the name field
        QTest.keyClicks(self.account_name, 'gma')

        # There is no errors
        self.checkNameErrors()

        # Toon then continue and types `il`
        QTest.keyClicks(self.account_name, 'il')

        # The error message appears saying that account with such name exists
        self.assertTrue(
            self.nameError.visibility,
            'Error message does not appears when name of account that'
            'already exists is in name field!')

        # He then types `2` to account name field
        QTest.keyClicks(self.account_name, '2')

        # The error message disappears
        self.assertFalse(
            self.nameError.visibility,
            'Name error does not disappear when name of account'
            'that already exists is no longer in the name field!')

        # Toon then erases account name
        self.account_name.setText('')

        # Another error message appears saying that he must feel account name field
        self.assertTrue(
            self.nameFilledError.visibility,
            'The error message does not appears when name field of'
            'create account form is not filled!')

        # Toon then types `someaccount` to name field
        self.account_name.setText('someaccount')

        # The error message disappears
        self.assertFalse(
            self.nameFilledError.visibility,
            'The filled error message does not disappears when name field of'
            'create account form is filled!')

    def test_create_button_enabled(self):
        """
        This tests tests whether create button is enabled or not in certain
        cases.
        """
        # Bob wants to create new account, create is button disabled
        self.accs.panel.addButton.click()
        self.assertFalse(
            self.createButton.isEnabled(),
            'Create button is not disabled when create form is just'
            'opened!')

        # He fills account name field and create button is still disabled
        self.account_name.setText('someaccount')
        self.assertFalse(
            self.createButton.isEnabled(),
            'Create button is not disabled when password fields'
            'aren\'t filled!')

        # He then fills password fields
        self.pass_input.setText('some_password')
        self.pass_repeat_input.setText('some_password')

        # Create button enables now
        self.assertTrue(
            self.createButton.isEnabled(),
            'Create button is not enabled when name and password'
            'fields of create account form are filled!')

        # Bob then erases name field, create button disables
        self.account_name.setText('')
        self.assertFalse(
            self.createButton.isEnabled(),
            'Create button is not enabled when name field is'
            'cleared!')

        # He then types `gmail` at the name field and create button is still disabled
        self.account_name.setText('gmail')
        self.assertFalse(
            self.createButton.isEnabled(),
            'Create button is not disabled when name of account '
            'that already exists is typed in name field!')

        # Then Bob changes it to `Gmail`, create button enables
        self.account_name.setText('Gmail')
        self.assertTrue(
            self.createButton.isEnabled(),
            'Create button is not enabled when name field no longer'
            'contains name of account that already exists!')

        # He then changes password in first field to `pass`
        self.pass_input.setText('pass')

        # Create button disables
        self.assertFalse(
            self.createButton.isEnabled(),
            'Create button is not disabled when password fields'
            'contain different passwords!')

        # Bob then erases both passwords and create button is still disabled
        self.pass_input.setText('')
        self.pass_repeat_input.setText('')
        self.assertFalse(
            self.createButton.isEnabled(),
            'Create button is not disabled when password fields '
            'are both erased!')

        # Bob then fills them again
        self.pass_input.setText('pass')
        self.pass_repeat_input.setText('pass')

        # And create button enables now
        self.assertTrue(
            self.createButton.isEnabled(),
            'Create button is not enabled when password fields are'
            'both filled with same password!')

    def test_create_button(self):
        """
        This test tests create button of create form.
        """
        # Lea wants to create account
        self.accs.panel.addButton.click()

        # There is copy section in this form:
        # it has label that says what will be copied
        self.assertEqual(
            self.copy_label.text(),
            'Тут ви можете вибрати що буде копіюватися до\n'
            'мишиного буферу:',
            'Message of copy label in create account form is incorrect!')

        # also it has two radio buttons that allow user to chose what will be
        # copied, e-main radio button is checked by default
        self.assertTrue(
            self.email_radio.isChecked(),
            'E-mail radio button in create account form must be checked by default!'
        )
        self.assertFalse(
            self.username_radio.isChecked(),
            'Username radio button in create account form must be unchecked by default!'
        )

        # this radio buttons have appropriate names: `email` and `username`
        self.assertEqual(self.email_radio.text(), 'E-mail',
                         'Text of e-mail radio button is incorrect!')
        self.assertEqual(self.username_radio.text(), 'Username',
                         'Text of username radio button is incorrect!')

        # Lea wont use default copy settings
        self.username_radio.setChecked(True)

        # She fills all fields
        QTest.keyClicks(self.account_name, 'someaccount')
        QTest.keyClicks(self.name, 'somename')
        QTest.keyClicks(self.pass_input, 'some_password')
        QTest.keyClicks(self.pass_repeat_input, 'some_password')
        QTest.keyClicks(self.email, 'example@gmail.com')
        QTest.keyClicks(self.comment, 'Comment of account.')

        # Everything is fine so she presses `create` button
        self.createButton.click()

        # The create form disappears
        self.checkOnlyVisible(self.accs.tips['help'])

        # `someaccount` appears in the account list
        self.checkAccInList('someaccount')

        # And it is in the database and has all keys and values
        self.assertIn('someaccount', self.win.db,
                      'Account has not appeared in database after creation!')
        acc = self.win.db['someaccount']
        self.assertEqual('someaccount', acc.account,
                         'account field of created account is incorrect!')
        self.assertEqual('somename', acc.name,
                         'name field of created account is incorrect!')
        self.assertEqual(b'some_password', acc.password,
                         'password field of created account is incorrect!')
        self.assertEqual('example@gmail.com', acc.email,
                         'email field of created account is incorrect!')
        self.assertEqual(False, acc.copy_email,
                         'copy_email field of created account is incorrect!')
        self.assertEqual('01.01.2000', acc.date,
                         'date field of created account is incorrect!')
        self.assertEqual('Comment of account.', acc.comment,
                         'comment field of created account is incorrect!')

    def test_cancel_button(self):
        """
        Here we test the cancel button of create account form. It must hide the
        form and clear it.
        """
        # Lea wants to create account
        self.accs.panel.addButton.click()

        # Lea wont use default copy settings
        self.username_radio.setChecked(True)

        # She fills all fields
        QTest.keyClicks(self.account_name, 'someaccount')
        QTest.keyClicks(self.name, 'somename')
        QTest.keyClicks(self.pass_input, 'some_password')
        QTest.keyClicks(self.pass_repeat_input, 'some_password')
        QTest.keyClicks(self.email, 'example@gmail.com')
        self.date.setDate(QDate(1990, 5, 2))
        QTest.keyClicks(self.comment, 'Comment of account.')

        # suddenly she changes her mind and presses `Cancel` button
        self.cancelButton.click()

        # create account form disappears
        self.checkOnlyVisible(self.help_tip)

        # and all fields of create account form are cleared
        self.assertEqual(
            self.account_name.text(), '',
            'Account-name field of create account form is not cleared when user '
            'pressed cancel button!')
        self.assertEqual(
            self.name.text(), '',
            'Name field of create account form is not cleared when user '
            'pressed cancel button!')
        self.assertEqual(
            self.pass_input.text(), '',
            'First password field of create account form is not cleared when user '
            'pressed cancel button!')
        self.assertEqual(
            self.pass_repeat_input.text(), '',
            'Second password field of create account form is not cleared when user '
            'pressed cancel button!')
        self.assertEqual(
            self.email.text(), '',
            'Email field of create account form is not cleared when user '
            'pressed cancel button!')
        self.assertEqual(
            self.comment.toPlainText(), '',
            'Comment field of create account form is not cleared when user '
            'pressed cancel button!')
        self.assertEqual(
            self.date.text(), '01.01.2000',
            'Date field of create account form is not cleared when user '
            'pressed cancel button!')
        self.assertTrue(
            self.email_radio.isChecked(),
            'Copy section of create account form is not cleared when user '
            'pressed cancel button!')
