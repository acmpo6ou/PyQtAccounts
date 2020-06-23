#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh Bogdan
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
This module patches QWidget object from PyQt5.QtWidgets by adding some helpful for
testing functionality to all widgets, because every widget is inherits from QWidget.
Every module that imports PyQt5.QtWidgets need to import QtWidget object from this module for
tests to work properly.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os

# Here we pre-saving real QWidget methods
real_init = QWidget.__init__
real_show = QWidget.show
real_hide = QWidget.hide


def patched_show(self, *args, **kwargs):
    """
    This function is a patched show method for QWidget.
    It changes visibility attribute of widget to True, because it become visible when
    we show it.
    """
    self.visibility = True

    # here we call real show method only when TESTING environment variable is set to False
    # (like in production), but while testing we don't actually want windows to be opened,
    # because it will waste our computation resources and will slow down our tests.
    # However sometimes we need to build and show our window during testing, so
    # in that case those tests that need this must set TESTING to `Func`.
    if not os.getenv('TESTING') or os.getenv('TESTING') == 'Func':
        real_show(self, *args, **kwargs)


def patched_hide(self, *args, **kwargs):
    """
    This function is a patched hide method for QWidget.
    It changes visibility attribute of widget to False, because it is not visible any more when
    we hide it.
    """
    self.visibility = False

    # here we call real hide method only when TESTING environment variable is set to False
    # (like in production), but while testing we don't actually want windows to be opened or hidden,
    # because it will waste our computation resources and will slow down our tests.
    # However sometimes we need to build, show and hide our window during testing, so
    # in that case those tests that need this must set TESTING to `Func`.
    if not os.getenv('TESTING') or os.getenv('TESTING') == 'Func':
        real_hide(self)


def patched_init(self, *args, **kwargs):
    """
    This function is a patched constructor for QWidget.
    It initializes visibility attribute which represents whether widget visible or not.
    It really helpful during testing.
    """
    self.visibility = False
    real_init(self, *args, **kwargs)


# here we patch all methods of QWidget.
QWidget.__init__ = patched_init
QWidget.show = patched_show
QWidget.hide = patched_hide
