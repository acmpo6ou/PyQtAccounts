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
import sys

sys.path.append('.')

from tests.base import UnitTest
from core.utils import *
from PyQtAccounts import *
from core.windows import About
import git


class AboutTest(UnitTest):
    def setUp(self):
        super().setUp()
        self.open = open

    def tearDown(self):
        __builtins__['open'] = self.open

    def test_about_version(self):
        self.patchVersion()
        about = About()
        self.assertIn('Version 2.0.6', about.about)

    def test_license_credits(self):
        def mock_open(path, *args, **kwargs):
            file = Mock()
            if path == 'COPYING':
                file.read.return_value = 'This is a License.'
            elif path == 'CREDITS':
                file.read.return_value = 'Here are credits.'
            else:
                file = self.open(path, *args, **kwargs)
            return file
        __builtins__['open'] = mock_open
        about = About()

        self.assertEqual(about.licenseText.toPlainText(), 'This is a License.')
        self.assertEqual(about.creditsText.text(), '<pre>Here are credits.</pre>')
