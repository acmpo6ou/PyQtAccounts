#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh Bogdan
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
This module provides all classes that represent windows or other big elements of program.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from core.testutils import QWidget

import os

from core.widgets import *
from core.updates import *
import core.const
from core.utils import *
from core.getaki import *
import tarfile
from core.account_forms import *


def export(name, path, parent):
    """
    This function called when user exports database
    :param name:
    name of the database being exported
    :param path:
    path where database will be exported
    :param parent:
    parent for messages
    """
    try:
        # here we create tar file that contains database files
        # tarfile structure:
        # src
        # ├── <database name>.bin
        # └── <database name>.db

        file = tarfile.open(path, 'w')
        file.add(f'{core.const.SRC_DIR}/{name}.db')
        file.add(f'{core.const.SRC_DIR}/{name}.bin')
        file.close()
    except RecursionError:  # to prevent fatal python error
        raise
    except Exception:
        # if there are some errors we show error message
        QMessageBox.critical(parent, 'Помилка!', 'Експорт бази данних '
                             'завершився невдачею.')
    else:
        # if not we show success message
        QMessageBox.information(
            parent, 'Експорт', 'Успішно експортовано базу '
            'данних <i><b>{}</b></i>'.format(name))


def _import(path, parent):
    """
    This function called when user tries to import database
    :param path:
    path to database tarfile
    :param parent:
    parent for messages
    """
    try:
        # here we try to extract files from tarfile archive to program directory
        tar = tarfile.open(path)
        for i, file in enumerate(tar.getmembers()):
            # here we check integrity of the tarfile, if there are any database file missing
            # we throw an exception
            if '.db' not in file.name and '.bin' not in file.name:
                raise TypeError('Невірний файл!')

        # here we obtain name of the database through its files names
        name = os.path.basename(file.name).replace('.db',
                                                   '').replace('.bin', '')

        # here we check whether number of files in archive is 2, if not we throw exception,
        # because file might be corrupted
        if i != 1:
            raise TypeError('Невірний файл!')
        tar.extractall(core.const.SRC_PATH)

        # and here we update database list
        model = parent.dbs.list.model
        _list = parent.dbs.list

        for item in model.findItems(name):
            model.removeRow(item.row())

        item = QStandardItem(_list.icon, name)
        model.appendRow(item)
        model.sort(0)
        parent.dbs.tips['help'].setText("Виберіть базу данних")
    except RecursionError:  # to prevent fatal python error
        raise
    except Exception as err:
        # if there are some errors we show error message
        QMessageBox.critical(parent, 'Помилка!', str(err))
    else:
        # if not we show success message
        QMessageBox.information(
            parent, 'Імпорт',
            'Успішно імпортовано базу данних <i><b>{}</b></i>'.format(name))


class Panel(QHBoxLayout):
    """
    This class is a panel for buttons, it has 2 buttons: `add` and `edit`.
    """
    def __init__(self, add, edit):
        """
        This is constructor of the panel.
        :param add:
        function that called when user presses `add` button
        :param edit:
        function that called when user presses `edit` button
        """
        QHBoxLayout.__init__(self)

        # this is `add` button it calls add function when user presses it.
        self.addButton = QPushButton()
        self.addButton.setIcon(QIcon('img/list-add.png'))
        self.addButton.setIconSize(QSize(22, 22))
        self.addButton.clicked.connect(add)

        # this is `edit` button it calls edit function when user presses it.
        self.editButton = QPushButton()
        self.editButton.setIcon(QIcon('img/edit.svg'))
        self.editButton.setIconSize(QSize(22, 22))
        self.editButton.clicked.connect(edit)

        self.addWidget(self.addButton)
        self.addWidget(self.editButton)


