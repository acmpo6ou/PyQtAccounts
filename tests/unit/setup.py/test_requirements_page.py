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


class RequirementsPageTest(UnitTest):
    def setUp(self):
        super().setUp()
        self.page = RequirementsPage()

    def test_requirements_page(self):
        # There is title that says `requirements`
        title = self.page.title.text()
        expected_title = '<h4>Залежності</h4>'
        self.assertEqual(title, expected_title)

        # There is also text that describes requirements
        text = self.page.text.text()
        expected_text = ('<pre>PyQtAccounts вимагає наявності\n'
                         'певних пакетів. Ось перелік тих які\n'
                         'встановлені, або не встановленні у вас:</pre>')
        self.assertEqual(text, expected_text)

        # There is no installation label and progressbar
        self.assertFalse(self.page.installLabel.visibility)
        self.assertFalse(self.page.installProgress.visibility)

    def test_install_button_enabled(self):
        # When every pip dependency is satisfied install button is disabled
        self.assertFalse(self.page.installButton.isEnabled())

        # When some are not installed install button is enabled
        reqs = Mock()
        reqs.to_install = ('gitpython', 'pyshortcuts')
        reqs.installed = ('some', 'packages')
        reqs.cant_install = ('some', 'packages')
        self.monkeypatch.setattr('setup.Reqs', lambda: reqs)

        page = RequirementsPage()
        self.assertTrue(page.installButton.isEnabled())
