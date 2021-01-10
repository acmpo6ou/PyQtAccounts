#!/usr/bin/env python3

#  Copyright (c) 2020-2021. Kolvakh Bohdan
#  This file is part of PyQtAccounts.
#
#  PyQtAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyQtAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.

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
    """
    This class provides all unit tests for Initialize class.
    """
    def check_progress(self, progress):
        """
        This function is a signal handler for Initialize process.
        :param progress:
        progress in % of Initialize process.
        """
        # here we just save received progress in list for further check on correctness
        self.progress.append(progress)

    def check_result(self, res):
        """
        This method is another signal handler for Initialize process.
        :param res:
        result of the process
        """
        # here we simply save result for further check on correctness
        self.res = res

    def test_initialize_no_errors(self):
        """
        This test tests process behavior when there are no errors during initialization.
        """
        # here we will save our progress received by check_progress method
        self.progress = []

        def mock_clone(path, folder, progress):
            """
            This function is a test double of clone_from method from Repo class.
            It will simulate cloning progress and will check some parameters that are passed to it.
            :param path:
            path of PyQtAccounts github repository.
            :param folder:
            path to folder where we will clone programs repository
            :param progress:
            signal which we will emit to send progress of cloning
            """
            # here we check some parameters
            self.assertEqual(path, 'https://github.com/Acmpo6ou/PyQtAccounts',
                             'Path to PyQtAccounts repository is incorrect!')
            self.assertEqual(folder, '/home/accounts/PyQtAccounts',
                             'Path to installation folder is incorrect!')

            # here we simulate progress by emitting a series of progress signals with increasing
            # progress values
            progress.update(None, 0, 120)
            progress.update(None, 30, 120)
            progress.update(None, 60, 120)
            progress.update(None, 90, 120)
            progress.update(None, 120, 120)

        # and here we patch clone_from method of Repo with our mock_clone function
        self.monkeypatch.setattr('git.Repo.clone_from', mock_clone)

        # then we create Initialize process, connect it signals to appropriate signal handlers
        # and start process
        init = Initialize('/home/accounts')
        init.progress.connect(self.check_progress)
        init.result.connect(self.check_result)
        init.run()

        # finally we check results
        self.assertEqual(self.res, 0, 'Initialization process emitted nonzero result but it should'
                                      'be zero!')
        self.assertEqual(self.progress, [0, 25, 50, 75, 100], 'Progress of clone is incorrect!')

    def test_initialize_errors(self):
        """
        This test tests process behavior when there are errors during initialization.
        """
        def mock_clone(path, folder, progress):
            """
            This function is a test double of clone_from method from Repo class.
            It simply raises an error simulating errors during initialization procces.
            :param path:
            path of PyQtAccounts github repository.
            :param folder:
            path to folder where we will clone programs repository
            :param progress:
            signal which we will emit to send progress of cloning
            """
            raise Exception('Error!')

        # here we monkeypatch clone_from method of Repo class
        self.monkeypatch.setattr('git.Repo.clone_from', mock_clone)

        # then we create Initialize process, connect it signals to appropriate signal handlers
        # and start process
        init = Initialize('/home/accounts')
        init.progress.connect(self.check_progress)
        init.result.connect(self.check_result)
        init.run()

        # finally we check that process has emitted nonzero result
        self.assertEqual(self.res, 1, 'Initialization process emitted zero result but it should'
                                      'emit a nonzero one since there are errors occur during the '
                                      'process.')
