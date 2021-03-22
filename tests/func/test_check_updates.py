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
from PyQt5.QtCore import *
from unittest.mock import Mock
import pytest
import os

from tests.base import DbsTest
from core.utils import *
from core.updates import *
import core.updates
from PyQtAccounts import *


class CheckForUpdatesTest(DbsTest):
    """
    This class provides all tests that will test PyQtAccounts checking for
    updates.
    """

    def setUp(self):
        """
        Here we go to menu: Updates -> Check for updates at the begining of
        every test.
        """
        super().setUp()
        # third is `Updates` submenu, first is `Check for updates` action
        self.check = self.menu(2, 0)

    def test_check_for_updates_unavailable_menu(self):
        """
        This test tests updates checking when there are no updates available.
        """

        # Lea wants to check for updates, so she goes to menu: Updates -> Check for updates
        # The message appears saying that there is no updates available
        def mock_run(self):
            self.result.emit(False, [])

        self.monkeypatch.setattr(Updating, "run", mock_run)
        self.monkeypatch.setattr(
            QMessageBox, "information", self.mess("Оновлення", "Немає оновленнь.")
        )
        self.check.trigger()

    def test_check_for_updates_available_menu(self):
        """
        This test tests updates checking when there are updates available.
        """

        # Emily wants to check for updates
        def mock_run(self):
            self.result.emit(
                True, ["Fixed issues.", "Changelog tested now.", "Other updates."]
            )

        self.monkeypatch.setattr(Updating, "run", mock_run)

        # Dialog window appears saying that there are updates available
        self.check.trigger()

        # We don't actually want to update anything during the tests
        def window_show():
            assert self.window.res, "No update available window was created!"

        self.qbot.waitUntil(window_show)
        self.window.res.laterButton.click()

        # There is changelog in that dialog
        right_text = (
            "<h4>Що нового:</h4><ul><li>Fixed issues.</li>\n"
            "<li>Changelog tested now.</li>\n"
            "<li>Other updates.</li>\n"
            "</ul>"
        )
        self.assertEqual(
            right_text,
            self.window.res.changelogLabel.text(),
            "Changelog text of UpdatesAvailable window is incorrect!",
        )

    def test_check_for_updates_available_at_startup(self):
        """
        This test tests updates checking on startup and when there are updates
        available.
        """

        # There are some updates available
        def mock_run(self):
            self.result.emit(
                True, ["Fixed issues.", "Changelog tested now.", "Other updates."]
            )

        self.monkeypatch.setattr(Updating, "run", mock_run)

        # So Ross launches PyQtAccounts to check for them
        window = Window()

        # A few seconds passes and dialog appears saying that there are updates available
        QTest.qWait(200)
        self.assertIsNotNone(window.res, "No update available window was created!")
        # We don't actually want to update anything during the tests
        window.res.laterButton.click()

        # There is changelog in that dialog
        right_text = (
            "<h4>Що нового:</h4><ul><li>Fixed issues.</li>\n"
            "<li>Changelog tested now.</li>\n"
            "<li>Other updates.</li>\n"
            "</ul>"
        )
        self.assertEqual(
            right_text,
            window.res.changelogLabel.text(),
            "Changelog text of UpdatesAvailable window is incorrect!",
        )

    def test_check_for_updates_unavailable_at_startup(self):
        """
        This test tests updates checking on startup and when there is no updates
        available.
        """

        # Tom wants to check are there any updates available
        def mock_run(self):
            self.result.emit(False, [])

        self.monkeypatch.setattr(Updating, "run", mock_run)

        # So he launches PyQtAccounts to check for them
        window = Window()

        # A few seconds passes and there is no updates available dialog
        QTest.qWait(100)
        self.assertIsNone(
            window.res,
            "UpdatesAvailable window was created when there are no"
            "updates available!",
        )
