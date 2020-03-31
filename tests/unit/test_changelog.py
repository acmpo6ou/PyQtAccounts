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
import unittest
import pytest
import os

from tests.base import UnitTest
from core.utils import *
from PyQtAccounts import *


class Test(UnitTest):
    def setUp(self):
        super().setUp()

    def test_changelog(self):
        def mock_open(*args):
            return ['Fixed issues.', 'Changelog tested now.', 'Other updates.']
        normal_open = __builtins__['open']
        __builtins__['open'] = mock_open
        self.patchVersion()

        log = ShowChangelog(None)
        right_text = '<h4>PyQtAccounts v2.0.6:</h4><ul><li>Fixed issues.</li>\n' \
                     '<li>Changelog tested now.</li>\n' \
                     '<li>Other updates.</li>\n' \
                     '</ul>'
        print(log.changelogLabel.text())
        self.assertEqual(right_text, log.changelogLabel.text())

        # clean up
        __builtins__['open'] = normal_open
