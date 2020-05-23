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
    """
    This test class provides all unit tests for updating.
    """
    def setUp(self):
        """
        Here we simulate changelog by monkeypatching `getChangelog` function,
        which provides changelog.
        """
        super().setUp()
        self.monkeypatch.setattr('core.updates.getChangeLog',
                                 lambda: ['Some changelog'])

    @staticmethod
    def mock_iter_commits(revision):
        """
        This is a test double of `iter_commits` method for Repo class.
        It simulates existance of commits, which is a signal for program that
        there are updates available, also this method is a generator.
        :param revision:
        parameter that we pass to iter_commits method, it represents revision
        """
        yield 'Some commits'

    @staticmethod
    def mock_iter_no_commits(revision):
        """
        This is a test double of `iter_commits` method for Repo class.
        It simulates INEXISTANCE of commits, which is a signal for program that
        there is no updates available, also this method is a generator.
        :param revision:
        parameter that we pass to iter_commits method, it represents revision
        """
        # we return once function is called, so it will generate an empty list
        # of commints
        return
        # we need yield to make this function generator
        yield

    def test_there_are_commits(self):
        """
        This test tests programs behavior when trere are new commits in programs
        github repository. In short it tests appearence of UpdatesAcailable
        dialog when there are new commits (i.e. there are updates).
        """
        # here we create fake of Repo class with fake iter_commits method which
        # will generate list of new commits.
        mock_Repo = Mock()
        mock_Repo.iter_commits = self.mock_iter_commits
        self.monkeypatch.setattr('git.Repo', lambda *args: mock_Repo)

        def check_result(changes, log):
            """
            This function will check cnagelog and `changes` variable that are
            emited by Updating process (which checks for updates).
            :param changes:
            represents are there updates available
            :param log:
            represents changlog which is obtained by Updating process using
            getChangelog function (which we monkeypatched).
            """
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
