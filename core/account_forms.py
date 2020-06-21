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
This module provides classes for account forms.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from core.testutils import QWidget

import core.akidump as akidump
import os

from core.forms import *
from core.utils import *
from core.widgets import *
from core.const import *
import core.const

# This is mostly for testing
SRC_DIR = core.const.SRC_DIR


class CreateAcc(CreateForm):
    """
    This is a superclass which specifies CreateForm class to account forms needs.
    """
    def __init__(self, title, db, helpTip, parent=None):
        """
        This constructor creates the form specifying all widgets parameters.
        :param title:
        Text of title that will show up when creating form.
        For example: `Create new account`
        :param db:
        Database where we will save account once we create one.
        :param helpTip:
        Tip that will be displayed when form is hidden.
        :param parent:
        The parent of the form.
        """
        namePlaceholder = "ім'я акаунта"
        nameTip = ''  # there is no name characters validation for account names.
        passTip = ("Якщо ви не хочете придумувати пароль ви можете\n"
                   "натиснути кнопку 'Згенерувати', аби згенерувати його.")
        nameError = 'Акаунт з таким іменем вже існує!'
        CreateForm.__init__(self, title, namePlaceholder, nameError, nameTip, passTip, \
                            helpTip, parent)
        self.hide()
        self.db = db

        # Account create form needs more fields
        # here we create label and field for
        # account name (account name and nickname aren't same things!), e-mail, date of birth
        # and comment to account.
        self.accountLabel = QLabel('Акаунт:')
        self.accountInput = QLineEdit()
        self.accountInput.setPlaceholderText('назва акаунту')
        self.accountInput.textChanged.connect(self.validateName)

        self.nameInput.setPlaceholderText("ваше ім'я або нікнейм")
        self.nameInput.textChanged.disconnect()

        self.emailLabel = QLabel('E-mail:')
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText('введіть e-mail акаунта')

        # here we have radio buttons that will define what will be copied to
        # mouseboard `email` or `username` when user performs copy operation
        self.copy_label = QLabel(
            'Тут ви можете вибрати що буде копіюватися до\n'
            'мишиного буферу:')
        self.username_radio = QRadioButton('Username', self)
        self.email_radio = QRadioButton('E-mail', self)

        # e-mail will be copied to mouseboard by default
        self.email_radio.setChecked(True)

        copyLayout = QHBoxLayout()
        copyLayout.addWidget(self.email_radio)
        copyLayout.addWidget(self.username_radio)

        self.attach_label = QLabel("Додати файли:")
        self.attach_list = QListView()
        self.attach_list.setModel(QStandardItemModel())
        self.attach_list.pathmap = {}

        self.attach_file_button = QPushButton()
        self.attach_file_button.clicked.connect(self.attach_file)
        self.attach_file_button.setIcon(QIcon('img/list-add.png'))
        self.attach_file_button.setIconSize(QSize(22, 22))
        attachButtonsLayout = QVBoxLayout()
        attachButtonsLayout.addWidget(self.attach_file_button)

        attachLayout = QHBoxLayout()
        attachLayout.addWidget(self.attach_list)
        attachLayout.addLayout(attachButtonsLayout)

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
        self.layout.insertWidget(7, self.copy_label)
        self.layout.insertLayout(9, copyLayout)
        self.layout.insertLayout(15, dateLayout)
        self.layout.insertWidget(16, self.attach_label)
        self.layout.insertLayout(17, attachLayout)
        self.layout.insertWidget(16, self.commentLabel)
        self.layout.insertWidget(17, self.commentInput)

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
        """
        This method called when we hide form, to clean up all fields.
        """
        self.accountInput.clear()
        self.nameInput.clear()
        self.emailInput.clear()
        self.passField.passInput.clear()
        self.passRepeatField.passInput.clear()
        self.dateInput.setDate(QDate(2000, 1, 1))
        self.commentInput.clear()
        self.email_radio.setChecked(True)

        for i in range(self.errors.layout().count()):
            err = self.errors.layout().itemAt(i).widget()
            err.hide()

        self.createButton.setEnabled(False)
        self.hide()
        self.helpTip.show()

    def attach_file(self):
        """
        This method is invoked when user presses on attache file button.
        """
        # here we get path of file to attach and then we obtain its name
        home = os.getenv('HOME')
        path = QFileDialog.getOpenFileName(self.parent(),
                                           'Виберіть файл для закріплення',
                                           home)[0]
        name = os.path.basename(path)

        # by default `answer` is `Yes` so we always will create path mapping, if
        # file specified in `name` already exists then we will display
        # confirmation dialog and if user answers `No` then we will change
        # `answer` to False and mapping wont be created
        answer = QMessageBox.Yes

        # here we check if file we trying to attache already exists then we ask
        # user what to do – replace existing file or abort attach operation
        if name in self.attach_list.pathmap:
            answer = QMessageBox.warning(
                self.parent,
                'Увага!',
                'Файл з таким іменем вже існує, замінити?',
                buttons=QMessageBox.Yes | QMessageBox.No)

        # there is no need to add another file name to list if it already
        # exists, so here we add it only when it isn't exist yet
        else:
            # here we add attached file to attach list
            item = QStandardItem(name)
            self.attach_list.model().appendRow(item)

        # here we check `answer` variable if it is `Yes` then we create mapping
        # from file name to its path
        if answer == QMessageBox.Yes:
            # here we create mapping of attached file name and its path
            self.attach_list.pathmap[name] = path


