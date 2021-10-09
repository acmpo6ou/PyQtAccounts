#!/usr/bin/env python3

#  Copyright (c) 2020-2021. Bohdan Kolvakh
#  This file is part of PyQtAccounts.
#
#  PyQtAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyQtAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.
#
#  PyQtAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyQtAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.

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

import core.akidump as akidump
from core.const import *
from core.forms import *
from core.widgets import *

# This is mostly for testing
SRC_DIR = core.const.SRC_DIR


class CreateAccount(CreateForm):
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
        nameTip = ""  # there is no name characters validation for account names.
        passTip = (
            "Якщо ви не хочете придумувати пароль ви можете\n"
            "натиснути кнопку 'Згенерувати', аби згенерувати його."
        )
        nameError = "Акаунт з таким іменем вже існує!"
        CreateForm.__init__(
            self, title, namePlaceholder, nameError, nameTip, passTip, helpTip, parent
        )
        self.hide()
        self.db = db

        # Account create form needs more fields
        # here we create label and field for
        # account name (account name and nickname aren't same things!), e-mail, date of birth
        # and comment to account.
        self.accountLabel = QLabel("Акаунт:")
        self.accountInput = QLineEdit()
        self.accountInput.setPlaceholderText("назва акаунту")
        self.accountInput.textChanged.connect(self.validateName)

        self.nameInput.setPlaceholderText("ваше ім'я або нікнейм")
        self.nameInput.textChanged.disconnect()

        self.emailLabel = QLabel("E-mail:")
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText("введіть e-mail акаунта")

        # here we have radio buttons that will define what will be copied to
        # mouseboard `email` or `username` when user performs copy operation
        self.copy_label = QLabel(
            "Тут ви можете вибрати що буде копіюватися до\n" "мишиного буферу:"
        )
        self.username_radio = QRadioButton("Username", self)
        self.email_radio = QRadioButton("E-mail", self)

        # e-mail will be copied to mouseboard by default
        self.email_radio.setChecked(True)

        copyLayout = QHBoxLayout()
        copyLayout.addWidget(self.email_radio)
        copyLayout.addWidget(self.username_radio)

        self.attach_label = QLabel("Додати файли:")
        self.attach_list = QListView()
        self.attach_list.setModel(QStandardItemModel())
        self.attach_list.pathmap = {}
        self.attach_list.clicked.connect(self.file_selected)
        self.attach_list.selected = None
        self.attach_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.attach_file_button = QPushButton()
        self.attach_file_button.clicked.connect(self.attach_file)
        self.attach_file_button.setIcon(QIcon("img/list-add.png"))
        self.attach_file_button.setIconSize(QSize(22, 22))

        self.detach_button = QPushButton()
        self.detach_button.clicked.connect(self.detach_file)
        self.detach_button.setIcon(QIcon("img/list-remove.svg"))
        self.detach_button.setIconSize(QSize(22, 22))

        attachButtonsLayout = QVBoxLayout()
        attachButtonsLayout.addWidget(self.attach_file_button)
        attachButtonsLayout.addWidget(self.detach_button)

        attachLayout = QHBoxLayout()
        attachLayout.addWidget(self.attach_list)
        attachLayout.addLayout(attachButtonsLayout)

        self.dateLabel = QLabel("Дата народження:")
        self.dateInput = QDateEdit()
        self.dateInput.setDisplayFormat("dd.MM.yyyy")
        dateLayout = QHBoxLayout()
        dateLayout.addWidget(self.dateLabel)
        dateLayout.addWidget(self.dateInput)

        self.commentLabel = QLabel("Коментарій:")
        self.commentInput = QTextEdit()
        self.commentInput.setPlaceholderText("Введіть коментарій")
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

        model = self.attach_list.model()
        model.removeRows(0, model.rowCount())

        for i in range(self.errors.layout().count()):
            err = self.errors.layout().itemAt(i).widget()
            err.hide()

        self.createButton.setEnabled(False)
        self.createButton.setStyleSheet(APPLY_BUTTON_DISABLED)
        self.createButton.setStyleSheet(APPLY_BUTTON_DISABLED)
        self.hide()
        self.helpTip.show()

    def attach_file(self):  # sourcery skip: use-assigned-variable
        """
        This method is invoked when user presses on attache file button.
        """
        # here we get path of file to attach and then we obtain its name
        home = os.getenv("HOME")
        path = QFileDialog.getOpenFileName(
            self.parent(), "Виберіть файл для закріплення", home
        )[0]
        # if user presses `Cancel` in chose file dialog then path will be empty
        # string and in this case there is no need to create empty file name in
        # attach list neither to create mapping for it
        if not path:
            return

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
                self.parent(),
                "Увага!",
                "Файл з таким іменем вже існує, замінити?",
                buttons=QMessageBox.Yes | QMessageBox.No,
            )

        # there is no need to add another file name to list if it already
        # exists, so here we add it only when it isn't exist yet
        else:
            # here we add attached file to attach list
            item = QStandardItem(QIcon("img/mail-attachment.svg"), name)
            self.attach_list.model().appendRow(item)

        # here we check `answer` variable if it is `Yes` then we create mapping
        # from file name to its path
        if answer == QMessageBox.Yes:
            # here we create mapping of attached file name and its path
            self.attach_list.pathmap[name] = path

    def file_selected(self, name):
        """
        This method is invoked when user clicks on file name in the attach files
        list.
        """
        # here we save selected file name, so later if user wants to delete
        # selected file we will be able to do it
        self.attach_list.selected = name.data()

    def detach_file(self):
        """
        We use this method to detach file from attach file list.
        """
        selected = self.attach_list.selected

        # here we check does user has any file selected, because if not we can't
        # determine which file he wants to detach
        if not selected:
            # if there is no file selected yet and user presses detach
            # button we simply do nothing
            return

        # here we show confirmation dialog in case if user pressed detach button
        # by accident
        answer = QMessageBox.warning(
            self.parent(),
            "Увага!",
            "Ви впевнені що хочете відкріпити " f"<b>{selected}</b>?",
            buttons=QMessageBox.Yes | QMessageBox.No,
        )

        if answer == QMessageBox.Yes:
            # if users answer is `Yes` then we delete appropriate file mapping
            del self.attach_list.pathmap[selected]

            # and we remove file name from attach list
            model = self.attach_list.model()
            filename = model.findItems(selected)[0]
            model.removeRow(filename.row())


