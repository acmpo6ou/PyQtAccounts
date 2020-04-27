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

import glob
import git
import os
from string import *
from core.const import *
import core.const


def getDbList():
    """
    This function returns list of databases in your `src` directory, path to which is defined by
    SRC_DIR constant from core.const module.
    Function finds databases by their .db files.
    """
    return [os.path.basename(db).replace('.db', '') for db in
            glob.glob(f'{core.const.SRC_DIR}/*.db')]


def getAkiList(db):
    """
    This function returns list of accounts in your `db` database, which you pass as argument.
    """
    return [acc for acc in db]


def getVersion():
    """
    This function returns current version of the program.
    Actually it returns last tag of program repository sorted by date.
    """
    repo = git.Repo('.')
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    version = tags[-1]
    return version


def hide(*args):
    """
    This function hides all widgets in all instances that are passed to it as arguments.
    """
    for arg in args:
        for widget in arg:
            arg[widget].hide()


def validName(name):
    """
    This function returns validated name (i.e. without unallowed characters).
    We need it because we store databases in files called by their name (plus `.db` extension)
    and you cant name files with for example this `/@` characters.

    :param name:
    name of database you need to validate.
    :return:
    validated name.

    Example of usage:
    >>> validName('hello\/@ it is name')                # all unallowed characters are removed
    'helloitisname'
    >>> validName('hello_this.is(allowed-characters)')  # '.()-_' -- are allowed characters
    'hello_this.is(allowed-characters)'
    """
    valid = ascii_letters + digits + '.()-_'
    result = ''
    for c in name:
        if c in valid:
            result += c
    return result


class Index:
    """
    Fake index for main database settings.
    This class emulates StandardItemModel index that is passed to selected() signal when you
    click at the QListView list element. This index stores the name of element being clicked.

    We need this class to implement main database setting: when on startup we automatically
    select main database which specified as `main_db` value of QSettings.
    """

    def __init__(self, name):
        self.name = name

    def data(self):
        """
        This method is called when you try to get name of element which index represents.
        Example of usage:
        >>> i = Index('main')
        >>> i.data()
        'main'
        """
        return self.name