class List(QListView):
    """
    This class is list of accounts or databases.
    """
    def __init__(self, list, icon, forms, windows, tips, select):
        """
        This is constructor of the list.
        :param list:
        list of items that will be shown at the list widget.
        :param icon:
        icon that will be shown near every item of the list.
        :param forms:
        list of all application forms.
        :param windows:
        list of all application windows.
        :param tips:
        list of all application tips.
        :param select:
        method that called when user chose item from list.
        """
        QListView.__init__(self)
        self.forms = forms
        self.windows = windows
        self.tips = tips
        self.select = select
        self.index = None

        # here we create list model and set this model to listview widget.
        self.icon = QIcon(icon)
        self.model = QStandardItemModel()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for name in list:
            item = QStandardItem(self.icon, name)
            self.model.appendRow(item)
        self.setModel(self.model)

        self.clicked.connect(self.selected)

    def selected(self, index):
        """
        Method that called when user chose item in the list.
        :param index:
        index that represents chosen item.
        """
        self.select(self, index)


def selectDb(obj, index):
    """
    Method that called when user chose database in the list.
    :param obj:
    Dbs instance
    :param index:
    index that represents chosen database.
    """
    obj.index = index

    # here we iterate through all windows of the application and if window of database being
    # chosen already exists we show message saying that database is already opened.
    for win in obj.windows:
        if index.data() == win.name:
            hide(obj.forms, obj.tips)
            obj.tips['already-open'].show()
            return

    # if there is no database window opened yet we show open database form.
    obj.forms['open'].setDb(index)
    hide(obj.forms, obj.tips)
    obj.forms['open'].show()
    obj.forms['open'].passField.passInput.setFocus()


class Dbs(QWidget):
    """
    This class is a container for everything that about databases.
    """
    def __init__(self, forms, windows, tips):
        """
        This is constructor that creates database panel and list.
        :param forms:
        list of all application forms.
        :param windows:
        list of all application windows.
        :param tips:
        list of all application tips.
        """
        super().__init__()
        self.forms = forms
        self.windows = windows
        self.tips = tips

        # here we create database panel and list
        self.panel = Panel(self.add, self.edit)
        self.list = List(sorted(getDbList()), 'img/icon.svg', forms, windows,
                         tips, selectDb)

        # and here we assign some stuff to database forms, such as database list, database model,
        # tips and forms
        self.forms['edit'].model = self.list.model
        self.forms['edit'].list = self.list
        self.forms['edit'].tips = tips
        self.forms['edit'].forms = forms

        self.forms['create'].list = self.list
        self.forms['create'].tips = tips

        layout = QVBoxLayout()
        layout.addLayout(self.panel)
        layout.addWidget(self.list)
        self.setLayout(layout)

    def add(self):
        """
        This method called when user presses `add` button on the panel.
        It shows create database form.
        """
        hide(self.forms, self.tips)
        self.forms['create'].show()

    def edit(self):
        """
        This method called when user presses `edit` button on the panel.
        It shows edit database form.
        """
        # self.list.index is index that represents currently chosen database at the list
        self.forms['edit'].setDb(self.list.index)


def select_account(obj, index):
    """
    Method that called when user chose account in the list.
    :param obj:
    Accs instance
    :param index:
    index that represents chosen account.
    """
    # here we set account that chosen to show account form and we show this form
    obj.index = index
    obj.forms['show'].set_account(index)
    hide(obj.forms, obj.tips)
    obj.forms['show'].show()


