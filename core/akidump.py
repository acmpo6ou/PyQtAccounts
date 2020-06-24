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
This module provides functions and classes for serializing and deserializing accounts.
This module has replaced pickle module from standard library because of security reasons.
"""

import json

# NOTE: this separator is now obsolete because we use json to serialize our databases
SEPARATOR = 's' + '-=' * 30 + 'e'  # this is a separator between accounts in .db file.


class Account:
    """
    This class stores data about account.
    """
    def __init__(self,
                 account,
                 name,
                 email,
                 password,
                 date,
                 comment,
                 copy_email=True,
                 attach_files=None):
        """
        This constructor saves all account data.
        """
        self.account = account
        self.name = name
        self.email = email
        self.password = password
        self.date = date
        self.comment = comment
        self.copy_email = copy_email
        # here we check whether attached_files argument is supplied if yes we
        # assign it to self.attached_files attribute else we assign empty
        # dictionary to self.attached_files
        # NOTE: that we do this in that strange way because we dict is mutable
        # type and we can't just write attached_files={} in __init__ constructor
        self.attached_files = attach_files if attach_files else {}

    def __eq__(self, other):
        """
        This method compares attributes of two accounts and returns True if all of them are equal.
        """
        attrs = ('account', 'name', 'email', 'password', 'date', 'comment',
                 'copy_email')

        for a in attrs:
            my = getattr(self, a)
            his = getattr(other, a)
            if my != his:
                return False
        else:
            return True

    def to_dict(self):
        """
        We use this method to convert our Account instance to dictionary which
        is json serializable.
        """
        return {
            'account': self.account,
            'name': self.name,
            'email': self.email,
            'password': self.password.decode(),
            'date': self.date,
            'comment': self.comment,
            'copy_email': self.copy_email,
        }


def dumps(data):
    """
    This function serializes database to string using json module.
    :param data:
    represents database, type: dict
    :return:
    serialized string, type: byte string
    """
    db = {}
    for account in data:
        db[account] = data[account].to_dict()
    return json.dumps(db).encode()


def loads_old(data):
    """
    This function deserializes string to database.
    NOTE: this function is obsolete but we use it only for backward
    comparability with those databases that are serialized in obsolete way.
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


def loads_json(data):
    """
    This function deserializes json string to database.
    :param data:
    json string to deserialize
    """
    # here db will be a dict which will contain dicts that will represent our
    # Account instances
    db = json.loads(data)

    # here we convert dicts in `db` to Account instances
    for account in db:
        # here we first encode password value of account dict to byte string,
        # because password in Account class must be a byte string
        password = db[account]['password'].encode()
        db[account]['password'] = password

        # then we unpack account dict as arguments for Account constructor to
        # create Account instance from account dict, then we save freshly
        # created Account instance back to the database
        db[account] = Account(**db[account])

    # finally we return deserialized database
    return db


def loads(data):
    """
    This function is an interface to `loads_old` and `loads_json` functions.
    `loads` will use `loads_old` for databases serialized in the
    obsolete way and `loads_json` for those serialized json way.
    """
    # here we first try to deserialize `data` using `loads_json`
    try:
        db = loads_json(data)
    except json.decoder.JSONDecodeError:
        # and if we cant decode that data, then perhaps it is database
        # serialized in the obsolete way, so we try `loads_old` to deserialize
        # it
        db = loads_old(data)

    # finally we return deserialized database
    return db
