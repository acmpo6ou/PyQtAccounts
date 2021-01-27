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
"""
This module provides helper functions for PyQtAccounts.
"""

import glob

import git
import os
import re

import core.const

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


def getDbList():
    """
    This function returns list of databases in your `src` directory, path to which is defined by
    SRC_DIR constant from core.const module.
    Function finds databases by their .db files.
    """
    return [
        os.path.basename(db).replace('.db', '')
        for db in glob.glob(f'{core.const.SRC_DIR}/*.db')
    ]


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
    return tags[-1]


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
    valid = "[-a-zA-Z0-9.()_]"  # this are all characters that are valid
    # here we get list of all valid characters from name
    valid_chars = re.findall(valid, name)
    result = ''.join(valid_chars)  # finally we join them
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


def set_form_completers(form, db):
    """
    We use this function to set completion for name, email and account name
    fields of the given form.
    From `db` (which is database) we get all names,
    emails and account names to create completers.
    """

    # here we create sets of all emails, names and account names of
    # accounts of given database, so we can use them for completion
    emails = set()
    names = set()
    accountnames = set()
    for account in db:
        a = db[account]
        accountnames.add(account)
        emails.add(a.email)
        names.add(a.name)

    # here we create completer for email field of create account form
    completer = QCompleter(emails)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    form.emailInput.setCompleter(completer)

    # here we create completer for name field of create account form
    completer = QCompleter(names)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    form.nameInput.setCompleter(completer)

    # here we create completer for accountname field of create account form
    completer = QCompleter(accountnames)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    form.accountInput.setCompleter(completer)
