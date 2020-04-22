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

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from unittest.mock import Mock
import pytest
import os

from tests.base import UnitTest
from setup import *
import git


class InitializeTest(UnitTest):
    def check_progress(self, progress):
        self.progress.append(progress)

    def check_result(self, res):
        self.res = res

    def test_initialize_no_errors(self):
        self.progress = []

        def mock_clone(path, folder, progress):
            self.assertEqual(path, 'https://github.com/Acmpo6ou/PyQtAccounts')
            self.assertEqual(folder, '/home/accounts/PyQtAccounts')

            progress.update(None, 0, 120)
            progress.update(None, 30, 120)
            progress.update(None, 60, 120)
            progress.update(None, 90, 120)
            progress.update(None, 120, 120)

        self.monkeypatch.setattr('git.Repo.clone_from', mock_clone)

        init = Initialize('/home/accounts')
        init.progress.connect(self.check_progress)
        init.result.connect(self.check_result)
        init.run()

        self.assertEqual(self.res, 0)
        self.assertEqual(self.progress, [0, 25, 50, 75, 100])

    def test_initialize_errors(self):
        def mock_clone(path, folder, progress):
            raise Exception('Error!')

        self.monkeypatch.setattr('git.Repo.clone_from', mock_clone)

        init = Initialize('/home/accounts')
        init.progress.connect(self.check_progress)
        init.result.connect(self.check_result)
        init.run()

        self.assertEqual(self.res, 1)
