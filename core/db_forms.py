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
from core.testutils import QWidget

from core.forms import *
from core.widgets import *
from core.getaki import *
from core.windows import *
from core.utils import *
import core.const
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken

SRC_DIR = core.const.SRC_DIR


class CreateDbForm(CreateForm):
    """
    This is a superclass which specifies CreateForm class for create database form needs.
    """

    def __init__(self, helpTip, parent=None):
        """
        This constructor creates the form specifying all widgets parameters.
        :param helpTip:
        Tip that will be displayed when form is hidden.
        :param parent:
        The parent of the form.
        """
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
        """
        This method called when user presses `Create` button.
        It create database from data that user entered in form and saves it to file called
        `<database name>.db`, it also creates salt file of the database called `<database
        name>.bin`.
        """
        # Here we get validated name and password, create database and clear form
        name = validName(self.nameInput.text())
        password = self.passField.passInput.text().encode()
        newDatabase(name, password)
        self.clear()

        # here we update database list and help tip
        item = QStandardItem(self.list.icon, name)
        self.list.model.appendRow(item)
        self.list.model.sort(0)
        self.tips['help'].setText("Виберіть базу данних")

    def validateName(self, event):
        """
        This method validates whether name entered in the field and is it unique.
        """
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
    """
    This is a superclass which specifies CreateForm class for edit database form needs.
    """

    def __init__(self, tips, windows, parent=None):
        """
        This constructor creates the form specifying all widgets parameters appropriately to
        edit form, it also adds `Delete` button and changes create buttons text to `Save`
        :param tips:
        list of all tips
        :param windows:
        list of all windows
        :param parent:
        parent of the form
        """
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
        self.buttonsLayout.insertWidget(1, self.deleteButton)

    def setDb(self, index):
        if not index:
            return
        # Here we iterate through all windows and when we find one that matches our name
        # we stop loop.
        for win in self.windows:
            if win.name == index.data():
                # Here we saving name of the old database and set all the fields values
                self.db = win
                self.old_name = win.name
                self.nameInput.setText(win.name)
                password = win.password.decode()
                self.passField.passInput.setText(password)
                self.passRepeatField.passInput.setText(password)
                hide(self.forms, self.tips)
                self.show()
                return

        # if no window for given database exist (i.e. it isn't opened yet) we show edit warning
        hide(self.forms, self.tips)
        self.tips['edit-w'].show()

    def validateName(self, event):
        """
        This method validates whether name entered in the field and is it unique (but if
        the name didn't changed it's okay!).
        """
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
        """
        This method deletes database showing confirmation dialog.
        """
        name = self.db.name
                                     # first is the main window
        action = QMessageBox.warning(self.windows[0], 'Увага!',
                                     'Ви певні що хочете видалити базу данних '
                                     '<i><b>{}</b></i>'.format(name),
                                     buttons=QMessageBox.No | QMessageBox.Yes,
                                     defaultButton=QMessageBox.No)

        # If users answer is `Yes` we delete database
        if action == QMessageBox.Yes:
            os.remove(f'{core.const.SRC_DIR}/{name}.db')
            os.remove(f'{core.const.SRC_DIR}/{name}.bin')

            # and we update database list
            for item in self.model.findItems(name):
                self.model.removeRow(item.row())
            self.model.sort(0)
            self.clear()
            self.db.ask = False

            # to avoid errors that occurs because of close behavior
            self.windows.remove(self.db)
            self.db.closeEvent = lambda *args: None

            # and then we close database window
            self.db.close()

            # if there is no databases left we show appropriate tip
            if not getDbList():
                self.tips['help'].setText(HELP_TIP)

    def create(self):
        """
        This method more logically would be to name as `save` but it called `create` due to
        compatibility with superclass.
        This method called when user presses `Save` button.
        It deletes old account and replaces it with new one created from data that user entered
        in form.
        """

        # Here we get validated name and password
        name = validName(self.nameInput.text())
        password = self.passField.passInput.text().encode()

        # Then we remove old database
        os.remove(f'{core.const.SRC_DIR}/{self.old_name}.db')
        os.remove(f'{core.const.SRC_DIR}/{self.old_name}.bin')

        # And we create new database based on the data of the form
        newDatabase(name, password)
        self.clear()

        # Here we delete old database name from list and add new name to it
        for item in self.model.findItems(self.old_name):
            self.model.removeRow(item.row())

        item = QStandardItem(self.list.icon, name)
        self.list.model.appendRow(item)
        self.list.model.sort(0)

        # to avoid errors that occurs because of close behavior
        self.windows.remove(self.db)
        self.db.closeEvent = lambda *args: None

        # Then we close database window
        self.db.close()


class OpenDbForm(QWidget):
    """
    This class represents form that we use to open databases
    """
    def __init__(self, helpTip, windows, parent=None):
        """
        This is constructor of the form, it creates all widgets.
        :param helpTip:
        Tip that will be displayed when form is hidden.
        :param windows:
        list of all windows
        :param parent:
        The parent of the form.
        """
        QWidget.__init__(self, parent)
        self.hide()
        self.name = None
        self.windows = windows
        self.helpTip = helpTip

        # Here we define title, password label and field of the form
        self.title = Title()
        self.passLabel = QLabel('Пароль:')
        self.passField = PasswordField('введіть пароль')
        self.passField.passInput.returnPressed.connect(self.open)

        # This is error that we show when password is incorrect
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
        """
        This method called when chose database from the list.
        :param index:
        the index of the database being chosen, it stores database name.
        """
        # Here we set title according to the name of database being chosen
        self.name = index.data()
        self.title.setText('Відкрити базу данних <i><b>{}</b></i>'.format(self.name))

    def open(self):
        """
        This method called when user presses `Open` button.
        It opens database creating its window.
        :return:
        """
        # we obtain name and password of the database
        name = self.name
        password = self.passField.passInput.text().encode()

        # Here we trying to open database
        try:
            db = openDatabase(self.name, password)
        except (InvalidSignature, InvalidToken):
            # if something goes wrong (i.e. password is incorrect)
            # we show appropriate error message
            self.incorrectPass.show()
            return
        else:
            # if everything is alright we hide error message in case if it showed
            self.incorrectPass.hide()

        # then we clear form, hide it and show help tip
        self.name = None
        self.passField.passInput.clear()
        self.hide()
        self.helpTip.show()

        # and create database window saving it to the windows list
        win = DbWindow(self.windows, name, db, password)
        self.windows.append(win)
        # when main window is closed we close all database windows
        win.setAttribute(Qt.WA_QuitOnClose)
