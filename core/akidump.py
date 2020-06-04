#!/usr/bin/env python3

# Copyright (c) 2020 Kolvah Bogdan
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
This module provides functions and classes for serializing and deserializing accounts.
This module has replaced pickle module from standard library because of security reasons.
"""

SEPARATOR = 's' + '-=' * 30 + 'e'  # this is a separator between accounts in .db file.


class Account:
    """
    This class stores data about account.
    """
    def __init__(self, account, name, email, password, date, comment):
        """
        This constructor saves all account data.
        """
        self.account = account
        self.name = name
        self.email = email
        self.password = password
        self.date = date
        self.comment = comment

    def __eq__(self, other):
        """
        This method compares attributes of two accounts and returns True if all of them are equal.
        """
        attrs = [a for a in dir(self) if not a.startswith('__')]

        for a in attrs:
            my = getattr(self, a)
            his = getattr(other, a)
            if my != his:
                return False
        else:
            return True


def dumps(data):
    """
    This function serializes database to string using SEPARATOR constant to separate accounts.
    :param data:
    represents database, type: dict
    :return:
    serialized string, type: byte string
    """
    res = ''
    for account in data:
        res += data[account].account + SEPARATOR
        res += data[account].name + SEPARATOR
        res += data[account].email + SEPARATOR
        res += data[account].password.decode() + SEPARATOR
        res += data[account].date + SEPARATOR
        res += data[account].comment + SEPARATOR

    return res.encode()


def loads(data):
    """
    This function deserializes string to database.
    :param data:
    string to deserialize, type: byte string
    :return:
    database, type: dict
    """
    data = data.decode().split(SEPARATOR)
    formated_data = []
    part = []
    for i, line in enumerate(data):
        part.append(line)
        if (int(i) + 1) % 6 == 0:
            formated_data.append(part[:])
            part = []

    res = {}
    for accountname, name, email, password, date, comment in formated_data:
        account = Account(accountname, name, email, password.encode(), date,
                          comment)
        res[accountname] = account
    return res