class CreateAccountForm(CreateAccount):
    """
    This is a class which specifies CreateAccount superclass even more.
    We use this class for creating account.
    """

    def __init__(self, db, helpTip, parent=None):
        """
        This constructor creates the form specifying title parameter, everything else it
        inherits from CreateAccount superclass.
        :param db:
        Database where we will save account once we create one.
        :param helpTip:
        Tip that will be displayed when form is hidden.
        :param parent:
        The parent of the form.
        """
        title = "Створити акаунт"
        CreateAccount.__init__(self, title, db, helpTip, parent)

    def validateName(self, event):
        """
        This method validates whether name entered in the field and is it unique.
        """
        name = self.accountInput.text()
        if name in getAkiList(self.db):
            self.nameError.show()
            self.createButton.setEnabled(False)
            self.createButton.setStyleSheet(APPLY_BUTTON_DISABLED)
            self.validate["name"] = False
        elif name == "":
            self.nameFilledError.show()
            self.createButton.setEnabled(False)
            self.createButton.setStyleSheet(APPLY_BUTTON_DISABLED)
            self.validate["name"] = False
        else:
            self.validate["name"] = True
            self.nameError.hide()
            self.nameFilledError.hide()

        if self.validate["pass"] and self.validate["name"]:
            self.createButton.setEnabled(True)
            self.createButton.setStyleSheet(APPLY_BUTTON)

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
        comment = self.commentInput.toPlainText().replace("\n", "\n\n")
        copy_email = self.email_radio.isChecked()

        attached_files = {}
        # here we iterate trough all files specified in attach_list's `pathmap`
        for name in self.attach_list.pathmap:
            # here we obtain file path
            path = self.attach_list.pathmap[name]
            # then we open and read the file using mapping associated with `name`
            with open(path, "rb") as f:
                file = f.read()
            # finally we save opened file content to dict and associate it with
            # appropriate file name
            attached_files[name] = file

        account = akidump.Account(
            accountname,
            name,
            email,
            password,
            date,
            comment,
            copy_email,
            attached_files,
        )
        self.db[accountname] = account
        self.clear()

        # Here we update accounts list, hide form and show help tip
        self.add_item(accountname)
        self.clear()
        self.tips["help"].setText("Виберіть акаунт")

        # also here we update completion of the form because we created new
        # account
        set_form_completers(self, self.db)
        set_form_completers(self.forms["edit"], self.db)