class Accs(QWidget):
    """
    This class is a container for everything that about accounts.
    """
    def __init__(self, name, db, forms, tips, windows):
        """
        This is constructor that creates account panel and list.
        :param name:
        name of the database that contains all accounts.
        :param db:
        database dict that contains all accounts.
        :param forms:
        list of all application forms.
        :param windows:
        list of all application windows.
        :param tips:
        list of all application tips.
        """
        QWidget.__init__(self)
        self.forms = forms
        self.windows = windows
        self.tips = tips
        self.db = db

        # here we create accounts panel and list
        self.panel = Panel(self.add, self.edit)
        self.list = List(sorted(getAkiList(db)), 'img/account.png', forms,
                         windows, tips, select_account)

        # and here we assign some stuff to account forms, such as account list, database name
        # tips, forms and windows
        self.forms['create'].list = self.list
        self.forms['create'].tips = tips

        self.forms['show'].tips = tips
        self.forms['show'].forms = forms

        self.forms['edit'].forms = forms
        self.forms['edit'].tips = tips
        self.forms['edit'].list = self.list
        self.forms['edit'].windows = windows
        self.forms['edit'].name = name

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.panel)
        self.layout.addWidget(self.list)
        self.setLayout(self.layout)

    def add(self):
        """
        This method called when user presses `add` button on the panel.
        It shows create account form.
        """
        hide(self.forms, self.tips)
        self.forms['create'].show()

    def edit(self):
        """
        This method called when user presses `edit` button on the panel.
        It shows edit account form.
        """
        # self.list.index is index that represents currently chosen account at the list
        self.forms['edit'].set_account(self.list.index)


class MenuBar(QMenuBar):
    """
    This class is superclass for other menu bars (i.e. for main window and database windows menu
    bars).
    """
    def __init__(self, parent):
        """
        This is a base constructor for menu bars.
        :param parent:
        window of the menu bar.
        """
        QMenuBar.__init__(self, parent)
        self.parent = parent
        self._thread = None

        # here we define every action that all menu bars are using
        self.File = self.addMenu('&File')
        self.quit = self.File.addAction(QIcon('img/quit.svg'), '&Quit',
                                        parent.close, QKeySequence('Ctrl+Q'))

        self.Edit = self.addMenu('&Edit')
        self.Edit.addAction(QIcon('img/preferences.png'), '&Preferences',
                            self.preferences, QKeySequence('Ctrl+P'))

        self.Updates = self.addMenu('&Updates')
        self.Updates.addAction(QIcon('img/update-available.svg'),
                               '&Check for updates', self.checkForUpdates)
        self.Updates.addAction(QIcon('img/changelog.svg'), '&View changelog',
                               lambda: ShowChangelog(parent))

        self.Help = self.addMenu('&Help')  # first is the main window
        self.Help.addAction(QIcon('img/info.png'), 'About',
                            parent.windows[0].about.exec, QKeySequence('F1'))
        self.Help.addAction(QIcon('img/qt5.png'), 'PyQt5',
                            lambda: QMessageBox.aboutQt(parent))

    def preferences(self):
        """
        This method called when users goes to menu: Edit -> Preferences.
        It shows settings dialog.
        """
        self.parent.settings.show()

    def checkForUpdates(self):
        """
        This method called when user goes to menu: Updates -> Check for updates.
        It runs process of checking for updates in another thread.
        """
        def mess(parent, changes, log):
            if changes:
                # if there are updates we show updates available dialog.
                res = UpdatesAvailable(parent, log)
            else:
                # else we show message saying that there are no updates.
                res = QMessageBox.information(parent, "Оновлення",
                                              "Немає оновленнь.")
            # here we assign resulting dialog to main window, so we can test those dialogs.
            parent.res = res

        # here we create process and start in another thread
        thread = QThread(parent=self)
        updating = Updating()
        updating.moveToThread(thread)
        updating.result.connect(
            lambda changes, log: mess(self.parent, changes, log))
        thread.started.connect(updating.run)
        thread.start()

        self._thread = thread
        self.updating = updating


