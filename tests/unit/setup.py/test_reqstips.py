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
from unittest.mock import Mock
import pytest
import os

from tests.base import UnitTest
from setup import *


class ReqsTipsTest(UnitTest):
    def test_tips_cant_install(self):
        reqs = Mock()
        reqs.cant_install = ('git', 'pip3', 'xclip')
        reqs.to_install = ()
        tips = ReqsTips(reqs)
        expect_text = (
            'Будь-ласка встановіть пакети git pip3 xclip самостійно. \n'
            'Для їх встановлення потрібні права адміністратора. \n'
            'Введіть в терміналі таку команду: \n'
            'sudo apt install git pip3 xclip')
        self.assertEqual(tips.toPlainText(), expect_text)
