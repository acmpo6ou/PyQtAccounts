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

import sys, os, base64
import os.path
from myutils import akidump

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generateSalt(saltfile):
    salt = os.urandom(16)
    with open(saltfile, 'wb') as file:
        file.write(salt)

def openDatabase(dbname, password):
    dbfile = 'src/' + dbname + '.db'
    saltfile = 'src/' + dbname + '.bin'
    with open(saltfile, 'rb') as file:
        salt = file.read()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    with open(dbfile, 'rb') as db:
        token = db.read()

    data = f.decrypt(token)
    db = akidump.loads(data)

    return db

def encryptDatabase(dbname, db, password):
    dbfile = 'src/' + dbname + '.db'
    saltfile = 'src/' + dbname + '.bin'

    with open(saltfile, 'rb') as file:
        salt = file.read()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    data = akidump.dumps(db)
    token = f.encrypt(data)
    with open(dbfile, 'wb') as db:
        db.write(token)

def newDatabase(dbname, password):
    saltfile = 'src/' + dbname + '.bin'
    db = {}
    generateSalt(saltfile)
    encryptDatabase(dbname, db, password)