class CreateAccForm(CreateAcc):
    """
    This is a class which specifies CreateAcc superclass even more.
    We use this class for creating account.
    """
    def __init__(self, db, helpTip, parent=None):
        """
        This constructor creates the form specifying title parameter, everything else it
        inherits from CreateAcc superclass.
        :param db:
        Database where we will save account once we create one.
        :param helpTip:
        Tip that will be displayed when form is hidden.
        :param parent:
        The parent of the form.
        """
        title = 'Створити акаунт'
        CreateAcc.__init__(self, title, db, helpTip, parent)

    def validateName(self, event):
        """
        This method validates whether name entered in the field and is it unique.
        """
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
        """
        This method called when user presses `Create` button.
        It create account from data that user entered in form and saves it to database(the `db`
        parameter).
        """
        # Here we create account and save it to database dict
        accountname = self.accountInput.text()
        name = self.nameInput.text()
        email = self.emailInput.text()
        password = self.passField.passInput.text().encode()
        date = self.dateInput.text()
        comment = self.commentInput.toPlainText().replace('\n', '\n\n')
        copy_email = self.email_radio.isChecked()

        account = akidump.Account(accountname, name, email, password, date,
                                  comment, copy_email)
        self.db[accountname] = account
        self.clear()

        # Here we update accounts list, hide form and show help tip
        self.add_item(accountname)
        self.clear()
        self.tips['help'].setText("Виберіть акаунт")


class EditAccForm(CreateAcc):
    """
    This is a class which specifies CreateAcc superclass even more.
    We use this class for editing account.
    """
    def __init__(self, db, helpTip):
        """
        This constructor creates the form specifying title parameter, adds `Delete` button
        and changes create buttons text to `Save`, everything else it inherits from CreateAcc
        superclass.
        :param db:
        Database where we will save account once we create one.
        :param helpTip:
        Tip that will be displayed when form is hidden.
        """
        title = 'Редагувати акаунт'
        CreateAcc.__init__(self, title, db, helpTip)
        self.createButton.setText('Зберегти')
        self.deleteButton = QPushButton('Видалити')
        self.deleteButton.clicked.connect(self.delete)
        self.buttonsLayout.insertWidget(1, self.deleteButton)

    def validateName(self, event):
        """
        This method validates whether name entered in the field and is it unique (but if
        the name didn't changed it's okay!).
        """
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
        """
        This method deletes account showing confirmation dialog.
        """
        # Here we iterate through all windows and when we find one that matches our name
        # we stop loop.
        for win in self.windows:
            if win.name == self.name:
                break

        # Then we show confirmation dialog.
        action = QMessageBox.warning(win,
                                     'Увага!',
                                     'Ви певні що хочете видалити акаунт '
                                     '<i><b>{}</b></i>'.format(
                                         self.account.account),
                                     buttons=QMessageBox.No | QMessageBox.Yes,
                                     defaultButton=QMessageBox.No)

        # If users answer is `Yes` we delete account
        if action == QMessageBox.Yes:
            del self.db[self.account.account]

            # and we delete it form accounts list
            self.remove_item(self.account.account)
            self.clear()

            # if database is empty now, we update help tip
            if not getAkiList(self.db):
                self.tips['help'].setText(HELP_TIP_ACCS)

    def setAcc(self, index):
        """
        This method sets all account values to all form fields,
        when user chose to edit an account.
        :param index:
        the index of the account being chosen, it stores account name.
        """
        # to avoid errors
        if not index:
            return

        # Here we saving name of the old account and set all the fields values
        account = index.data()
        self.old_account = account
        self.account = self.db[account]
        self.accountInput.setText(account)
        self.nameInput.setText(self.account.name)
        self.emailInput.setText(self.account.email)
        password = self.account.password.decode()
        self.passField.passInput.setText(password)
        self.passRepeatField.passInput.setText(password)

        day, month, year = [int(d) for d in self.account.date.split('.')]
        self.dateInput.setDate(QDate(year, month, day))

        self.commentInput.setText(self.account.comment)
        hide(self.forms, self.tips)
        self.show()

    def create(self, event):
        """
        This method more logically would be to name as `save` but it called `create` due to
        compatibility with superclass.
        This method called when user presses `Save` button.
        It deletes old account and replaces it with new one created from data that user entered
        in form.
        """
        # Here we get all values from all fields
        accountname = self.accountInput.text()
        name = self.nameInput.text()
        email = self.emailInput.text()
        password = self.passField.passInput.text().encode()
        date = self.dateInput.text()
        comment = self.commentInput.toPlainText()
        copy_email = self.email_radio.isChecked()

        # and here we create new account and also delete the old one
        account = akidump.Account(accountname, name, email, password, date,
                                  comment, copy_email)
        del self.db[self.old_account]
        self.db[accountname] = account
        self.clear()

        # here we update accounts list and clear the edit account form
        self.remove_item(self.old_account)
        self.add_item(accountname)
        self.clear()


