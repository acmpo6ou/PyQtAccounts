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

from PyQt5.QtWidgets import *
import unittest
from unittest.mock import Mock
import pytest
import sys
import os

sys.path.append('.')

from PyQtAccounts import *


class BaseTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def monkeypatching(self, monkeypatch):
        self.monkeypatch = monkeypatch

    def file_dialog(self, result):
        def file_dialog(caption, filter, directory):
                assert caption == 'Імпортувати базу данних'
                assert filter == 'Tarball (*.tar)'
                assert directory == os.getenv('HOME')
                return result
        return file_dialog

    def save_file_dialog(self, name, result):
        def save_file_dialog(caption, filter, directory):
                home = os.getenv('HOME')
                assert caption == 'Експортувати базу данних'
                assert filter == 'Tarball (*.tar)'
                assert directory == f'{home}/{name}.tar'
                return result
        return save_file_dialog

    def mess(self, head, text, button=QMessageBox.Ok):
        def mess(parent, this_head, this_text, *args, **kwargs):
                assert this_head == head
                assert this_text == text
                return button
        return mess

    def critical(self, parent, head, text):
        assert head == 'Помилка!'
        return QMessageBox.Ok


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
        self.window = Window()
        self.dbs = self.window.dbs

    def tearDown(self):
        self.window.destroy = True
        self.window.close()

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

class DbsTest(FuncTest):
    def setUp(self):
        super().setUp()

    def checkOnlyVisible(self, elem):
        self.check_only_visible(elem, self.dbs)

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

class AccsTest(FuncTest):
    def setUp(self):
        super().setUp()
        form = self.dbs.forms['open']
        self.list = self.dbs.list
        self.pass_input = form.passField.passInput
        self.list.selected(Index('database'))
        self.pass_input.setText('some_password')
        form.openButton.click()
        self.win = self.window.windows[1]
        self.accs = self.win.accs
        self.splt = self.win.splt

    def checkOnlyVisible(self, elem):
        self.check_only_visible(elem, self.splt)
