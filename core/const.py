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
This module provides helper constants for PyQtAccounts.
"""

# This constants provide information about requirements
# either system (i.e. that we can install only with root privileges) or pip.
sys_reqs = ('git', 'pip3', 'xclip')
reqs_pip = ('setuptools', 'cryptography', 'gitpython', 'pyshortcuts')

# This constants provide information about folder that stores databases
# First constant provides name of folder
# Second provides path where the folder is
# Both constants were designed for testing
SRC_DIR = 'src'
SRC_PATH = '.'

# This constant stores information message that PyQtAccounts shows when you have no databases
# created yet.
HELP_TIP_DB = ("<pre>Поки що у вас немає жодної бази данних.\n" +
               '{0:<39}\n'.format("Спробуйте:") +
               '{0:<39}\n'.format("Натиснути +") +
               '{0:<39}\n'.format("Гарячі клавіші Ctl+N") +
               '{0:<39}\n'.format("Меню: File -> New database...") +
               "</pre>")

# This constant stores information message that PyQtAccounts shows when you have no accounts
# created yet.
HELP_TIP_ACCS = ("<pre>Поки що у вас немає жодного акаунта.\n" +
                          '{0:<36}\n'.format("Спробуйте:") +
                          '{0:<36}\n'.format("Натиснути +") +
                          '{0:<36}\n'.format("Гарячі клавіші Ctl+N") +
                          '{0:<36}\n'.format("Меню: File -> New account...") +
                          "</pre>")