class ShowAccForm(QWidget):
    """
    This class is a form that shows account information,
    such as password, e-mail, date of birth etc.
    """
    def __init__(self, db, parent=None):
        """
        This is a constructor of the form, it creates all widgets (mostly labels).
        :param db:
        database that contains given account.
        :param parent:
        parent of the form
        """
        QWidget.__init__(self, parent)
        self.hide()
        self.db = db

        self.account = QLabel()
        self.name = QLabel()
        self.email = QLabel()
        self.password = QLabel()
        self.date = QLabel()
        self.mouse_copy = QLabel()
        self.comment = QTextEdit()
        self.comment.setReadOnly(True)

        # Here we make all label selectable so user can select their text and copy it if he wants
        # Also we set appropriate cursor for labels.
        for label in (self.account, self.name, self.email, self.password,
                      self.date, self.comment):
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            label.setCursor(QCursor(Qt.IBeamCursor))

        # Tip about fast copying feature
        self.copyTip = Tip('Ви можете натиснути гарячі клавіші Ctrl+C\n'
                           'аби скопіювати пароль і e-mail одразу.')

        # her we add every form widget to layout
        layout = QVBoxLayout()
        layout.addWidget(self.account)
        layout.addWidget(self.name)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.date)
        layout.addWidget(self.mouse_copy)
        layout.addWidget(self.copyTip)
        layout.addWidget(self.comment)
        self.setLayout(layout)

    def setAcc(self, index):
        """
        This method changes content of the form accordingly to given account index
        :param index:
        index of the account
        """
        accountname = index.data()
        account = self.db[accountname]

        self.account.setText('Акаунт: ' + account.account)
        self.name.setText("Ім'я: " + account.name)
        self.email.setText('E-mail: ' + account.email)
        self.password.setText('Пароль: ' + account.password.decode())
        self.date.setText('Дата: ' + account.date)
        self.comment.setText('Коментарій: ' + account.comment)

        mouse_copy = 'e-mail' if account.copy_email else 'username'
        self.mouse_copy.setText(f'До мишиного буферу копіюється: {mouse_copy}')

    def copyAcc(self):
        """
        This method is called when user presses Ctrl+C or through menu: File -> Copy.
        It copies e-mail or username to mouse buffer, depending on `copy_email`
        setting of account, and password to clipboard.
        """
        # to copy password
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.password.text().replace('Пароль: ', ''))

        # we need this to know what will be copied to mouseboard
        mouse_copy = self.mouse_copy.text().replace(
            "До мишиного буферу копіюється: ", '')

        # and here we check if mouse_copy contains `e-mail` then we have to copy e-mail
        if mouse_copy == 'e-mail':
            email = self.email.text().replace('E-mail: ', '')
            os.system(f'echo {email} | xclip')
        else:
            # we copy username to mouseboard
            username = self.name.text().replace("Ім'я: ", '')
            os.system(f'echo {username} | xclip')
