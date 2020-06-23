#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh Bogdan
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
import glob

from tests.base import AccsTest
import core.utils
from core.const import *
from PyQtAccounts import *


class HelpTipTest(AccsTest):
    """
    This class provides all functional tests for accounts HelpTip.
    """
    def test_no_accs(self):
        """
        This test tests HelpTip when there is no accounts yet.
        """
        # Ross opens his database, he has no accounts yet
        super().setUp('a', 'a')

        # There is help tip saying how he can create new account
        tip = self.win.accs.tips['help']
        self.assertEqual(
            tip.text(), HELP_TIP_ACCS,
            'Accounts help tip message when there are no'
            'accounts is incorrect!')

    def test_has_accs(self):
        """
        This test tests HelpTip when there are accounts.
        """
        # Emily opens up PyQtAccounts, she has some databases
        super().setUp()

        # There is help tip saying that she need to chose account
        tip = self.accs.tips['help']
        self.assertEqual(
            tip.text(), "Виберіть акаунт",
            'Accounts help tip message when there are '
            'accounts is incorrect!')
