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
import unittest
import pytest
import os
import setup

from tests.base import UnitTest
from setup import *


class ReqsTest(UnitTest):
    """
    This class provides all unit tests for Reqs class.
    """
    def test_all_reqs_installed(self):
        """
        This test tests Reqs when all requirements are satisfied.
        """
        reqs = Reqs()
        all_req = set(reqs_pip + reqs_list)
        self.assertFalse(all_req - set(reqs.installed))

    def test_pip_reqs_not_installed(self):
        """
        This test tests Reqs when some pip requirements are not satisfied.
        """
        # these requirements aren't installed
        to_install = ['setuptools', 'cryptography']

        def mock_testing(req):
            """
            This function is a fake for our testing function from setup.py that called by Reqs
            when it tries to check what requirements are satisfied and what are not,
            it uses __import__ function but we don't mock it because it can cause strange errors
            as __import__ function is widely used by other python modules.
            :param req:
            name of requirement we want to check
            """
            # here we check if requirement is in the list of requirements that are not
            # satisfied (created above) if yes, then we raise ImportError to simulate that this
            # requirements is not satisfied
            if req in to_install:
                raise ImportError

        # here we patch `testing` function
        self.monkeypatch.setattr('setup.testing', mock_testing)

        # and here we create Reqs instance and check its lists on correctness
        reqs = Reqs()
        self.assertEqual(reqs.to_install, to_install,
                         'to_install list of Reqs is incorrect, must contain `setuptools` and '
                         '`cryptography`!')
        self.assertNotIn('setuptools', reqs.installed,
                         'installed list of Reqs is incorrect, must not contain `setuptools`!')
        self.assertNotIn('cryptography', reqs.installed,
                         'installed list of Reqs is incorrect, must not contain `cryptography`!')

    def test_sys_req_not_installed(self):
        """
        This test tests Reqs when some system reqs are not installed.
        """
        # these requirements aren't installed
        cant_install = ['git', 'xclip']

        def mock_system(command):
            """
            This function is a test double of os.system, we use it to simulate that some
            requirements are not satisfied.
            :param command:
            command that we use to check whether system requirements is satisfied or not.
            Here is the commend form:
            which <requirement name>
            """
            # here we extract requirement name from command by deleting `which ` part:
            req = command.replace('which ', '')

            # here we check if requirement is in the list of requirements that are not
            # satisfied (created above) if yes, then we return nonzero code to simulate that
            # this requirement is not satisfied
            if req in cant_install:
                return True
            else:
                # every other requirement is satisfied so we return zero exit code
                return False

        # here we patch `os.system` function
        self.monkeypatch.setattr('os.system', mock_system)

        # and here we create Reqs instance and check its lists on correctness
        reqs = Reqs()
        self.assertEqual(reqs.cant_install, cant_install,
                         'to_install list of Reqs is incorrect, must contain `git` and '
                         '`xclip`!')
        self.assertNotIn('git', reqs.installed,
                         'installed list of Reqs is incorrect, must not contain `git`!')
        self.assertNotIn('xclip', reqs.installed,
                         'installed list of Reqs is incorrect, must not contain `xclip`!')
