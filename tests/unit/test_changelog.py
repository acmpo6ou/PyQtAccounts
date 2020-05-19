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

"""
This test module contains all unit tests for ShowChangelog dialog of PyQtAccounts.
"""

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
import unittest
import pytest
import os

from tests.base import UnitTest
from core.utils import *
from PyQtAccounts import *


class ChangelogTest(UnitTest):
    """
    This test class contains all unit tests for ShowChangelog dialog of PyQtAccounts.
    """
    def test_changelog(self):
        """
        This test tests whether text changelog in ShowChangelog dialog is constructed correctly.
        """
        def mock_open(*args):
            """
            This is a test double for `open` built in function, we use it to create fake changelog
            file that ShowChangelog dialog uses.
            """
            return ['Fixed issues.', 'Changelog tested now.', 'Other updates.']

        # here we pre-saving and mocking `open` function, also we patch version to check does
        # ShowChangelog dialog shows it correctly too.
        normal_open = __builtins__['open']
        __builtins__['open'] = mock_open
        self.patchVersion()

        # then we create ShowChangelog instance and check its changelog label content.
        log = ShowChangelog(None)
        right_text = '<h4>PyQtAccounts v2.0.6:</h4><ul><li>Fixed issues.</li>\n' \
                     '<li>Changelog tested now.</li>\n' \
                     '<li>Other updates.</li>\n' \
                     '</ul>'
        self.assertEqual(right_text, log.changelogLabel.text(),
                         'Changelog label in ShowChangelog dialog is incorrect!')

        # clean up
        # here we restore pre-saved `open` function
        __builtins__['open'] = normal_open
