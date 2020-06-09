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
This module provides function to generate random password.
"""

import random
import string


def gen(symbols, length):
    """
    This function generates random password using symbols that passed in `symbols` argument.
    :param symbols:
    represents symbols that will be included in password:
    if `d` in symbols then digits will be included
    if `l` ascii lower case symbols
    if `u` ascii upper case symbols
    if `p` punctuation symbols
    :param length:
    represents length of password, by default 16
    :return:
    password string
    """
    symbs = ''
    if "d" in symbols:
        symbs += string.digits

    if "l" in symbols:
        symbs += string.ascii_lowercase

    if "u" in symbols:
        symbs += string.ascii_uppercase

    if "p" in symbols:
        symbs += string.punctuation

    password = ''
    for i in range(length):
        password += random.choice(symbs)
    return password


def checkHasOneOf(syms, password):
    """
    We use this method to check that password has at least one of characters
    specified in `syms`.
    """
    # here we iterate trough all characters of `syms`
    for s in syms:
        # and some of them is in password then we break and everything is OK.
        if s in password:
            break
    else:
        # else we raise exception
        raise AssertionError


def main(symbols, length=16):
    """
    This function uses gen() to generate password and then checks whether
    password contains specified in `symbols` characters. Because of random
    password generation even though user specified `d` in `symbols` to include
    digits, that doesn't necessary means that digits will be included! In rare
    cases gen() will generate password without digits even when `d` is specified
    in `symbols`.
    Note: parameters to this function are the same as to gen() so you can find
    their description there.
    """
    # here we call gen() to create password and if it does not contain
    # characters that are specified in `symbols` then we regenerate it again and again
    # until we generate password that contains at least one of the characters
    # that specified by types in `symbols`
    while True:
        password = gen(symbols, length)

        try:
            # here we check password
            if 'd' in symbols:
                checkHasOneOf(string.digits, password)
            if 'l' in symbols:
                checkHasOneOf(string.ascii_lowercase, password)
            if 'u' in symbols:
                checkHasOneOf(string.ascii_uppercase, password)
            if 'p' in symbols:
                checkHasOneOf(string.punctuation, password)

            # if everything is OK then we return generated password
            return password
        except AssertionError:
            # and if it doesn't contain some characters we regenerate it
            continue