class EditAccountForm(CreateAccount):
    """
    This is a class which specifies CreateAccount superclass even more.
    We use this class for editing account.
    """

    def __init__(self, db, helpTip):
        """
        This constructor creates the form specifying title parameter, adds `Delete` button
        and changes create buttons text to `Save`, everything else it inherits from CreateAccount
        superclass.
        :param db:
        Database where we will save account once we create one.
        :param helpTip:
        Tip that will be displayed when form is hidden.
        """
        title = "Редагувати акаунт"
        CreateAccount.__init__(self, title, db, helpTip)
        self.createButton.setText("Зберегти")
        self.deleteButton = GTKButton(DELETE_BUTTON, "Видалити")
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
            self.createButton.setStyleSheet(APPLY_BUTTON_DISABLED)
            self.validate["name"] = False
        elif name == "":
            self.nameFilledError.show()
            self.createButton.setEnabled(False)
            self.createButton.setStyleSheet(APPLY_BUTTON_DISABLED)
            self.validate["name"] = False
        else:
            self.validate["name"] = True
            self.nameError.hide()
            self.nameFilledError.hide()

        if self.validate["pass"] and self.validate["name"]:
            self.createButton.setEnabled(True)
            self.createButton.setStyleSheet(APPLY_BUTTON)

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
        action = QMessageBox.warning(
            win,
            "Увага!",
            "Ви певні що хочете видалити акаунт "
            "<i><b>{}</b></i>".format(self.account.account),
            buttons=QMessageBox.No | QMessageBox.Yes,
            defaultButton=QMessageBox.No,
        )

        # If users answer is `Yes` we delete account
        if action == QMessageBox.Yes:
            del self.db[self.account.account]

            # and we delete it form accounts list
            self.remove_item(self.account.account)
            self.clear()

            # if database is empty now, we update help tip
            if not getAkiList(self.db):
                self.tips["help"].setText(HELP_TIP_ACCS)

    def set_account(self, index):
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

        day, month, year = [int(d) for d in self.account.date.split(".")]
        self.dateInput.setDate(QDate(year, month, day))

        self.commentInput.setText(self.account.comment)

        self.email_radio.setChecked(self.account.copy_email)
        self.username_radio.setChecked(not self.account.copy_email)

        self.attach_model = QStandardItemModel()
        for file in self.account.attached_files:
            item = QStandardItem(QIcon("img/mail-attachment.svg"), file)
            self.attach_model.appendRow(item)

            # all files that are already attached will map to None
            self.attach_list.pathmap[file] = None
        self.attach_list.setModel(self.attach_model)

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

        # here we obtain attached files
        attached_files = {}
        for file in self.attach_list.pathmap:
            path = self.attach_list.pathmap[file]
            if not path:
                # if file maps to None then we already loaded this file, so we
                # use it from old account
                old_account = self.db[self.old_account]
                attached_files[file] = old_account.attached_files[file]
            else:
                # else, file maps to path then we load file using this path
                attached_files[file] = open(path, "rb").read()

        # and here we create new account and also delete the old one
        account = akidump.Account(
            accountname,
            name,
            email,
            password,
            date,
            comment,
            copy_email,
            attached_files,
        )
        del self.db[self.old_account]
        self.db[accountname] = account
        self.clear()

        # here we update accounts list and clear the edit account form
        self.remove_item(self.old_account)
        self.add_item(accountname)
        self.clear()

        # also here we update completion of the form because we edited account
        set_form_completers(self, self.db)
        set_form_completers(self.forms["create"], self.db)