class AppMenuBar(MenuBar):
    """
    This class inherits from MenuBar, and it specifies actions that will be in the main window
    menu bar.
    """
    def __init__(self, parent):
        """
        This is the constructor of menu bar, it adds new actions to menu bar that already created
        by base constructor.
        :param parent:
        main application window
        """
        MenuBar.__init__(self, parent)

        # here we add actions specific to databases
        self.new = QAction(QIcon('img/list-add.svg'), '&New database...')
        self.new.triggered.connect(parent.dbs.panel.addButton.click)
        self.new.setShortcut(QKeySequence('Ctrl+N'))

        self._import = QAction(QIcon('img/import.png'), '&Import database...')
        self._import.triggered.connect(self.Import)
        self._import.setShortcut(QKeySequence('Ctrl+I'))

        self.export = QAction(QIcon('img/export.png'), '&Export database...')
        self.export.triggered.connect(self.Export)
        self.export.setShortcut(QKeySequence('Ctrl+E'))

        self.File.insertAction(self.quit, self.new)
        self.File.insertAction(self.quit, self._import)
        self.File.insertAction(self.quit, self.export)

    def Import(self):
        """
        This method called when user goes to menu: File -> Import database...
        It asks user about database tarfile that he would like to import then it
        calls export function with all parameters specified.
        """
        # by default we show home directory at the `Chose directory dialog`
        home = os.getenv('HOME')
        path = QFileDialog.getOpenFileName(caption='Імпортувати базу данних',
                                           filter='Tarball (*.tar)',
                                           directory=home)[0]
        # if user pressed `cancel` button we abort export, if not we call _import function
        if path:
            _import(path, self.parent)

    def Export(self):
        """
        This method called when user goes to menu: File -> Export database...
        It asks user about folder where he would like to extract his database then it calls export
        function with all parameters specified.
        """
        try:
            # here we obtain name of chosen database user wants to export
            name = self.parent.dbs.list.index.data()
        except AttributeError:
            # if user doesn't chose database we show warning saying that he must chose database
            # before export
            tips = self.parent.dbs.tips
            forms = self.parent.dbs.forms
            hide(tips, forms)
            tips['export'].show()
            return

        # by default we show home directory at the `Chose directory dialog`
        home = os.getenv('HOME')
        path = QFileDialog.getSaveFileName(caption='Експортувати базу данних',
                                           filter='Tarball (*.tar)',
                                           directory=f'{home}/{name}.tar')[0]

        # if user pressed `cancel` button we abort export
        if not path:
            return
        # if user typed name of tarfile without .tad extension we add it to name.
        if not path.endswith('.tar'):
            path += '.tar'
        # then we call export function
        export(name, path, self.parent)


class DbMenuBar(MenuBar):
    """
    This class is a menu bar for database window.
    """
    def __init__(self, parent):
        """
        This is the constructor of menu bar, it adds new actions to menu bar that already created
        by base constructor.
        :param parent:
        database window
        """
        MenuBar.__init__(self, parent)

        # here we add actions specific to accounts
        self.new = QAction(QIcon('img/list-add.svg'), '&New account...')
        self.new.triggered.connect(parent.accs.panel.addButton.click)
        self.new.setShortcut(QKeySequence('Ctrl+N'))

        self.save = QAction(QIcon('img/save.png'), '&Save')
        self.save.triggered.connect(self.Save)
        self.save.setShortcut(QKeySequence('Ctrl+S'))

        self.copy = QAction(QIcon('img/copy.png'), '&Copy')
        self.copy.triggered.connect(parent.accs.forms['show'].copy_account)
        self.copy.setShortcut(QKeySequence('Ctrl+C'))

        self.File.insertAction(self.quit, self.new)
        self.File.insertAction(self.quit, self.save)
        self.File.insertAction(self.quit, self.copy)

    def Save(self):
        """
        This method called when user goes to menu: File -> Save or press Ctrl+S.
        It saves database on the disk.
        """
        # here we obtain database dict, name and password
        db = self.parent.db
        name = self.parent.name
        password = self.parent.password

        # then we encrypt that database and save it to file
        token = encryptDatabase(name, db, password)
        dbfile = f'{core.const.SRC_DIR}/{name}.db'
        with open(dbfile, 'wb') as file:
            file.write(token)


