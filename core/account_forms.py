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

import akidump
import os

from forms import *
from utils import *
from widgets import *

HELP_TIP = ("<pre>Поки що у вас немає жодного акаунта.\n" +
                          '{0:<36}\n'.format("Спробуйте:") +
                          '{0:<36}\n'.format("Натиснути +") +
                          '{0:<36}\n'.format("Гарячі клавіші Ctl+N") +
                          '{0:<36}\n'.format("Меню: File -> New account...") +
                          "</pre>")

class CreateAcc(CreateForm):
    def __init__(self, title, db, helpTip, parent=None):
        namePlaceholder = "ім'я акаунта"
        nameTip = ''
        passTip = ("Якщо ви не хочете придумувати пароль ви можете\n"
                      "натиснути кнопку 'Згенерувати', аби згенерувати його.")
        nameError = 'Акаунт з таким іменем вже існує!'
        CreateForm.__init__(self, title, namePlaceholder, nameError, nameTip, passTip, \
                                                     helpTip, parent)
        self.hide()
        self.db = db

        self.accountLabel = QLabel('Акаунт:')
        self.accountInput = QLineEdit()
        self.accountInput.setPlaceholderText('назва акаунту')
        self.accountInput.textChanged.connect(self.validateName)

        self.nameInput.setPlaceholderText("ваше ім'я або нікнейм")
        self.nameInput.textChanged.disconnect()

        self.emailLabel = QLabel('E-mail:')
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText('введіть e-mail акаунта')

        self.dateLabel = QLabel('Дата народження:')
        self.dateInput = QDateEdit()
        self.dateInput.setDisplayFormat('dd.MM.yyyy')
        dateLayout = QHBoxLayout()
        dateLayout.addWidget(self.dateLabel)
        dateLayout.addWidget(self.dateInput)

        self.commentLabel = QLabel('Коментарій:')
        self.commentInput = QTextEdit()
        self.commentInput.setPlaceholderText('Введіть коментарій')
        self.commentInput.setMinimumHeight(200)

        self.layout.insertWidget(1, self.accountLabel)
        self.layout.insertWidget(2, self.accountInput)
        self.layout.insertWidget(5, self.emailLabel)
        self.layout.insertWidget(6, self.emailInput)
        self.layout.insertLayout(13, dateLayout)
        self.layout.insertWidget(14, self.commentLabel)
        self.layout.insertWidget(15, self.commentInput)

        # Creating a scroll area which contains a fake layout (widget) which
        # contains layout of form, and putting
        # scroll area to main layout, and then setting the main layout to
        # layout of the form:
        # form -> main layout -> scroll area -> fake layout -> layout -> content
        self.scrollArea = QScrollArea()
        layout = QWidget()
        layout.setLayout(self.layout)
        self.scrollArea.setWidget(layout)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)

    def clear(self):
        self.accountInput.clear()
        self.nameInput.clear()
        self.emailInput.clear()
        self.passField.passInput.clear()
        self.passRepeatField.passInput.clear()
        self.commentInput.clear()

        for i in range(self.errors.layout().count()):
            err = self.errors.layout().itemAt(i).widget()
            err.hide()

        self.createButton.setEnabled(False)
        self.hide()
        self.helpTip.show()

class CreateAccForm(CreateAcc):
    def __init__(self, db, helpTip, parent=None):
        title = 'Створити акаунт'
        CreateAcc.__init__(self, title, db, helpTip, parent)

    def validateName(self, event):
        name = self.accountInput.text()
        if name in getAkiList(self.db):
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

    def create(self, event):
        accountname = self.accountInput.text()
        name = self.nameInput.text()
        email = self.emailInput.text()
        password = self.passField.passInput.text().encode()
        date = self.dateInput.text()
        comment = self.commentInput.toPlainText().replace('\n', '\n\n')

        account = akidump.Account(accountname, name, email, password, date,
                                comment)
        self.db[accountname] = account
        self.clear()

        item = QStandardItem(self.list.icon, accountname)
        self.list.model.appendRow(item)
        self.list.model.sort(0)
        self.clear()

        self.tips['help'].setText("Виберіть акаунт")