class ShowAccountForm(QWidget):
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

        # display password only when checkbox is checked
        self.password = QCheckBox("Пароль: " + "•" * 32)
        self.password.setChecked(False)
        self.password.toggled.connect(self.passwordChecked)
        self.password.setStyleSheet(
            "font-family: Ubuntu Mono, Ubuntu;"
            "font-size: 24px;"
            "outline: none;"
            "border: none;"
        )

        self.date = QLabel()
        self.mouse_copy = QLabel()
        self.comment = QTextEdit()
        self.comment.setReadOnly(True)

        self.attached_files = QListView()
        self.attached_model = QStandardItemModel()
        self.attached_files.setModel(self.attached_model)
        self.attached_files.clicked.connect(self.download_file)
        self.attached_files.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Here we make all label selectable so user can select their text and copy it if he wants to
        # Also we set appropriate cursor for labels.
        for label in (
            self.account,
            self.name,
            self.email,
            self.date,
            self.comment,
        ):
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            label.setCursor(QCursor(Qt.IBeamCursor))

        # Tip about fast copying feature
        self.copyTip = Tip(
            "Ви можете натиснути гарячі клавіші Ctrl+C\nаби скопіювати e-mail."
        )

        # her we add every form widget to layout
        layout = QVBoxLayout()
        layout.addWidget(self.account)
        layout.addWidget(self.name)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.date)
        layout.addWidget(self.mouse_copy)
        layout.addWidget(self.attached_files)
        layout.addWidget(self.copyTip)
        layout.addWidget(self.comment)
        self.setLayout(layout)

    def passwordChecked(self, event):
        """
        Display password if password checkbox is checked and hide it if checkbox is unchecked.
        """
        if self.password.isChecked():
            password = self._account.password.decode().replace("&", "&&")  # escape &
            self.password.setText(f"Пароль: {password}")
        else:
            self.password.setText("Пароль: " + "•" * 32)

    def set_account(self, index):
        """
        This method changes content of the form accordingly to given account index
        :param index:
        index of the account
        """
        accountname = index.data()
        account = self.db[accountname]
        self._account = account

        self.account.setText("Акаунт: " + account.account)
        self.name.setText("Ім'я: " + account.name)
        self.email.setText("E-mail: " + account.email)
        self.password.setChecked(False)
        self.date.setText("Дата: " + account.date)
        self.comment.setText("Коментарій: " + account.comment)

        mouse_copy = "e-mail" if account.copy_email else "username"
        self.mouse_copy.setText(f"Копіюється: {mouse_copy}")

        # to clear the model
        self.attached_model = QStandardItemModel()
        self.attached_files.setModel(self.attached_model)
        for file in account.attached_files:
            item = QStandardItem(QIcon("img/mail-attachment.svg"), file)
            self.attached_model.appendRow(item)

    def copy_email(self):
        """
        This method is called when user presses Ctrl+C or through menu: File -> Copy.
        It copies e-mail or username depending on `copy_email` property of account.
        """
        account = self._account
        data = account.email if account.copy_email else account.name
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(data)

        self.window().windows[0].password = account.password.decode()

    def download_file(self, file):
        """
        This method is invoked when user chose file from attached files list to
        download it.
        """
        # here we show save file dialog, so user can chose where to save
        # attached file
        home = os.getenv("HOME")
        path = QFileDialog.getSaveFileName(
            self.parent(), "Зберегти закріплений файл", f"{home}/{file.data()}"
        )[0]

        # if user presses `Cancel` in the dialog then we do nothing
        if not path:
            return

        try:
            saved_file = open(path, "wb")
            saved_file.write(self._account.attached_files[file.data()])
        except Exception:
            QMessageBox.critical(self.parent(), "Помилка!", "Операція не успішна!")
        else:
            QMessageBox.information(self.parent(), "Успіх!", "Операція успішна!")
        finally:
            saved_file.close()
