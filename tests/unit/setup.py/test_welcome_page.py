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

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import unittest
import pytest
import os

from tests.base import UnitTest
from setup import *


class WelcomePageTest(UnitTest):
    """
    This test class provides all unit tests for WelcomePage.
    """
    def test_welcome_page(self):
        """
        This test tests content of WelcomePage.
        """
        page = WelcomePage()
        # There is an icon at the welcome page
        icon = page.pixmap(QWizard.WatermarkPixmap).toImage()
        expected_icon = QImage(
            '/usr/share/icons/Mint-X/mimetypes/96/application-pgp-keys.svg')
        self.assertEqual(icon, expected_icon,
                         'Image on WelcomePage is incorrect!')

        # And title that welcomes you
        title = page.title.text()
        expected_title = '<h4><pre>Вітаємо у майстрі встановлення\n PyQtAccounts!</pre></h4>'
        self.assertEqual(title, expected_title,
                         'Title on WelcomePage is incorrect!')

        # There is also text that describes installation wizard
        text = page.text.text()
        expected_text = '<pre><br>Ми допоможемо вам пройти всі кроки \nвстановлення.</pre>'
        self.assertEqual(text, expected_text,
                         'Message on WelcomePage is incorrect!')
