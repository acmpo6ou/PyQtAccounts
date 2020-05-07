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
        submenu = self.window.menuBar().actions()[submenu_index]
        return submenu.menu().actions()[action_index]

    @staticmethod
    def file_dialog(result):
        def file_dialog(caption, filter, directory):
            assert caption == 'Імпортувати базу данних'
            assert filter == 'Tarball (*.tar)'
            assert directory == os.getenv('HOME')
            return result

        return file_dialog

    @staticmethod
    def save_file_dialog(name, result):
        def save_file_dialog(caption, filter, directory):
            home = os.getenv('HOME')
            assert caption == 'Експортувати базу данних'
            assert filter == 'Tarball (*.tar)'
            assert directory == f'{home}/{name}.tar'
            return result

        return save_file_dialog

    @staticmethod
    def mess(head, text, button=QMessageBox.Ok):
        def mess(parent, this_head, this_text, *args, **kwargs):
            assert this_head == head
            assert this_text == text
            return button

        return mess

    @staticmethod
    def mess_showed(*args, **kwargs):
        raise AssertionError('This message showed, but shouldn\'t be!')

    @staticmethod
    def critical(parent, head, text):
        assert head == 'Помилка!'
        return QMessageBox.Ok

    @staticmethod
    def copyDatabase(name):
        shutil.copy(f'tests/src/{name}.db', '/home/accounts/test/src')
        shutil.copy(f'tests/src/{name}.bin', '/home/accounts/test/src')


class UnitTest(BaseTest):
    def patchVersion(self):
        class Tag:
            def __init__(self, name, date):
                self.name = name
                self.commit = Mock()
                self.commit.committed_datetime = date

            def __str__(self):
                return self.name

        class Repo:
            def __init__(self, *args):
                pass

            tags = []
            for i, name in enumerate(['v1.0.0', 'v1.0.2', 'v2.0.6']):
                tags.append(Tag(name, i))

        self.monkeypatch.setattr(git, 'Repo', Repo)


class FuncTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.window = Window()
        self.dbs = self.window.dbs

        init_accounts_folder()
        init_src_folder(self.monkeypatch)
        self.copyDatabase('main')
        self.copyDatabase('crypt')
        self.copyDatabase('a')
        self.copyDatabase('database')
        self.copyDatabase('import_database')

    def tearDown(self):
        try:
            self.window.destroy = True
            self.window.close()
        except AttributeError:
            pass

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

    def check_in_list(self, name, parent):
        model = parent.list.model
        for i in range(model.rowCount()):
            index = model.item(i)
            if index.text() == name:
                break
        else:
            raise AssertionError('Not in the list!')

    def check_not_in_list(self, name):
        try:
            self.checkDbInList(name)
        except RecursionError:  # to prevent fatal python error
            raise
        except:
            pass
        else:
            raise AssertionError("In the list, but it shouldn't be!")


class DbsTest(FuncTest):
    def checkOnlyVisible(self, elem):
        self.check_only_visible(elem, self.dbs)

    def checkDbInList(self, name):
        self.check_in_list(name, self.dbs)

    def checkDbNotInList(self, name):
        self.check_not_in_list(name)

    def checkDbOnDisk(self, name):
        self.assertTrue(os.path.exists(f'/home/accounts/test/src/{name}.bin'))
        self.assertTrue(os.path.exists(f'/home/accounts/test/src/{name}.db'))

    def checkDbNotOnDisk(self, name):
        self.assertFalse(os.path.exists(f'/home/accounts/test/src/{name}.bin'))
        self.assertFalse(os.path.exists(f'/home/accounts/test/src/{name}.db'))


class AccsTest(FuncTest):
    def setUp(self, name='database', password='some_password'):
        super().setUp()

        init_accounts_folder()
        init_src_folder(self.monkeypatch)
        self.copyDatabase(name)

        form = self.dbs.forms['open']
        self.list = self.dbs.list
        self.pass_input = form.passField.passInput
        self.list.selected(Index(name))
        self.pass_input.setText(password)
        form.openButton.click()
        self.win = self.window.windows[1]
        self.accs = self.win.accs

    def checkOnlyVisible(self, elem):
        self.check_only_visible(elem, self.accs)

    def checkAccInList(self, name):
        self.check_in_list(name, self.accs)

    def checkAccNotInList(self, name):
        self.check_not_in_list(name)


class SetupMixin:
    def patchReqs(self, to_install=[], cant_install=[]):
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
