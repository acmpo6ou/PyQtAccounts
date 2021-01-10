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

from tests.base import UnitTest, SetupMixin
from setup import *
import setup


class TestPipInstall(UnitTest, SetupMixin):
    """
    This test tests PiPInstall process.
    """
    def check_result(self, res, req):
        """
        This method is a signal handler for PipInstall process.
        :param res:
        code result of installation
        :param req:
        name of requirement that we tried to install
        """
        # here we check that result is a zero code and here we append requirement to reqs list
        # for further check on correctness
        self.assertFalse(res)
        self.reqs.append(req)

    def test_pip_install(self):
        """
        This test tests PipInstall process.
        """
        # this is a list where we will collect names of requirements that we will try to install
        self.reqs = []

        # here we patch os.system function which will always return zero status code simulation
        # that there is no errors occur during installation process
        self.monkeypatch.setattr('os.system', lambda command: False)

        # and here we patch Reqs class with patchReqs method from SetupMixin, so it will simulate
        # that gitpython and cryptography aren't installed
        self.patchReqs(['gitpython', 'cryptography'])

        # then we create PipInstall process, connect it signals to appropriate signal handlers
        # and start it
        install = setup.PipInstall(setup.Reqs())
        install.result.connect(self.check_result)
        install.run()

        # finally we check that reqs that process emitted are those that it tried to install
        self.assertEqual(self.reqs, ['gitpython', 'cryptography'],
                         'Requirements that PipInstall process emitted and those that it tried to '
                         'install differ!')
