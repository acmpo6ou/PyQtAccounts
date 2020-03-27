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
from PyQt5.QtCore import *
from testutils import QWidget

from forms import *
from widgets import *
from getaki import *
from windows import *
from utils import *

from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken

HELP_TIP_DB = ("<pre>Поки що у вас немає жодної бази данних.\n" +
                          '{0:<39}\n'.format("Спробуйте:") +
                          '{0:<39}\n'.format("Натиснути +") +
                          '{0:<39}\n'.format("Гарячі клавіші Ctl+N") +
                          '{0:<39}\n'.format("Меню: File -> New database...") +
                          "</pre>")

class CreateDbForm(CreateForm):
    def __init__(self, helpTip, parent=None):
        title = 'Створити базу данних'
        namePlaceholder = "ім'я бази данних"
        nameTip = ("Для імені бази данних підтримуються \n"
                           "лише великі та малі англійські символи, а також ці: .()-_\n"
                           "Усі неправильні символи видаляються автоматично.")
        passTip = ("Якщо ви не хочете придумувати пароль ви можете\n"
                      "натиснути кнопку 'Згенерувати', аби згенерувати його.")
        nameError = 'База даних з таким іменем вже існує!'
        CreateForm.__init__(self, title, namePlaceholder, nameError, nameTip, passTip, \
                                                     helpTip, parent)
    def create(self, event):
        name = validName(self.nameInput.text())
        password = self.passField.passInput.text().encode()
        newDatabase(name, password)
        self.clear()

        item = QStandardItem(self.list.icon, name)
        self.list.model.appendRow(item)
        self.list.model.sort(0)

        self.tips['help'].setText("Виберіть базу данних")

    def validateName(self, event):
        name = validName(self.nameInput.text())
        if name in getDbList():
            self.nameError.show()
            self.createButton.setEnabled(False)
            self.validate['name'] = False
        elif name == '':
            self.nameFilledError.show()
            self.createButton.setEnabled(False)
            self.validate['name'] = False
        else:
            self.validate['name'] = True
            self.nameError.hide()
            self.nameFilledError.hide()

        if self.validate['pass'] and self.validate['name']:
            self.createButton.setEnabled(True)

class EditDbForm(CreateForm):
    def __init__(self, tips, windows, parent=None):
        title = 'Редагувати базу данних'
        namePlaceholder = "ім'я бази данних"
        nameTip = ("Для імені бази данних підтримуються \n"
                           "лише великі та малі англійські символи, а також ці: .()-_\n"
                           "Усі неправильні символи видаляються автоматично.")
        passTip = ("Якщо ви не хочете придумувати пароль ви можете\n"
                      "натиснути кнопку 'Згенерувати', аби згенерувати його.")
        nameError = 'База даних з таким іменем вже існує!'
        CreateForm.__init__(self, title, namePlaceholder, nameError, nameTip, passTip, \
                                                     tips['help'], parent)
        self.windows = windows
        self.hide()
        self.tips = tips

        self.createButton.setText('Зберегти')
        self.deleteButton = QPushButton('Видалити')
        self.deleteButton.clicked.connect(self.delete)
        self.buttonsLayot.insertWidget(1, self.deleteButton)

    def setDb(self, index):
        if not index:
            return
        for win in self.windows:
            if win.name == index.data():
                self.db = win
                self.old_name = win.name
                self.nameInput.setText(win.name)
                password = win.password.decode()
                self.passField.passInput.setText(password)
                self.passRepeatField.passInput.setText(password)
                hide(self.forms, self.tips)
                self.show()
                return

        hide(self.forms, self.tips)
        self.tips['edit-w'].show()

    def validateName(self, event):
        name = validName(self.nameInput.text())
        if name in getDbList() and name != self.db.name:
            self.nameError.show()
            self.createButton.setEnabled(False)
            self.validate['name'] = False
        elif name == '':
            self.nameFilledError.show()
            self.createButton.setEnabled(False)
            self.validate['name'] = False
        else:
            self.validate['name'] = True
            self.nameError.hide()
            self.nameFilledError.hide()

        if self.validate['pass'] and self.validate['name']:
            self.createButton.setEnabled(True)

    def delete(self, event):
        name = self.db.name
                            # first is the main window
        action = QMessageBox.warning(self.windows[0], 'Увага!',
                             'Ви певні що хочете видалити базу данних '
                             '<i><b>{}</b></i>'.format(name),
                             buttons=QMessageBox.No | QMessageBox.Yes,
                             defaultButton=QMessageBox.No)
        if action == QMessageBox.Yes:
            os.remove('../src/{}.db'.format(name))
            os.remove('../src/{}.bin'.format(name))

            for item in self.model.findItems(name):
                self.model.removeRow(item.row())
            self.model.sort(0)
            self.clear()
            self.db.ask = False
            self.db.close()

            if not getDbList():
                self.tips['help'].setText(HELP_TIP)

    def create(self):
        name = validName(self.nameInput.text())
        password = self.passField.passInput.text().encode()

        os.remove('../src/{}.db'.format(self.old_name))
        os.remove('../src/{}.bin'.format(self.old_name))

        newDatabase(name, password)
        self.clear()

        for item in self.model.findItems(self.old_name):
            self.model.removeRow(item.row())

        item = QStandardItem(self.list.icon, name)
        self.list.model.appendRow(item)
        self.list.model.sort(0)
        self.db.close()

class OpenDbForm(QWidget):
    def __init__(self, helpTip, windows, parent=None):
        QWidget.__init__(self, parent)
        self.hide()
        self.name = None
        self.windows = windows
        self.helpTip = helpTip

        self.title = Title()
        self.passLabel = QLabel('Пароль:')
        self.passField = PasswordField('введіть пароль')
        self.passField.passInput.returnPressed.connect(self.open)

        self.incorrectPass = Error('Неправильний пароль!')
        self.incorrectPass.hide()

        self.openButton = QPushButton('Відкрити')
        self.openButton.clicked.connect(self.open)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.title)
        layout.addWidget(self.passLabel)
        layout.addLayout(self.passField)
        layout.addWidget(self.incorrectPass)
        layout.addWidget(self.openButton)

    def setDb(self, index):
        self.name = index.data()
        self.title.setText('Відкрити базу данних <i><b>{}</b></i>'.format(self.name))

    def open(self):
        name = self.name
        password = self.passField.passInput.text().encode()
        try:
            db = openDatabase(self.name, password)
        except (InvalidSignature, InvalidToken):
            self.incorrectPass.show()
            return
        else:
            self.incorrectPass.hide()

        self.incorrectPass.hide()
        self.name = None
        self.passField.passInput.clear()

        win = DbWindow(self.windows, name, db, password)
        self.windows.append(win)
        win.setAttribute(Qt.WA_QuitOnClose)


        self.hide()
        self.helpTip.show()