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
from core.testutils import QWidget
import core.widgets as widgets


class CreateForm(QWidget):
    def __init__(self, title, namePlaceholder, nameError, nameTip, passTip, \
                 helpTip, \
                 parent=None):
        QWidget.__init__(self, parent)
        self.hide()
        self.helpTip = helpTip

        self.title = widgets.Title(title)

        self.nameLabel = QLabel("Ім'я:")
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText(namePlaceholder)
        self.nameInput.textChanged.connect(self.validateName)

        self.passLabel = QLabel('Пароль:')
        self.passField = widgets.PasswordField('введіть пароль')
        self.passField.passInput.textChanged.connect(self.validatePass)

        self.nameTip = widgets.Tip(nameTip)
        self.passTip = widgets.Tip(passTip)

        self.validate = {'pass': False, 'name': False}

        self.passRepeatLabel = QLabel('Повторіть пароль:')
        self.passRepeatField = widgets.PasswordField('повторно введіть пароль')
        self.passRepeatField.passInput.textChanged.connect(self.validatePass)

        self.passEqError = widgets.Error('Паролі не співпадають!')
        self.passEqError.hide()
        self.passFilledError = widgets.Error('Введіть пароль!')
        self.passFilledError.hide()

        self.nameError = widgets.Error(nameError)
        self.nameError.hide()
        self.nameFilledError = widgets.Error("Введіть ім'я!")
        self.nameFilledError.hide()

        self.errors = QWidget()
        self.errors.setLayout(QVBoxLayout())
        self.errors.layout().addWidget(self.passEqError)
        self.errors.layout().addWidget(self.passFilledError)
        self.errors.layout().addWidget(self.nameError)
        self.errors.layout().addWidget(self.nameFilledError)

        self.createButton = QPushButton('Створити')
        self.createButton.setEnabled(False)
        self.generateButton = QPushButton('Згенерувати')
        self.cancelButton = QPushButton('Скасувати')
        self.createButton.clicked.connect(self.create)
        self.generateButton.clicked.connect(self.generate)
        self.cancelButton.clicked.connect(self.clear)

        self.buttonsLayot = QHBoxLayout()
        self.buttonsLayot.addWidget(self.cancelButton)
        self.buttonsLayot.addWidget(self.generateButton)
        self.buttonsLayot.addWidget(self.createButton)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.nameInput)
        self.layout.addWidget(self.nameTip)
        self.layout.addWidget(self.passLabel)
        self.layout.addLayout(self.passField)
        self.layout.addWidget(self.passRepeatLabel)
        self.layout.addLayout(self.passRepeatField)
        self.layout.addWidget(self.passTip)
        self.layout.addWidget(self.errors)
        self.layout.addLayout(self.buttonsLayot)
        self.setLayout(self.layout)

    def validatePass(self, event):
        passInput = self.passField.passInput.text()
        passRepeatInput = self.passRepeatField.passInput.text()
        if passInput != passRepeatInput:
            self.passEqError.show()
            self.createButton.setEnabled(False)
            self.validate['pass'] = False
        elif passInput == '' or passRepeatInput == '':
            self.passFilledError.show()
            self.createButton.setEnabled(False)
            self.validate['pass'] = False
        else:
            self.validate['pass'] = True
            self.passEqError.hide()
            self.passFilledError.hide()

        if self.validate['pass'] and self.validate['name']:
            self.createButton.setEnabled(True)

    def generate(self, event):
        self.dialog = widgets.GenPassDialog(self)
        self.dialog.show()

    def clear(self, event=None):
        self.nameInput.clear()
        self.passField.passInput.clear()
        self.passRepeatField.passInput.clear()

        for i in range(self.errors.layout().count()):
            err = self.errors.layout().itemAt(i).widget()
            err.hide()

        self.createButton.setEnabled(False)
        self.hide()
        self.helpTip.show()

    def create(self):
        print('Not implemented!')
