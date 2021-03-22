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

# here are path to icons that represent installed and not installed requirements respectively
installed = "/usr/share/icons/Humanity/actions/48/gtk-yes.svg"
not_installed = "/usr/share/icons/Humanity/actions/48/stock_not.svg"


class ReqsListTest(UnitTest):
    """
    This class provides tests for ReqsList.
    """

    def test_icons(self):
        """
        This test tests does icons for installed and not installed requirements exist.
        """
        self.assertTrue(
            os.path.exists(installed), "Icon for installed requirements does not exist!"
        )
        self.assertTrue(
            os.path.exists(not_installed),
            "Icon for not installed requirements does not exist!",
        )

    def test_reqs(self):
        """
        This test tests ReqsList itself.
        """
        # here we create fake Reqs with fake lists of installed and not installed requirements
        reqs = Mock()
        reqs.cant_install = ("git", "xclip")
        reqs.to_install = ("gitpython",)
        reqs.installed = ("python3-pip", "cryptography")

        # and here we pass our fake reqs to ReqsList constructor creating ReqsList instance that
        # we will test
        reqslist = ReqsList(reqs)

        # here we check that user can't edit items in ReqsList
        self.assertEqual(
            reqslist.editTriggers(),
            QAbstractItemView.NoEditTriggers,
            "Items of ReqsList can be edited!",
        )

        # and here we check that model in our requirements list contains exactly that amount of
        # items that we specified by passing fake reqs in constructor
        model = reqslist.model
        length = len(reqs.cant_install) + len(reqs.to_install) + len(reqs.installed)
        self.assertEqual(
            length, model.rowCount(), "Length of ReqsList model is incorrect!"
        )

        # and here by iterating through all items of lists model we check that they have
        # appropriate icon
        for i in range(model.rowCount()):
            req = model.item(i).text()
            icon = model.item(i).icon().pixmap(QSize(48, 48)).toImage()

            if req in reqs.installed:
                self.assertEqual(
                    icon,
                    QImage(installed),
                    f"{req} has incorrect icon: must have `installed` icon!",
                )
            else:
                self.assertEqual(
                    icon,
                    QImage(not_installed),
                    f"{req} has incorrect icon: must have `not installed` icon!",
                )
