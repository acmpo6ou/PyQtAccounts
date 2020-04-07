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
from PyQt5.QtCore import *
from unittest.mock import Mock
import pytest
import os
import git

from tests.base import UnitTest
from core.const import *
from core.updates import *


class UpdatingTest(UnitTest):
    def setUp(self):
        super().setUp()
        self.monkeypatch.setattr('core.updates.getChangeLog', lambda: ['Some changelog'])

    @staticmethod
    def mock_iter_commits(revision):
        yield 'Some commits'

    @staticmethod
    def mock_iter_no_commits(revision):
        return
        yield

    def test_there_are_commits(self):
        mock_Repo = Mock()
        mock_Repo.iter_commits = self.mock_iter_commits
        self.monkeypatch.setattr('git.Repo', lambda *args: mock_Repo)

        def check_result(changes, log):
            assert changes
            assert log == ['Some changelog']

        updating = Updating()
        updating.result.connect(check_result)
        updating.run()

    def test_there_are_no_commits(self):
        self.monkeypatch.setattr('core.updates.getChangeLog', lambda: ['Some changelog'])

        mock_Repo = Mock()
        mock_Repo.iter_commits = self.mock_iter_no_commits
        self.monkeypatch.setattr('git.Repo', lambda *args: mock_Repo)
        print(list(mock_Repo.iter_commits('')))

        def check_result(changes, log):
            assert not changes
            assert log == ['Some changelog']

        updating = Updating()
        updating.result.connect(check_result)
        updating.run()
