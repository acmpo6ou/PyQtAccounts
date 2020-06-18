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
This module provides functions for creating, encrypting and decrypting databases.
"""

import os
import base64
import core.akidump as akidump
import core.const

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generateSalt(saltfile):
    """
    This function generates salt for cryptographic encryption and writes it to file.
    :param saltfile:
    represents path where file with salt will be located.
    """
    salt = os.urandom(16)
    with open(saltfile, 'wb') as file:
        file.write(salt)


def openDatabase(dbname, password):
    """
    This function opens database by its name and password.
    :param dbname:
    represents name of database
    :param password:
    represents password of database, must be byte string
    :return:
    opened database, type: dict
    """

    # here we construct path to database and its salt file by concatenating SRC_DIR constant,
    # database name and .db or .bin extension,
    # SRC_DIR represents name of folder in which database files are stored.
    dbfile = f'{core.const.SRC_DIR}/' + dbname + '.db'
    saltfile = f'{core.const.SRC_DIR}/' + dbname + '.bin'

    with open(saltfile, 'rb') as file:
        salt = file.read()

    # here we using fernet encryption function to decrypt and deserialize database.
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    with open(dbfile, 'rb') as db:
        token = db.read()

    data = f.decrypt(token)
    db = akidump.loads(data)

    return db


def encryptDatabase(dbname, db, password):
    """
    THis function encrypts database.
    :param dbname:
    name of the database
    :param db:
    database, type: dict
    :param password:
    password of the database, type: byte string
    :return:
    encrypted database string
    """
    # here we construct path to salt file of database by concatenating SRC_DIR constant,
    # database name and .bin extension
    saltfile = f'{core.const.SRC_DIR}/' + dbname + '.bin'

    with open(saltfile, 'rb') as file:
        salt = file.read()

    # here we using fernet encryption function to encrypt and serialize database.
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    data = akidump.dumps(db)
    token = f.encrypt(data)
    return token


def newDatabase(dbname, password):
    """
    This function creates empty database and saves it to file.
    :param dbname:
    name of the database
    :param password:
    password of the database, type: byte string
    """
    # here we construct path to database and its salt file by concatenating SRC_DIR constant,
    # database name and .db or .bin extension,
    # SRC_DIR represents name of folder in which database files are stored.
    saltfile = f'{core.const.SRC_DIR}/' + dbname + '.bin'
    dbfile = f'{core.const.SRC_DIR}/' + dbname + '.db'

    generateSalt(saltfile)
    token = encryptDatabase(dbname, {}, password)

    with open(dbfile, 'wb') as file:
        file.write(token)


def isEqual(first, second):
    """
    This function compares two databases and returns True if they are equal.
    """
    if set(first) != set(second):
        return False

    for acc in first:
        if first[acc] != second[acc]:
            return False
    else:
        return True
