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

"""
This test module contains all unit tests for `about` dialog of PyQtAccounts.
"""

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
from unittest.mock import Mock
import pytest
import sys

from tests.base import UnitTest
from core.utils import *
from PyQtAccounts import *
from core.windows import About
import git


class AboutTest(UnitTest):
    """
    This class contains all unit tests for `about` dialog of PyQtAccounts.
    """
    def setUp(self):
        """
        In this method we simply pre-saving built in open function, because we will replace it
        with ours during tests.
        """
        super().setUp()
        self.open = open

    def tearDown(self):
        """
        In this method we restore built in open function from our `open` attribute where we
        pre-save it.
        """
        super().tearDown()
        __builtins__['open'] = self.open

    def test_about_version(self):
        """
        This method tests does version displays right in about section.
        """
        # Tom has PyQtAccounts v2.0.6 installed
        self.patchVersion()

        # he opens about dialog and sees correct version number `Version 2.0.6` in about section
        about = About()
        self.assertIn('Version 2.0.6', about.about, 'Version number in about dialog is incorrect!')

    def test_license_credits(self):
        """
        This method tests does license and credits loads correctly from their files.
        :return:
        """
        def mock_open(path, *args, **kwargs):
            """
            This function is a test double for open built in function.
            :param path:
            path to file we want to open
            :return:
            fake file descriptor if function was called by PyQtAccounts about dialog else real
            file descriptor (using our pre-saved open function)
            """
            # here we check whether function was called by PyQtAccounts about dialog or not
            file = Mock()
            # if it was we check what file does about dialog wants to load LICENSE or CREDITS and
            # return him appropriate fake file descriptor
            if path == 'COPYING':
                file.read.return_value = 'This is a License.'
            elif path == 'CREDITS':
                file.read.return_value = 'Here are credits.'
            else:
                # if function was called by another code (i.e. not about dialogs) we return real
                # file descriptor
                file = self.open(path, *args, **kwargs)
            return file

        # here we patch open function with our fake one and create about dialog
        __builtins__['open'] = mock_open
        about = About()

        # then we check license and credits sections of about dialog
        self.assertEqual(about.licenseText.toPlainText(), 'This is a License.',
                         'License text is incorrectly loaded!')
        self.assertEqual(about.creditsText.text(), '<pre>Here are credits.</pre>',
                         'Credits text is incorrectly loaded!')
