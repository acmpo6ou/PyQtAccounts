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

import unittest

class RunShTest(unittest.TestCase):
    '''
    We don't want to accidentally push run.sh with incorrect paths.
    '''
    def setUp(self):
        self.file = open('run.sh').read()

    def test_run_sh_path(self):
        self.assertIn('cd .', self.file)

    def test_run_sh_pythonpath(self):
        self.assertIn('export PYTHONPATH="$PYTHONPATH:./"', self.file)