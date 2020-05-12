#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh B.
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

"""
This module contains test case classes and helpful functions that are used by tests.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtTest import QTest
from unittest.mock import Mock

import unittest
import pytest
import shutil
import sys
import os
import time
import setup
import core.const

from PyQtAccounts import *
from setup import InstallationWizard


class BaseTest(unittest.TestCase):
    """
    Base test superclass almost all tests are inherit from it.
    """
    def setUp(self):
        """
        This method setts up environment for every test, here we set TESTING environment variable
        to True, for example adjusted hide and show functions from testutils module use it to
        determine whether they should construct (or destruct) windows or not. This variable is like
        a signal for program that it is running under test, this strategy very helpful.
        """
        os.environ['TESTING'] = 'True'

    @pytest.fixture(autouse=True)
    def monkeypatching(self, monkeypatch):
        """
        This method is a fixture that defines monkeypatch attribute for test class, because pytest
        doesn't pass monkeypatch to methods, only to functions.
        :param monkeypatch:
        Monkeypatch instance
        """
        self.monkeypatch = monkeypatch

    @pytest.fixture(autouse=True)
    def bot(self, qtbot):
        """
        This method is a fixture that defines qbot attribute for test class, because pytest
        doesn't pass qtbot to methods, only to functions.
        :param qtbot:
        QtBot instance
        """
        self.qbot = qtbot

    def menu(self, submenu_index, action_index):
        """
        This method returns menu action instance (QAction) by given index of submenu and index
        of menu action.
        :param submenu_index:
        index of submenu that contains menu action we want to get, type int
        :param action_index:
        index of menu action we want to get, type int
        :return:
        menu action, type QAction
        """
        submenu = self.window.menuBar().actions()[submenu_index]
        return submenu.menu().actions()[action_index]

    @staticmethod
    def import_database_dialog(result):
        """
        This method constructs mock function for chose file dialog from QFileDialog module,
        in this case file dialog that user will use to chose database that program will import.
        :param result:
        Result that open file dialog returns, i.e. tuple first element of which is path to file
        being chosen. Using this parameter we can simulate user respond to dialog.
        :return:
        mock function that will mock import database dialog.
        """
        def file_dialog(caption, filter, directory):
            """
            This is a mock function itself, it checks whether arguments being passed are right,
            and returns, specified in `result`, tuple with path to file which we use to simulate
            user respond to dialog.
            :return:
            tuple first element of which is path to file that fake user is chose
            """
            assert caption == 'Імпортувати базу данних'
            assert filter == 'Tarball (*.tar)'
            assert directory == os.getenv('HOME')
            return result

        return file_dialog

    @staticmethod
    def export_database_dialog(name, result):
        """
        This method constructs mock function for chose folder dialog from QFileDialog module,
        in this case dialog that user will use to chose folder where program will export database.
        :param name:
        name of database that fake user wants export
        :param result:
        Result that open directory dialog returns, i.e. tuple first element of which is path to that
        directory that fake user chose. Using this parameter we can simulate user respond to dialog.
        :return:
        mock function that will mock export database dialog.
        """
        def export_database_dialog(caption, filter, directory):
            """
            This is a mock function itself, it checks whether arguments being passed are right,
            and returns, specified in `result`, tuple with path to folder which we use to simulate
            user respond to dialog.
            :return:
            tuple first element of which is path to folder that fake user is chose
            """
            home = os.getenv('HOME')
            assert caption == 'Експортувати базу данних'
            assert filter == 'Tarball (*.tar)'
            assert directory == f'{home}/{name}.tar'
            return result

        return export_database_dialog

    @staticmethod
    def mess(head, text, button=QMessageBox.Ok):
        """
        This method constructs mock function for dialogs from QMessageBox module.
        :param head:
        :param text:
        :param button:
        Button code that mock function will return when called, that code represents button that
        user pressed (e.g. QMessageBox.Ok). Using this code we can simulate user clicks on the
        dialog buttons.
        :return:
        mock function that will mock some function from QMessageBox.
        """
        def mess(parent, this_head, this_text, *args, **kwargs):
            """
            This is a mock function itself, it checks whether arguments being passed are right,
            and returns, specified in `button`, button code that we use to simulate user respond to
            dialog i.e. button that he click.
            :return:
            button code that represents button that fake user clicks as respond to dialog.
            """
            assert this_head == head
            assert this_text == text
            return button

        return mess

    @staticmethod
    def mess_showed(*args, **kwargs):
        """
        This is a mock function that mocks dialogs that shouldn't be showed, if this dialogs are
        showed something isn't right and we throw exception.
        """
        raise AssertionError(f"The message showed, but it shouldn't be!\n"
                             f"Args: {args}\n"
                             f"Kwargs: {kwargs}")

    @staticmethod
    def critical(parent, head, text):
        """
        This is a mock function that mocks critical dialogs (i.e. error dialogs), it simply
        checks whether title is right (we don't check error message itself) and returns `Ok`
        button code to emulate dialog. close.
        """
        assert head == 'Помилка!'
        return QMessageBox.Ok

    @staticmethod
    def copyDatabase(name):
        """
        This method copies test databases to in memory filesystem, because it is faster to edit
        them in memory and it prevents collisions.
        :param name:
        name of the database which files we want to copy.
        """
        # here we copy database .db and .bin files to fake src directory in fake filesystem
        shutil.copy(f'tests/src/{name}.db', '/home/accounts/test/src')
        shutil.copy(f'tests/src/{name}.bin', '/home/accounts/test/src')


class UnitTest(BaseTest):
    """
    This class is a test case for unit tests, it contains all methods that are specific to
    them.
    """
    def patchVersion(self):
        """
        This function is used to mock some classes from git module which getVersion function
        uses to identify which version of PyQtAccounts is installed.
        """
        class Tag:
            """
            This is a double of Tag class from git module.
            """
            def __init__(self, name, date):
                """
                In this constructor we save tags name and fake date of its creation.
                :param name:
                name of the tag
                :param date:
                date of tags creation, it is not necessarily for this parameter to be real date,
                it can be any number.
                """
                self.name = name
                self.commit = Mock()
                self.commit.committed_datetime = date

            def __str__(self):
                """
                This method simulates __str__ from real Tag class.
                :return:
                tags name
                """
                return self.name

        class Repo:
            """
            This is a mock for Repo class from git module, we use it create fake tags for
            repository.
            """
            def __init__(self, *args):
                """
                In constructor we simply create fake tags using Tag mock class.
                """
                self.tags = []
                for i, name in enumerate(['v1.0.0', 'v1.0.2', 'v2.0.6']):
                    # tag will have its name from the list and `i` variable will represent
                    # its date of creation. getVersion sorts tags by its date but its actually
                    # doesn't matter will it be real date or just number.
                    self.tags.append(Tag(name, i))

        # here we monkeypatch Repo class
        self.monkeypatch.setattr(git, 'Repo', Repo)


class FuncTest(BaseTest):
    """
    This class is a test case for functional tests, it contains all methods that are specific to
    them. It is a superclass for DbsTest and AccsTest.
    """
    def setUp(self):
        """
        This method sets up everything specific for functional tests.
        """
        super().setUp()
        # here we create application main window and dbs instance which both DbsTest and AccsTest
        # are using.
        self.window = Window()
        self.dbs = self.window.dbs

        # here we initialize fake /home/accounts folder and fake src directory in it
        init_accounts_folder()
        init_src_folder(self.monkeypatch)

        # here we copy all test databases into test src folder.
        self.copyDatabase('main')
        self.copyDatabase('crypt')
        self.copyDatabase('a')
        self.copyDatabase('database')
        self.copyDatabase('import_database')

    def check_only_visible(self, elem, parent):
        """
        This method is used to check that `elem` parameter is the only visible widget in parent
        (e.g Dbs or Accs instance) and other elements in parent are hidden.
        Note: that you should not call this method directly, DbsTest and AccsTest will implement
        checkOnlyVisible method that will call check_only_visible with specified parent parameter.
        :param elem:
        tip or form that we want to check on visibility.
        :param parent:
        Dbs or Accs instance which contains forms and tips (and elem as well).
        """
        # here we check every form of parent:
        # if this form is elem we check whether it is visible
        # if form isn't elem we check whether it is hidden
        for form in parent.forms:
            if parent.forms[form] == elem:
                self.assertTrue(parent.forms[form].visibility)
                continue
            self.assertFalse(parent.forms[form].visibility)

        # here we check every tip of parent:
        # if this tip is elem we check whether it is visible
        # if tip isn't elem we check whether it is hidden
        for tip in parent.tips:
            if parent.tips[tip] == elem:
                self.assertTrue(parent.tips[tip].visibility)
                continue
            self.assertFalse(parent.tips[tip].visibility)

    @staticmethod
    def check_in_list(name, parent):
        """
        This function checks whether given element is in the list of parent.
        Note: that you should not call this method directly, DbsTest and AccsTest will implement
        their method that will call check_in_list with specified parent parameter.
        :param name:
        name of the element (e.g. database or account).
        :param parent:
        Dbs or Accs instance which contains list.
        """
        # here we obtain the model of the parents list
        model = parent.list.model

        # then we iterate trough every index of the model if we don't find index data of which
        # equal to given `name` parameter then we throw AssertionError with appropriate message
        for i in range(model.rowCount()):
            index = model.item(i)
            if index.text() == name:
                break
        else:
            raise AssertionError(f'{name} not in the list of {parent}!')

    def check_not_in_list(self, name, parent):
        """
        This function checks whether given element is NOT in the list of parent.
        Note: that you should not call this method directly, DbsTest and AccsTest will implement
        their method that will call check_not_in_list with specified parent parameter.
        :param name:
        name of the element (e.g. database or account).
        :param parent:
        Dbs or Accs instance which contains list.
        """
        try:
            # here we to check is given element IS in the list
            self.check_in_list(name, parent)
        except AssertionError:
            # if AssertionError caught then it is OK, element is NOT in the list, so we do nothing
            pass
        else:
            # and if there is no exceptions then element IS in the list and it is not right, so we
            # throw AssertionError with appropriate message
            raise AssertionError(f"{name} is IN the list of {parent}, but it shouldn't be!")


class DbsTest(FuncTest):
    """
    This class is a test case for everything that about databases.
    """
    def checkOnlyVisible(self, elem):
        """
        This method is used to check that `elem` parameter is the only visible widget in Dbs
        instance and other elements in Dbs are hidden.
        It calls check_only_visible with specified parent parameter (Dbs instance).
        :param elem:
        tip or form that we want to check on visibility.
        """
        self.check_only_visible(elem, self.dbs)

    def checkDbInList(self, name):
        """
        This method is used to check whether given database is in the database list.
        It calls check_in_list method with specified `parent` parameter (Dbs instance).
        :param name:
        name of the database
        """
        self.check_in_list(name, self.dbs)

    def checkDbNotInList(self, name):
        """
        This method is used to check whether given database is NOT in the database list.
        It calls check_not_in_list method with specified `parent` parameter (Dbs instance).
        :param name:
        name of the database
        """
        self.check_not_in_list(name, self.dbs)

    def checkDbOnDisk(self, name):
        """
        This method is used to check whether files of given database are on the disk or not.
        :param name:
        name of the database
        """
        # here we check existence of database file and saltfile in the test src directory.
        self.assertTrue(os.path.exists(f'/home/accounts/test/src/{name}.bin'))
        self.assertTrue(os.path.exists(f'/home/accounts/test/src/{name}.db'))

    def checkDbNotOnDisk(self, name):
        """
        This method is used to check whether files of given database are NOT on the disk or they
        are.
        :param name:
        name of the database
        """
        # here we check inexistence of database file and saltfile in the test src directory.
        self.assertFalse(os.path.exists(f'/home/accounts/test/src/{name}.bin'))
        self.assertFalse(os.path.exists(f'/home/accounts/test/src/{name}.db'))


class AccsTest(FuncTest):
    """
    This class is a test case for everything that about accounts.
    """
    def setUp(self, name='database', password='some_password'):
        """
        This method is called before each accounts test, it opens test database because in
        account tests we need to test accounts and accounts are stored in database.
        :param name:
        name of the database we which contains our test accounts, by default we open `database`
        but in some cases we need to open another one.
        :param password:
        password to database specified in name parameter, by default it is `some_password` (i.e.
        password to `database`).
        """
        super().setUp()

        # Here we initialize accounts and src test folders (i.e. that are in fake file
        # system). Then we copy database specified in `name` parameter to test src directory.
        init_accounts_folder()
        init_src_folder(self.monkeypatch)
        self.copyDatabase(name)

        # here we open database
        form = self.dbs.forms['open']
        self.list = self.dbs.list
        self.pass_input = form.passField.passInput
        self.list.selected(Index(name))
        self.pass_input.setText(password)
        form.openButton.click()

        # and here we save database window and accs instance
        self.win = self.window.windows[1]
        self.accs = self.win.accs

    def checkOnlyVisible(self, elem):
        """
        This method is used to check that `elem` parameter is the only visible widget in Accs
        instance and other elements in Accs are hidden.
        It calls check_only_visible with specified parent parameter (Accs instance).
        :param elem:
        tip or form that we want to check on visibility.
        """
        self.check_only_visible(elem, self.accs)

    def checkAccInList(self, name):
        """
        This method is used to check whether given account is in the account list.
        It calls check_in_list method with specified `parent` parameter (Accs instance).
        :param name:
        name of the account
        """
        self.check_in_list(name, self.accs)

    def checkAccNotInList(self, name):
        """
        This method is used to check whether given account is NOT in the account list.
        It calls check_not_in_list method with specified `parent` parameter (Accs instance).
        :param name:
        name of the account
        """
        self.check_not_in_list(name, self.accs)


class SetupMixin:
    """
    This mixin is provides some helpful methods that are about setup.py module (i.e. installation
    wizard).
    """
    def patchReqs(self, to_install=[], cant_install=[]):
        """
        This method is used to monkeypatch Reqs class from setup.py module. Reqs is class that
        represents dependencies that are installed or not installed.
        :param to_install:
        fake list of pip dependencies that we need to install
        :param cant_install:
        fake list of system dependencies that are not installed
        """
        # here we create fake reqs instance
        reqs = Mock()
        reqs.installed = ['git', 'pip3', 'xclip',
                          'setuptools', 'cryptography', 'gitpython', 'pyshortcuts']
        reqs.to_install = to_install
        reqs.cant_install = cant_install

        for req in cant_install + to_install:
            reqs.installed.remove(req)

        self.monkeypatch.setattr('setup.Reqs', lambda: reqs)

    @staticmethod
    def mock_system(res):
        def wrap(command):
            time.sleep(0.1)
            # req = command.replace('pip3 install ', '')
            # self.to_install.remove(req)
            # self.patchReqs(self.to_install)
            return res

        return wrap


def init_accounts_folder():
    os.environ['HOME'] = '/home/accounts'
    if os.path.exists('/dev/shm/accounts'):
        shutil.rmtree('/dev/shm/accounts')
    os.mkdir('/dev/shm/accounts')


def init_src_folder(monkeypatch):
    init_accounts_folder()
    os.makedirs('/home/accounts/test/src')
    monkeypatch.setattr('core.const.SRC_DIR', '/home/accounts/test/src')
    monkeypatch.setattr('core.const.SRC_PATH', '/home/accounts/test')


class SettingsMixin:
    def setUp(self):
        os.environ['TESTING'] = 'True'
        os.mkdir('/home/accounts/.config')
        self.settings = QSettings(f'{os.getenv("HOME")}/PyTools', 'PyQtAccounts')
