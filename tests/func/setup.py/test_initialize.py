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

import pyfakefs.fake_filesystem_unittest as fs_unit
from unittest.mock import Mock
import pytest
import os
import io

from tests.base import SetupFuncTest
from setup import *
import git

fs_unit.Patcher.SKIPMODULES = [io, os, git]
HOME_DIR = '/home/accounts'


class Test(SetupFuncTest):
    def check_progress(self, progress):
        self.progress.append(progress)

    def check_result(self, res):
        self.assertFalse(res)
        self.assertTrue(os.path.exists(f'{HOME_DIR}/PyQtAccounts/src'))
        self.assertTrue(os.path.exists(f'{HOME_DIR}/PyQtAccounts/core'))
        self.assertTrue(os.path.exists(f'{HOME_DIR}/PyQtAccounts/run.sh'))
        self.assertTrue(os.path.exists(f'{HOME_DIR}/PyQtAccounts/change.log'))
        self.assertTrue(os.path.exists(f'{HOME_DIR}/PyQtAccounts/PyQtAccounts.py'))
        self.assertTrue(os.path.exists(f'{HOME_DIR}/PyQtAccounts/README.md'))
        self.assertTrue(os.path.exists(f'{HOME_DIR}/PyQtAccounts/CREDITS'))
        self.assertTrue(os.path.exists(f'{HOME_DIR}/PyQtAccounts/COPYING'))

    def test_initialize_no_errors(self):
        self.progress = []
        self.monkeypatch.setenv('HOME', HOME_DIR)

        with fs_unit.Patcher(additional_skip_names=[io, os, git]) as p:
            p.fs.create_dir(HOME_DIR)
            init = Initialize(HOME_DIR)
            init.progress.connect(self.check_progress)
            init.result.connect(self.check_result)
            init.run()
