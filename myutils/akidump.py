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

class Account:
    def __init__(self, account, name, email, password, date, comment):
        self.account = account
        self.name = name
        self.email = email
        self.password = password
        self.date = date
        self.comment = comment

SEPARATOR = 's' + '-='*30 + 'e'

def dumps(data):
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
    data = data.decode().split(SEPARATOR)
    formated_data = []
    part = []
    for i, line in enumerate(data):
        part.append(line)
        if (int(i)+1) % 6 == 0:
            formated_data.append(part[:])
            part = []

    res = {}
    for accountname, name, email, password, date, comment in formated_data:
        account = Account(accountname, name, email, password.encode(), date,
                          comment)
        res[accountname] = account
    return res

def main():
    pass

if __name__ == '__main__':
    main()