class DbWindow(QMainWindow):
    """
    This class is a database window.
    """
    def __init__(self, windows, name, db, password):
        """
        This is a constructor of window, it initializes all forms, tips and other widgets.
        :param windows:
        list of all application windows.
        :param name:
        name of the database
        :param db:
        dict of the database
        :param password:
        password of the database
        """
        QMainWindow.__init__(self)
        self.resize(1000, 500)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('img/account.png'))
        self.name = name
        self.db = db
        self.password = password
        self.windows = windows

        # this attribute represents whether we would show close confirmation dialog on close or
        # not, if user has changed something in database we will, if not we wont annoy user with
        # message.
        self.ask = True

        # here we create account forms an tips
        helpTip = HelpTip(HELP_TIP_ACCS)
        if getAkiList(db):
            helpTip = HelpTip("Виберіть акаунт")
        helpTip.show()

        create_account_form = CreateAccountForm(self.db, helpTip)
        edit_account_form = EditAccountForm(self.db, helpTip)
        show_account_form = ShowAccountForm(self.db)

        # here we create set of all emails of accounts of given database, so we
        # can use them for email completion
        lst = set()
        for account in db:
            a = db[account]
            lst.add(a.email)

        completer = QCompleter(lst)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        create_account_form.emailInput.setCompleter(completer)

        tips = {'help': helpTip}
        forms = {
            'create': create_account_form,
            'edit': edit_account_form,
            'show': show_account_form
        }

        splitter = QSplitter()
        for tip in tips:
            splitter.addWidget(tips[tip])

        for form in forms:
            splitter.addWidget(forms[form])

        # and here we create accounts panel and list by instantiating Accs class
        accs = Accs(name, db, forms, tips, windows)
        accs.setMaximumWidth(200)
        splitter.addWidget(accs)
        accs.forms = forms
        accs.tips = tips
        self.accs = accs

        # here we create menu bar for window
        self.menu = DbMenuBar(self)
        self.setMenuBar(self.menu)

        self.setCentralWidget(splitter)
        self.show()

    def closeEvent(self, event):
        """
        This method called when user closes database window.
        """
        # here we open database that is currently on disk
        name = self.name
        password = self.password
        db = openDatabase(name, password)

        # then we compare database on disk and database in memory, if they differ it means that
        # user changed database, so we will ask him about unsaved changes
        if isEqual(db, self.db) and self.ask:
            self.windows.remove(self)
            return

        # here we asking user does he sure about exit
        if self.ask:
            action = QMessageBox.question(
                self, 'Увага!', 'Ви певні що хочете вийти?\n'
                'Усі незбережені зміни буде втрачено!\n'
                'Натисніть Ctrl+S аби зберегти зміни.')
        else:
            action = QMessageBox.Yes

        # if he answers `Yes` (i.e. he is sure) we close window
        if action == QMessageBox.Yes:
            self.windows.remove(self)
        else:
            # else we ignore event and abort window close
            event.ignore()


