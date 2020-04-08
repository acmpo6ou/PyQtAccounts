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

from tests.base import UnitTest
from setup import *

real_replace = str.replace


class ReqsTest(UnitTest):
    def test_all_reqs_installed(self):
        reqs = Reqs()
        all_req = set(reqs_pip + reqs_list)
        self.assertFalse(all_req - set(reqs.installed))

    def test_sys_req_not_installed(self):
        def mock_system(sys_req):
            def wrap(command):
                req = command.replace('which ', '')
                assert req in reqs_list
                if req == sys_req:
                    return True
                else:
                    return False
            return wrap

        for req in reqs_list:
            self.monkeypatch.setattr('os.system', mock_system)
            reqs = Reqs()
            self.assertNotIn(req, reqs.installed)
            self.assertIn(req.replace('pip3', 'python3-pip'), reqs.cant_install)
