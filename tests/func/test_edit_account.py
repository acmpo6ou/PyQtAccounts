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
from subprocess import Popen, PIPE, STDOUT

from tests.base import AccsTest, init_accounts_folder, init_src_folder
from core.utils import *
from PyQtAccounts import *


class EditAccountsTest(AccsTest):
    """
    This test class provides all functional tests for edit account form.
    """
    def setUp(self, name='database'):
        """
        Here we reassign some widely used variables and initialize in-memory
        file system.
        """
        super().setUp(name)
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
        self.username_radio = self.form.username_radio
        self.email_radio = self.form.email_radio

        # here we initialize in-memory file system because our tests will change
        # databases and sometimes save those changes but we don't want to change
        # our test databases so we use fake file system
        init_src_folder(self.monkeypatch)
        self.copyDatabase(name)

    def test_edit_content(self):
        """
        Here we test how content of account is loaded in edit account form.
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
        self.assertTrue(
            self.email_radio.isChecked(),
            "Email radio of edit form isn't checked when user has email set as "
            "what will be copied to mouseboard!")

    def test_edit_content_copy_username(self):
        """
        Here we test how content of account is loaded in edit account form when
        user has username set to be copied into mouseboard.
        """
        # we need another database for this test `database2` contains account
        # that has username set as what will be copied to mouseboard
        self.setUp(name='database2')
        self.username_radio = self.form.username_radio
        self.email_radio = self.form.email_radio

        # here we initialize fake file system and copy `database2` database in
        # there which we will use during tests
        init_src_folder(self.monkeypatch)
        self.copyDatabase('database2')

        # Chris wants to edit her account, so she chose it in the list and presses edit button
        self.list.selected(Index('stackoverflow'))
        self.editButton.click()

        # Edit form appears
        self.checkOnlyVisible(self.form)

        # Every field is filled as well
        self.assertEqual(
            self.account.text(), 'stackoverflow',
            'account name field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.name.text(), 'Chris Kirkman',
            'name field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.pass_input.text(), '930bU~1j.;nLS<Ga',
            'password field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.pass_repeat_input.text(), '930bU~1j.;nLS<Ga',
            'second password field of edit form is filled with incorrect data!'
        )
        self.assertEqual(
            self.email.text(), 'chris@gmail.com',
            'email field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.date.text(), '01.01.1995',
            'date field of edit form is filled with incorrect data!')
        self.assertEqual(
            self.comment.toPlainText(), '',
            'comment field of edit form is filled with incorrect data!')

        self.assertTrue(
            self.username_radio.isChecked(),
            "Username radio of edit form isn't checked when user has email set as "
            "what will be copied to mouseboard!")

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

        # He changes name, password, date, comment and what will be copied to
        # mouseboard
        self.account.setText('stackoverflow')
        self.pass_input.setText('mypass')
        self.pass_repeat_input.setText('mypass')
        self.name.setText('Tom')
        self.email.setText('tom@gmail.com')
        self.date.setDate(QDate(1997, 7, 10))
        self.comment.setText('I love stackoverflow!')
        self.username_radio.setChecked(True)

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
        self.assertFalse(account.copy_email,
                         "Copy e-mail of edited account is incorrect!")

        # And there is no longer `mega` in the list neither in database
        self.checkAccNotInList('mega')
        self.assertNotIn(
            'mega', getAkiList(self.win.db),
            'Old replica of edited account is still in the database!')

        # Tom then wants to view edited account
        self.list.selected(Index('stackoverflow'))

        # Show account form appears, and everything is fine
        self.checkOnlyVisible(self.accs.forms['show'])

        # He then goes to menu: File -> Copy
        self.account_menu(0, 2).trigger()

        # when he performs copy operation username is copied to mouseboard and
        # password to clipboard
        clipboard = QGuiApplication.clipboard()
        self.assertEqual(
            clipboard.text(),
            'mypass',  # those symbols are password
            "Password isn't copied to clipboard when performed "
            "copy operation in show account form!")

        # Username is copied to mouse clipboard by xclip tool
        xclip = Popen(['xclip', '-o'], stdout=PIPE, stderr=STDOUT)
        mouseboard = xclip.communicate()[0].decode()
        self.assertEqual(
            mouseboard, 'Tom\n',
            "Username isn't copied to mouse clipboard when performed"
            " copy operation in show account form!")

    def test_no_changes(self):
        """
        Here we test what happens when user didn't change anything and presses
        save button.
        """
        # Tom wants to edit database
        self.list.selected(Index('mega'))
        self.editButton.click()

        # then he changes his mind and presses save button without changing
        # anything
        self.saveButton.click()

        # Edit account form disappears
        self.checkOnlyVisible(self.help)

        # Account name doesn't changes in the list nor in database
        self.checkAccInList('mega')
        self.assertIn(
            'mega', getAkiList(self.win.db),
            'Account name has changed in account list after user'
            'didn\'t change anything in edit account form!')

        # Also it has all properties left unchanged
        account = self.win.db['mega']
        self.assertEqual(
            'mega', account.account,
            'account name of account that was edited, but doesn\'t changed is incorrect!'
        )
        self.assertEqual(
            b'tom', account.password,
            'password of account that was edited, but doesn\'t changed is incorrect!'
        )
        self.assertEqual(
            'Tom', account.name,
            'name of account that was edited, but doesn\'t changed is incorrect!'
        )
        self.assertEqual(
            'tom@gmail.com', account.email,
            'email of account that was edited, but doesn\'t changed is incorrect!'
        )
        self.assertEqual(
            '01.01.2000', account.date,
            'date of account that was edited, but doesn\'t changed is incorrect!'
        )
        self.assertEqual(
            'Mega account.', account.comment,
            'comment of account that was edited, but doesn\'t changed is incorrect!'
        )
        self.assertTrue(
            account.copy_email, "Copy e-mail of account that was edited, but "
            "doesn't changed is incorrect!")

        # Tom then wants to view edited account
        self.list.selected(Index('mega'))

        # Show account form appears, and everything is fine
        self.checkOnlyVisible(self.accs.forms['show'])

        # He then goes to menu: File -> Copy
        self.account_menu(0, 2).trigger()

        # when he performs copy operation e-mail is copied to mouseboard and
        # password to clipboard
        clipboard = QGuiApplication.clipboard()
        self.assertEqual(
            clipboard.text(),
            'tom',  # those symbols are password
            "Password isn't copied to clipboard when performed "
            "copy operation in show account form!")

        # E-mail is copied to mouse clipboard by xclip tool
        xclip = Popen(['xclip', '-o'], stdout=PIPE, stderr=STDOUT)
        mouseboard = xclip.communicate()[0].decode()
        self.assertEqual(
            mouseboard, 'tom@gmail.com\n',
            "Email isn't copied to mouse clipboard when performed"
            " copy operation in show account form!")

    def test_edit_attached_files(self):
        """
        Here we test editing of attached files.
        """
        # we need another database for this test, `database2` contains account
        # that has attached files
        self.setUp(name='database2')
        self.attach_list = self.form.attach_list
        self.attach_file_button = self.form.attach_file_button
        self.detach_button = self.form.detach_button

        # Bob has account with attached files that he wants to edit, so he chose
        # it in the list
        self.list.selected(Index('python'))
        self.editButton.click()

        # Edit form appears
        self.checkOnlyVisible(self.form)

        # and it has a list of attached files that contains 2 items
        self.assertEqual(
            self.attach_list.model().rowCount(), 2,
            'Attach list of create account form must have 2 items in it!')

        # it has `pyqt5.py` file
        model = self.attach_list.model()
        self.assertTrue(
            model.findItems('pyqt5.py'),
            'Attach list of edit account form must have `pyqt5.py` '
            'file in it!')

        # it has `somefile.txt` as well
        self.assertTrue(
            model.findItems('somefile.txt'),
            'Attach list of edit account form must have `somefile.txt` '
            'file in it!')

        # this files also have appropriate file mappings, which maps to None
        # because this files are already attached
        self.assertEqual(self.attach_list.pathmap, {
            'somefile.txt': None,
            'pyqt5.py': None
        }, "File mapping of edit account form is incorrect!")

        # Bob wants to detach `pyqt5.py`, so he chose it in the list and presses
        # detach button
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
        self.assertIn(
            'pyqt5.py', self.attach_list.pathmap,
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
            "File is not detached when user tries to detach it and presses `Yes` "
            "in confirmation dialog!")

        # there is button that Bob can use to add files to list, Bob presses
        # it and file dialog appears asking him to chose file to attach
        # Bob chose script.js
        self.monkeypatch.setattr(
            QFileDialog, 'getOpenFileName',
            self.mock_browse(
                f'{self.home}/Documents/PyQtAccounts/tests/func/src/attach_files/script.js'
            ))

        self.attach_file_button.click()

        # `script.js` appears in the attach list
        self.assertTrue(
            self.attach_list.model().findItems('script.js'),
            "File name of attached file doesn't appear in the attach list!")

        # and in the dict that maps attached file name to file path
        self.assertEqual(
            self.attach_list.pathmap['script.js'],
            f'{self.home}/Documents/PyQtAccounts/tests/func/src/attach_files/script.js',
            "Mapping from attached file name to its path doesn't created!")

        # satisfied with his attached files Bob presses `Save` button
        self.saveButton.click()

        # The edit account form disappears
        self.checkOnlyVisible(self.accs.tips['help'])

        # account is saved and attached_files is changed
        acc = self.win.db['python']
        expected_attached_files = {
            'somefile.txt': b'This is a simple file.\nTo test PyQtAccounts.'
            b'\nHello World!\n',
            'script.js': b"var py = 'PyQtAccounts';\n"
        }
        self.assertEqual(
            expected_attached_files, acc.attached_files,
            "Attached files dictionary of edited account is incorrect!")
