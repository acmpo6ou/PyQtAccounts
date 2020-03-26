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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import glob
import git
import os
from string import *


def getDbList():
    return [os.path.basename(db).replace('.db', '') for db in
            glob.glob('../src/*.db')]


def getAkiList(db):
    return [acc for acc in db]


def getVersion():
    repo = git.Repo('../')
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    version = tags[-1]
    return version


def hide(*args):
    for arg in args:
        for widget in arg:
            arg[widget].hide()


def validName(name):
    valid = ascii_letters + digits + '.()-_'
    result = ''
    for c in name:
        if c in valid:
            result += c
    return result


class Index:
    '''Fake index for main database settings.'''

    def __init__(self, name):
        self.name = name

    def data(self):
        return self.name
