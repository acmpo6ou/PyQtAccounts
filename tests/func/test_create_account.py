#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh Bogdan
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

        self.attach_label = self.form.attach_label
        self.attach_list = self.form.attach_list
        self.attach_file_button = self.form.attach_file_button
        self.detach_button = self.form.detach_button

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

    def test_attach_files(self):
        """
        Here we test attach files feature of create account form.
        """
        # we must use real HOME environment variable for this test
        os.environ['HOME'] = f'/home/{os.getlogin()}'

        # Toon wants to create account and attach some files to it
        self.accs.panel.addButton.click()

        # he fills only required fields
        QTest.keyClicks(self.account_name, 'tf2')
        QTest.keyClicks(self.pass_input, 'something')
        QTest.keyClicks(self.pass_repeat_input, 'something')

        # then he finds label that says `attach files`
        self.assertEqual(self.attach_label.text(), 'Додати файли:',
                         "Message of attach label is incorrect!")

        # there is also an empty list under it
        self.assertEqual(
            self.attach_list.model().rowCount(), 0,
            'Attach list of create account form must be empty when'
            'form is just displayed!')

        # there is button that Toon can use to add files to list, Toon presses
        # it and file dialog appears asking him to chose file to attach
        def mock_browse(path):
            """
            This function constructs test double of getOpenFileName so it will
            simulate that user chose file in open file dialog.
            """
            def wrap(parrent, caption, folder):
                """
                We use this function to monkeypatch getOpenFileName and check
                arguments that are passed to it.
                """
                assert caption == "Виберіть файл для закріплення",\
                        "Title of attach file dialog is incorrect!"
                assert folder == os.getenv('HOME'),\
                       "Default folder of attach file dialog must be a home folder!"
                return (path, )

            return wrap

        # Toon chose somefile.txt
        self.monkeypatch.setattr(
            QFileDialog, 'getOpenFileName',
            mock_browse(
                'Documents/PyQtAccounts/tests/func/src/attach_files/somefile.txt'
            ))

        self.attach_file_button.click()

        # `somefile.txt` appears in the attach list
        self.assertTrue(
            self.attach_list.model().findItems('somefile.txt'),
            "File name of attached file doesn't appear in the attach list!")

        # and in the dict that maps attached file name to file path
        self.assertEqual(
            self.attach_list.pathmap['somefile.txt'],
            'Documents/PyQtAccounts/tests/func/src/attach_files/somefile.txt',
            "Mapping from attached file name to its path doesn't created!")

        # so Toon attaches another file
        self.monkeypatch.setattr(
            QFileDialog, 'getOpenFileName',
            mock_browse(
                'Documents/PyQtAccounts/tests/func/src/attach_files/pyqt5.py'))

        self.attach_file_button.click()

        # and he attaches another one, that has the same name as already
        # attached file - `somefile.txt`
        self.monkeypatch.setattr(
            QFileDialog, 'getOpenFileName',
            mock_browse(
                'Documents/PyQtAccounts/tests/func/src/attach_files/sub/somefile.txt'
            ))

        # Warning message appears saying that file with such name already
        # exists, this message asks Toon what he would like to do – replace
        # existing file or abort the operation
        # Toon answers `No`
        self.monkeypatch.setattr(
            QMessageBox, 'warning',
            self.mess('Увага!',
                      "Файл з таким іменем вже існує, замінити?",
                      button=QMessageBox.No))

        self.attach_file_button.click()

        # `somefile.txt` is still in the list and it name still has the old mapping
        self.assertEqual(
            self.attach_list.pathmap['somefile.txt'],
            'Documents/PyQtAccounts/tests/func/src/attach_files/somefile.txt',
            "Mapping from attached file name to its path is replaced when user "
            "tried to attach file with same name and pressed `No` in "
            "confirmation dialog!")

        self.assertTrue(
            self.attach_list.model().findItems('somefile.txt'),
            "File name of attached file disappears from attach list when user "
            "tried to attach file with same name and pressed `No` in "
            "confirmation dialog!")

        # Toon then changed his mind and attaches `sub/somefile.txt` replacing
        # existing `somefile.txt`
        self.monkeypatch.setattr(
            QFileDialog, 'getOpenFileName',
            mock_browse(
                'Documents/PyQtAccounts/tests/func/src/attach_files/sub/somefile.txt'
            ))

        # Warning message appears saying that file with such name already
        # exists, this message asks Toon what he would like to do – replace
        # existing file or abort the operation
        # Toon answers `Yes`
        self.monkeypatch.setattr(
            QMessageBox, 'warning',
            self.mess('Увага!',
                      "Файл з таким іменем вже існує, замінити?",
                      button=QMessageBox.Yes))

        self.attach_file_button.click()

        # `somefile.txt` is still in the list but it name has another mapping
        self.assertEqual(
            self.attach_list.pathmap['somefile.txt'],
            'Documents/PyQtAccounts/tests/func/src/attach_files/sub/somefile.txt',
            "Mapping from attached file name to its path isn't replaced when user "
            "tried to attach file with same name and pressed `Yes` in "
            "confirmation dialog!")

        self.assertTrue(
            self.attach_list.model().findItems('somefile.txt'),
            "File name of attached file disappears from attach list when user "
            "tried to attach file with same name and pressed `Yes` in "
            "confirmation dialog!")

        # Toon then wants to attach another file, but then changes his mind and
        # presses `Cancel` in chose file dialog
        self.monkeypatch.setattr(QFileDialog, 'getOpenFileName',
                                 mock_browse(''))
        self.attach_file_button.click()

        # the empty file name doesn't appear in the attach list
        self.assertEqual(
            2,
            self.attach_list.model().rowCount(),
            "The empty file name was added when user tries to "
            "attach file and presses `Cancel` in chose file dialog!")

        # also there is no empty mapping
        self.assertNotIn(
            '', self.attach_list.pathmap,
            "The empty file mapping was added when user tries to "
            "attach file and presses `Cancel` in chose file dialog!")

        # Toon then decides to detach `pyqt5.py` file:
        # so he chose it in the list
        self.form.file_selected(Index('pyqt5.py'))

        # He presses detach button, but suddenly changes his mind and presses
        # `No` in confirmation dialog
        self.monkeypatch.setattr(
            QMessageBox, 'warning',
            self.mess('Увага!',
                      "Ви впевнені що хочете відкріпити <b>pyqt5.py</b>?",
                      button=QMessageBox.No))
        self.detach_button.click()

        # `pyqt5.py` is still in the list and has its mapping
        self.assertEqual(
            self.attach_list.pathmap['pyqt5.py'],
            'Documents/PyQtAccounts/tests/func/src/attach_files/pyqt5.py',
            "File mapping was deleted when user tries to detach file "
            "associated with it but presses `No` in confirmation dialog!")

        self.assertTrue(
            self.attach_list.model().findItems('pyqt5.py'),
            "File was detached when user tries to detach it but presses `No` "
            "in confirmation dialog!")

        # Toon then changes his mind again and detaches `pyqt5.py` pressing
        # `Yes` in confirmation dialog
        self.monkeypatch.setattr(
            QMessageBox, 'warning',
            self.mess('Увага!',
                      "Ви впевнені що хочете відкріпити <b>pyqt5.py</b>?",
                      button=QMessageBox.Yes))
        self.detach_button.click()

        # and `pyqt5.py` is detached, there is no longer mapping for it neither
        # it exists in the list
        self.assertNotIn(
            'pyqt5.py', self.attach_list.pathmap,
            "File mapping isn't deleted when user tries to detach the file and "
            "presses `Yes` in confirmation dialog!")

        self.assertFalse(
            self.attach_list.model().findItems('pyqt5.py'),
            "File isn't removed from attach list when user tries to detach it "
            "and presses `Yes` in confirmation dialog!")

        # satisfied with his attached files Toon presses `Create` button
        self.createButton.click()

        # The create form disappears
        self.checkOnlyVisible(self.accs.tips['help'])

        # `tf2` appears in the account list
        self.checkAccInList('tf2')

        # And it is in the database and has all keys and values
        self.assertIn('tf2', self.win.db,
                      'Account has not appeared in database after creation!')
        acc = self.win.db['tf2']
        self.assertEqual('tf2', acc.account,
                         'account field of created account is incorrect!')
        self.assertEqual(b'something', acc.password,
                         'password field of created account is incorrect!')
        expected_attached_files = {
            'somefile.txt': b"Some another file.\n<h1></h1>\n"
        }
        self.assertEqual(
            expected_attached_files, acc.attached_files,
            "Attached files dictionary of created account is incorrect!")
