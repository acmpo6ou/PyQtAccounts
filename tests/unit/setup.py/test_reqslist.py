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

installed = '/usr/share/icons/Humanity/actions/48/gtk-yes.svg'
not_installed = '/usr/share/icons/Humanity/actions/48/stock_not.svg'


class ReqsListTest(UnitTest):
    def test_icons(self):
        self.assertTrue(os.path.exists(installed))
        self.assertTrue(os.path.exists(not_installed))

    def test_reqs(self):
        reqs = Mock()
        reqs.cant_install = ('git', 'xclip')
        reqs.to_install = ('gitpython',)
        reqs.installed = ('python3-pip', 'cryptography')

        reqslist = ReqsList(reqs)
        self.assertEqual(reqslist.editTriggers(), QAbstractItemView.NoEditTriggers)
        self.assertEqual(reqslist.model, QListView.model(reqslist))  # We override model method

        model = reqslist.model
        length = len(reqs.cant_install) + len(reqs.to_install) + len(reqs.installed)
        self.assertEqual(length, model.rowCount())

        for i in range(model.rowCount()):
            req = model.item(i).text()
            icon = model.item(i).icon().pixmap(QSize(48, 48)).toImage()

            if req in reqs.installed:
                self.assertEqual(icon, QImage(installed))
            else:
                self.assertEqual(icon, QImage(not_installed))