class About(QDialog):
    """
    This class is an About dialog, it appears when user goes to menu: Help -> About or presses F1.
    This dialog provides all helpful information about PyQtAccounts such as license, credits etc.
    """
    def __init__(self):
        QDialog.__init__(self)
        self.resize(300, 500)

        # here we create dialog title with icon
        self.title = QLabel('<h3>About PyQtAccounts</h3>')
        self.title.setMinimumWidth(800)
        self.icon = QLabel()
        icon = QPixmap('img/icon.svg')
        self.icon.setPixmap(icon)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.icon)
        self.titleLayout.addWidget(self.title)

        # and here we obtain current programs version to use it in about section of dialog
        version = str(
            getVersion())[1:]  # to prevent the appearance of the `v` symbol

        # this is `about` label, it provides information about PyQtAccounts
        self.about = \
            '''<pre>


            Author: Kolvakh Bogdan
            Version {}
            <b>PyQtAccounts</b> — is simple account database manager made 
            using Python 3 and PyQt5.
            You can easily manage your accounts and store them safely in 
            encrypted databases.
            The interface of PyQtAccounts is common and easy to use.
            PyQtAccounts is completely free and open source project (see our license).
            Also here you can see PyQtAccounts source code <a 
            href='https://github.com/Acmpo6ou/PyQtAccounts' 
            style='color: #3791ff;'>GitHub</a>
            <span style='color: #37FF91;'>According to our privacy policy you must know 
            that we do not saving or sharing any private data such as your 
            account passwords or databases.
            </span>
            (c) Copyright 2020 Kolvakh Bogdan
            </pre>'''.format(version)
        self.aboutLabel = QLabel(self.about)
        self.aboutLabel.setOpenExternalLinks(True)

        # here we load license from COPYING file and set it as text to license label
        self.license = \
            '<pre>{}</pre>'.format(open('COPYING').read())
        self.licenseText = QTextEdit(self.license)
        self.licenseText.setReadOnly(True)

        # here we load credits from COPYING file and set it as text to credits label
        self.credits = \
            '<pre>{}</pre>'.format(open('CREDITS').read())
        self.creditsText = QLabel(self.credits)

        # here we create tab widget, so each label has its own tab
        self.content = QTabWidget()
        self.content.addTab(self.aboutLabel, 'About')
        self.content.addTab(self.licenseText, 'License')
        self.content.addTab(self.creditsText, 'Credits')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addLayout(self.titleLayout)
        self.layout.addWidget(self.content)


class Settings(QDialog):
    """
    This is settings dialog it appears when uer goes to menu: Edit -> Preferences or presses
    Ctrl+P.
    """
    def __init__(self, parent):
        """
        This is constructor of the dialog.
        :param parent:
        main window
        """
        QDialog.__init__(self, parent)
        self.setWindowTitle('Settings - PyQtAccounts')
        # here we open user settings that store in his home directory
        self.settings = QSettings(f'{os.getenv("HOME")}/PyTools',
                                  'PyQtAccounts')

        # here we create title and label for main database feature
        # feature when we auto select main database on startup (database that user chose as main).
        header = QLabel('<h4>Швидке введення</h4>')
        label = QLabel('Головна база данних:')

        # here we create checkbox to switch database feature and combobox to chose main database.
        checkbox = QCheckBox(
            'Показувати форму для введення пароля одразу після запуску')
        checkbox.setChecked(
            self.settings.value('advanced/is_main_db', False, type=bool))

        dbs = QComboBox()
        dbs.setModel(parent.dbs.list.model)
        dbs.model = parent.dbs.list.model
        main_db = self.settings.value('advanced/main_db', '', type=str)
        if main_db:
            dbs.setCurrentText(main_db)
        elif 'main' in getDbList():
            # by default current is main database
            dbs.setCurrentText('main')

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(label)
        mainLayout.addWidget(dbs)

        mainDbLayout = QVBoxLayout()
        mainDbLayout.addWidget(header)
        mainDbLayout.addWidget(checkbox)
        mainDbLayout.addLayout(mainLayout)

        mainDbLayout.checkbox = checkbox
        mainDbLayout.dbs = dbs
        self.mainDbLayout = mainDbLayout

        self.saveButton = QPushButton('Зберегти')
        self.saveButton.clicked.connect(self.save)
        self.closeButton = QPushButton('Скасувати')
        self.closeButton.clicked.connect(self.hide)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.closeButton)
        buttonsLayout.addWidget(self.saveButton)

        layout = QVBoxLayout()
        layout.addLayout(mainDbLayout)
        layout.addLayout(buttonsLayout)
        self.setLayout(layout)

    def save(self):
        """
        This method called when user presses `Save` button.
        """
        # here we save all settings to file and hide our dialog.
        is_main_db = self.mainDbLayout.checkbox.isChecked()
        self.settings.setValue('advanced/is_main_db', is_main_db)
        main_db = self.mainDbLayout.dbs.currentText()
        self.settings.setValue('advanced/main_db', main_db)
        self.hide()
