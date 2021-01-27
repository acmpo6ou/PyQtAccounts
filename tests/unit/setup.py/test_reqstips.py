#!/usr/bin/env python3

#  Copyright (c) 2020-2021. Bohdan Kolvakh
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

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from unittest.mock import Mock
import pytest
import os

from tests.base import UnitTest
from setup import *


class ReqsTipsTest(UnitTest):
    """
    This test provides all unit tests for ReqsTips.
    """
    def test_all_installed(self):
        """
        Here we test content of tips when every requirement is satisfied.
        """
        # here we create fake Reqs instance that will simulate that all requirements are satisfied
        reqs = Mock()
        reqs.cant_install = ()
        reqs.to_install = ()

        # and here we create ReqsTips instance using fake reqs and then we check tips message
        tips = ReqsTips(reqs)
        expect_text = 'Всі залежності встановленно!'
        self.assertEqual(tips.toPlainText(), expect_text,
                         'ReqsTips message is incorrect, must be successful!')

    def test_tips_cant_install(self):
        """
        This test tests ReqsTips behavior when some system requirements are not satisfied.
        """
        # here we create fake Reqs instance that will simulate that some system requirements aren't
        # satisfied
        reqs = Mock()
        reqs.cant_install = ('git', 'pip3', 'xclip')
        reqs.to_install = ()

        # then we create ReqsTips and check its message
        tips = ReqsTips(reqs)
        expect_text = (
            'Будь-ласка встановіть пакети git pip3 xclip самостійно. \n'
            'Для їх встановлення потрібні права адміністратора. \n'
            'Введіть в терміналі таку команду: \n'
            'sudo apt install git pip3 xclip')
        self.assertEqual(tips.toPlainText(), expect_text,
                         'ReqsTips message is incorrect, must contain advise about unsatisfied '
                         'system requirements!')

    def test_tips_to_install(self):
        """
        This test tests ReqsTips behavior when some pip requirements are not satisfied.
        """
        # here we create fake Reqs instance that will simulate that some pip requirements aren't
        # satisfied
        reqs = Mock()
        reqs.cant_install = ()
        reqs.to_install = ('gitpython', 'cryptography', 'pyshortcuts')

        # then we create ReqsTips and check its message
        tips = ReqsTips(reqs)
        expect_text = ('Пакети gitpython, cryptography, pyshortcuts ми можемо встановити для вас,'
                       ' для цього натисніть кнопку "Встановити". \n'
                       'Але спершу не забудьте перевірити наявність пакету pip3!')
        self.assertEqual(tips.toPlainText(), expect_text,
                         'ReqsTips message is incorrect, must contain advise about unsatisfied '
                         'pip requirements!')

    def test_tips_to_install_and_cant_install(self):
        """
        This test tests ReqsTips behavior when both system and pip requirements are not satisfied.
        """
        # here we create fake Reqs instance that will simulate that both system and pip
        # requirements aren't satisfied
        reqs = Mock()
        reqs.cant_install = ('git', 'pip3', 'xclip')
        reqs.to_install = ('gitpython', 'cryptography', 'pyshortcuts')

        # and here we create ReqsTips and check its message
        tips = ReqsTips(reqs)
        expect_text = ('Будь-ласка встановіть пакети git pip3 xclip самостійно. \n'
                       'Для їх встановлення потрібні права адміністратора. \n'
                       'Введіть в терміналі таку команду: \n'
                       'sudo apt install git pip3 xclip\n'
                       'Пакети gitpython, cryptography, pyshortcuts ми можемо встановити для вас, '
                       'для цього натисніть кнопку "Встановити". \n'
                       'Але спершу не забудьте перевірити наявність пакету pip3!')
        self.assertEqual(tips.toPlainText(), expect_text,
                         'ReqsTips message is incorrect, must contain advise about unsatisfied '
                         'pip and system requirements!')
