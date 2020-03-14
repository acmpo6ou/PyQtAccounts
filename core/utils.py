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
import os.path
import os
import tarfile
from string import *
from account_forms import *
from getaki import *


def getDbList():
    return [os.path.basename(db).replace('.db', '') for db in
            glob.glob('../src/*.db')]

def getAkiList(db):
    return [acc for acc in db]

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

def selectDb(obj, index):
    obj.index = index

    for win in obj.windows:
        if index.data() == win.name:
            hide(obj.forms, obj.tips)
            obj.tips['already-open'].show()
            return
    obj.forms['open'].setDb(index)
    hide(obj.forms, obj.tips)
    obj.forms['open'].show()
    obj.forms['open'].passField.passInput.setFocus()

def export(name, path, parent):
    name = name.data()
    try:
        file = tarfile.open(path, 'w')
        os.chdir(os.path.abspath(__file__).replace('utils.py', '../src'))
        file.add('{}.db'.format(name))
        file.add('{}.bin'.format(name))
        os.chdir(os.path.abspath(__file__).replace('utils.py', ''))
        file.close()
    except Exception:
        QMessageBox.critical(parent, 'Помилка!', 'Експорт бази данних '
                                                 'завершився невдачею.')
    else:
        QMessageBox.information(parent, 'Експорт', 'Успішно експортовано базу '
                                        'данних <i><b>{}</b></i>'.format(name))

def _import(path, parent):
    try:
        tar = tarfile.open(path)
        for i, file in enumerate(tar.getmembers()):
            if '.db' not in file.name and '.bin' not in file.name:
                raise Exception('Невірний файл!')
            name = file.name.replace('.db', '').replace('.bin', '')
        if i != 1:
            raise Exception('Невірний файл!')
        tar.extractall('../src/')

        model = parent.dbs.layout().list.model
        list = parent.dbs.layout().list

        for item in model.findItems(name):
            model.removeRow(item.row())

        item = QStandardItem(list.icon, name)
        model.appendRow(item)
        model.sort(0)
        parent.dbs.layout().tips['help'].setText("Виберіть базу данних")

    except Exception as err:
        QMessageBox.critical(parent, 'Помилка!', str(err))
    else:
        QMessageBox.information(parent, 'Імпорт',
                'Успішно імпортовано базу данних <i><b>{}</b></i>'.format(name))