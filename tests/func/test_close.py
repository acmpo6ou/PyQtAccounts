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
import unittest
import pytest
import os

from tests.base import AccsTest, FuncTest
from core.utils import *
from PyQtAccounts import *


class CloseWhenDatabaseOpenedTest(AccsTest):
    """
    This test class provides all tests for close event of database window.
    """

    def test_close_when_database_opened_Yes(self):
        """
        This test tests close event of main window when database window is
        opened and user presses `Yes` on confirmation dialog.
        """
        # Tom closes main window when database window is opened,
        # confirmation dialog appears asking does he
        # realy wants to close window, Tom answers `No`.
        self.monkeypatch.setattr(
            QMessageBox,
            "question",
            self.mess("Увага!", "Ви певні що хочете вийти?", button=QMessageBox.Yes),
        )
        self.window.close()

        # and database window disappears
        self.assertEqual(
            len(self.window.windows),
            1,
            "Database window is not closed when user chose `Yes` in"
            "confirmation dialog!",
        )

    def test_close_when_database_opened_No(self):
        """
        This test tests close event of main window when database window is
        opened and user presses `No` on confirmation dialog.
        """
        # Tom closes main window when database window is opened,
        # confirmation dialog appears asking does he
        # realy wants to close window, Tom answers `No`.
        self.monkeypatch.setattr(
            QMessageBox,
            "question",
            self.mess("Увага!", "Ви певні що хочете вийти?", button=QMessageBox.No),
        )
        self.window.close()

        # and database window is still opened
        self.assertEqual(
            len(self.window.windows),
            2,
            "Database window is closed when user chose `No` in" "confirmation dialog!",
        )

    def test_close_when_no_database_opened(self):
        """
        This test tests close event of main window when there is no database
        window opened.
        """
        # Lea closes PyQtAccounts window when there is no database opened, when
        # she does this no confirmation popup is appearing.
        self.monkeypatch.setattr(QMessageBox, "question", self.mess_showed)
        del self.window.windows[1:]  # we have only 1 window - main window
        self.window.close()

        # window simply closes
        self.assertFalse(self.window.visibility, "Main window isn't closed!")

    def close_from_menu(self):
        """
        This test tests close event of main window through menu and when there
        is no database opened.
        """
        # Emily closes PyQtAccounts through menu:
        # First is `File` submenu, last is `Quit` action
        self.monkeypatch.setattr(QMessageBox, "question", self.mess_showed)
        self.menu(0, -1).trigger()

        # window is closed now
        self.assertFalse(self.window.visibility, "Main window isn't closed!")