class EditAccForm(CreateAcc):
    def __init__(self, db, helpTip):
        title = 'Редагувати акаунт'
        CreateAcc.__init__(self, title, db, helpTip)
        self.createButton.setText('Зберегти')
        self.deleteButton = QPushButton('Видалити')
        self.deleteButton.clicked.connect(self.delete)
        self.buttonsLayot.insertWidget(1, self.deleteButton)

    def validateName(self, event):
        name = self.accountInput.text()
        if name in getAkiList(self.db) and name != self.account.account:
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

    def delete(self):
        for win in self.windows:
            if win.name == self.name:
                break
        action = QMessageBox.warning(win, 'Увага!',
                             'Ви певні що хочете видалити акаунт '
                             '<i><b>{}</b></i>'.format(self.account.account),
                             buttons=QMessageBox.No | QMessageBox.Yes,
                             defaultButton=QMessageBox.No)
        if action == QMessageBox.Yes:
            del self.db[self.account.account]

            for item in self.list.model.findItems(self.account.account):
                self.list.model.removeRow(item.row())
            self.list.model.sort(0)
            self.clear()

            if not getAkiList(self.db):
                self.tips['help'].setText(HELP_TIP)

    def setAcc(self, index):
        if not index:
            return
        for account in self.db:
            if account == index.data():
                self.old_account = index.data()
                self.account = self.db[account]
                self.accountInput.setText(account)
                self.nameInput.setText(self.account.name)
                self.emailInput.setText(self.account.email)
                password = self.account.password.decode()
                self.passField.passInput.setText(password)
                self.passRepeatField.passInput.setText(password)

                day, month, year = [int(d) for d in self.account.date.split(
                    '.')]
                self.dateInput.setDate(QDate(year, month, day))

                self.commentInput.setText(self.account.comment)
                hide(self.forms, self.tips)
                self.show()
                return

        self.tips['edit-w'].show()
        self.forms['open'].hide()

    def create(self, event):
        accountname = self.accountInput.text()
        name = self.nameInput.text()
        email = self.emailInput.text()
        password = self.passField.passInput.text().encode()
        date = self.dateInput.text()
        comment = self.commentInput.toPlainText()

        account = akidump.Account(accountname, name, email, password, date,
                                comment)
        self.db[accountname] = account
        self.clear()

        for item in self.list.model.findItems(self.old_account):
             self.list.model.removeRow(item.row())
        item = QStandardItem(self.list.icon, accountname)
        self.list.model.appendRow(item)
        self.list.model.sort(0)
        self.clear()

class ShowAccForm(QWidget):
    def __init__(self, db, parent=None):
        QWidget.__init__(self, parent)
        self.hide()
        self.db = db

        self.account = QLabel()
        self.name = QLabel()
        self.email = QLabel()
        self.password = QLabel()
        self.date = QLabel()
        self.comment = QTextEdit()
        self.comment.setReadOnly(True)

        for label in (self.account, self.name, self.email, self.password,
                      self.date, self.comment):
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            label.setCursor(QCursor(Qt.IBeamCursor))

        self.copyTip = Tip('Ви можете натиснути гарячі клавіші Ctrl+C\n'
                           'аби скопіювати пароль і e-mail одразу.')

        layout = QVBoxLayout()
        layout.addWidget(self.account)
        layout.addWidget(self.name)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.date)
        layout.addWidget(self.copyTip)
        layout.addWidget(self.comment)
        self.setLayout(layout)

    def setAcc(self, index):
        accountname = index.data()
        account = self.db[accountname]

        self.account.setText('Акаунт: ' + account.account)
        self.name.setText("Ім'я: " + account.name)
        self.email.setText('E-mail: ' + account.email)
        self.password.setText('Пароль: ' + account.password.decode())
        self.date.setText('Дата: ' + account.date)
        self.comment.setText('Коментарій: ' + account.comment)

    def copyAcc(self):
        # to copy password
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.password.text().replace('Пароль: ', ''))

        # to copy e-mail
        email = self.email.text().replace('E-mail: ', '')
        os.system(f'echo {email} | xclip')