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
from PyQt5.QtCore import *
from unittest.mock import Mock
import pytest
import os

from tests.base import FuncTest
from core.utils import *
from core.updates import *
import core.updates
from PyQtAccounts import *


class Test(FuncTest):
    def setUp(self):
        super().setUp()
        updates = self.window.menuBar().actions()[2]  # third is `Updates` submenu
        self.check = updates.menu().actions()[0]

    def test_check_for_updates_unavailable(self):
        # Lea wants to check for updates, so she goes to menu: Updates -> Check for updates
        # The message appears saying that there is no updates available
        def mock_run(self):
            self.result.emit(False, [])
        self.monkeypatch.setattr(Updating, 'run', mock_run)
        self.monkeypatch.setattr(QMessageBox, 'information',
                                 self.mess('Оновлення', "Немає оновленнь."))
        self.check.trigger()

    def test_check_for_updates_available(self):
        # Emily wants to check for updates
        def mock_run(self):
            self.result.emit(True, ['Fixed issues.', 'Changelog tested now.', 'Other updates.'])
        self.monkeypatch.setattr(Updating, 'run', mock_run)

        # Dialog window appears saying that there are updates available
        self.check.trigger()
        QTest.qWait(100)
        try:
            # We don't actually want to update anything during the tests
            self.window.res.laterButton.click()
        except AttributeError:
            assert AssertionError('No update available window was created!')

        # There is changelog in that dialog
        right_text = '<h4>Що нового:</h4><ul><li>Fixed issues.</li>\n' \
                     '<li>Changelog tested now.</li>\n' \
                     '<li>Other updates.</li>\n' \
                     '</ul>'
        self.assertEqual(right_text, self.window.res.changelogLabel.text())
