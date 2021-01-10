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

import unittest
import pytest
import os

from tests.base import UnitTest
from core.windows import _import


class ImportTest(UnitTest):
    """
    This class contains all unit tests about import.
    """
    def test_bin_and_db_files_in_tar(self):
        """
        This test tests whether _import function raises TypeError when we try
        to import corrupted database archive.
        """
        # When no .db and .bin files in tar
        self.assertRaises(TypeError, _import, 'src/corrupted_no_db_no_bin.tar')

        # When no .db file in tar
        self.assertRaises(TypeError, _import, 'src/corrupted_no_db.tar')

        # When no .bin file in tar
        self.assertRaises(TypeError, _import, 'src/corrupted_no_bin.tar')
