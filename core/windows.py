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

import os

from core.widgets import *
from core.updates import *
from core.const import *
from core.utils import *
from core.getaki import *
import tarfile
from core.account_forms import *


def export(name, path, parent):
    try:
        file = tarfile.open(path, 'w')
        file.add('src/{}.db'.format(name))
        file.add('src/{}.bin'.format(name))
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
            if not ('.db' in file.name and '.bin' in file.name):
                raise TypeError('Невірний файл!')

        name = os.path.basename(file.name).replace('.db', '').replace('.bin', '')

        if i != 1:
            raise TypeError('Невірний файл!')
        tar.extractall('src/')

        model = parent.dbs.list.model
        list = parent.dbs.list

        for item in model.findItems(name):
            model.removeRow(item.row())

        item = QStandardItem(list.icon, name)
        model.appendRow(item)
        model.sort(0)
        parent.dbs.tips['help'].setText("Виберіть базу данних")

    except Exception as err:
        QMessageBox.critical(parent, 'Помилка!', str(err))
    else:
        QMessageBox.information(parent, 'Імпорт',
                                'Успішно імпортовано базу данних <i><b>{}</b></i>'.format(name))


class Panel(QHBoxLayout):
    def __init__(self, add, edit):
        QHBoxLayout.__init__(self)

        self.addButton = QPushButton()
        self.addButton.setIcon(QIcon('img/list-add.png'))
        self.addButton.setIconSize(QSize(22, 22))
        self.addButton.clicked.connect(add)

        self.editButton = QPushButton()
        self.editButton.setIcon(QIcon('img/edit.svg'))
        self.editButton.setIconSize(QSize(22, 22))
        self.editButton.clicked.connect(edit)

        self.addWidget(self.addButton)
        self.addWidget(self.editButton)


class List(QListView):
    def __init__(self, list, icon, forms, windows, tips, select):
        QListView.__init__(self)
        self.forms = forms
        self.windows = windows
        self.tips = tips
        self.select = select
        self.index = None

        self.icon = QIcon(icon)
        self.model = QStandardItemModel()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for name in list:
            item = QStandardItem(self.icon, name)
            self.model.appendRow(item)
        self.setModel(self.model)

        self.clicked.connect(self.selected)

    def selected(self, index):
        self.select(self, index)


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


class Dbs(QWidget):
    def __init__(self, forms, windows, tips):
        super().__init__()
        self.forms = forms
        self.windows = windows
        self.tips = tips

        self.panel = Panel(self.add, self.edit)
        self.list = List(sorted(getDbList()), 'img/icon.svg', forms, windows,
                         tips, selectDb)

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
        hide(self.forms, self.tips)
        self.forms['create'].show()

    def edit(self):
        self.forms['edit'].setDb(self.list.index)


def selectAcc(obj, index):
    obj.index = index

    obj.forms['show'].setAcc(index)
    hide(obj.forms, obj.tips)
    obj.forms['show'].show()


class Accs(QWidget):
    def __init__(self, name, db, forms, tips, windows):
        QWidget.__init__(self)
        self.forms = forms
        self.windows = windows
        self.tips = tips
        self.db = db

        self.panel = Panel(self.add, self.edit)
        self.list = List(sorted(getAkiList(db)), 'img/account.png', forms,
                         windows, tips, selectAcc)

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
        hide(self.forms, self.tips)
        self.forms['create'].show()

    def edit(self):
        self.forms['edit'].setAcc(self.list.index)


class MenuBar(QMenuBar):
    def __init__(self, parent):
        QMenuBar.__init__(self, parent)
        self.parent = parent
        self._thread = None

        self.File = self.addMenu('&File')
        self.quit = self.File.addAction(QIcon('img/quit.svg'), '&Quit',
                                        parent.close, QKeySequence('Ctrl+Q'))

        self.Edit = self.addMenu('&Edit')
        self.Edit.addAction(QIcon('img/preferences.png'), '&Preferences',
                            self.preferences, QKeySequence('Ctrl+P'))

        self.Updates = self.addMenu('&Updates')
        self.Updates.addAction(QIcon('img/update-available.svg'), '&Check for updates',
                               self.checkForUpdates)
        self.Updates.addAction(QIcon('img/changelog.svg'), '&View changelog',
                               lambda: ShowChangelog(parent))

        self.Help = self.addMenu('&Help')                     # first is the main window
        self.Help.addAction(QIcon('img/info.png'), 'About', parent.windows[0].about.exec,
                            QKeySequence('F1'))
        self.Help.addAction(QIcon('img/qt5.png'), 'PyQt5',
                            lambda: QMessageBox.aboutQt(parent))

    def preferences(self):
        self.parent.settings.show()

    def checkForUpdates(self):
        def mess(parent, changes, log):
            if changes:
                res = UpdatesAvailable(parent, log)
            else:
                res = QMessageBox.information(parent, "Оновлення", "Немає оновленнь.")
            parent.res = res

        thread = QThread(parent=self)
        updating = Updating()
        updating.moveToThread(thread)
        updating.result.connect(lambda changes, log: mess(self.parent, changes, log))
        thread.started.connect(updating.run)
        thread.start()

        if self._thread and not self._thread.isFinished():
            self._thread.exit()
        self._thread = thread
        self.updating = updating


class AppMenuBar(MenuBar):
    def __init__(self, parent):
        MenuBar.__init__(self, parent)

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
        home = os.getenv('HOME')
        path = QFileDialog.getOpenFileName(
            caption='Імпортувати базу данних',
            filter='Tarball (*.tar)',
            directory=home)[0]
        if path:
            _import(path, self.parent)

    def Export(self):
        try:
            name = self.parent.dbs.list.index.data()
        except AttributeError:
            tips = self.parent.dbs.tips
            forms = self.parent.dbs.forms
            hide(tips, forms)
            tips['export'].show()
            return

        home = os.getenv('HOME')
        path = QFileDialog.getSaveFileName(
            caption='Експортувати базу данних',
            filter='Tarball (*.tar)',
            directory=f'{home}/{name}.tar')[0]
        if not path:
            return
        if not path.endswith('.tar'):
            path += '.tar'
        export(name, path, self.parent)


class DbMenuBar(MenuBar):
    def __init__(self, parent):
        MenuBar.__init__(self, parent)

        self.new = QAction(QIcon('img/list-add.svg'), '&New account...')
        self.new.triggered.connect(parent.accs.panel.addButton.click)
        self.new.setShortcut(QKeySequence('Ctrl+N'))

        self.save = QAction(QIcon('img/save.png'), '&Save')
        self.save.triggered.connect(self.Save)
        self.save.setShortcut(QKeySequence('Ctrl+S'))

        self.copy = QAction(QIcon('img/copy.png'), '&Copy')
        self.copy.triggered.connect(parent.accs.forms['show'].copyAcc)
        self.copy.setShortcut(QKeySequence('Ctrl+C'))

        self.File.insertAction(self.quit, self.new)
        self.File.insertAction(self.quit, self.save)
        self.File.insertAction(self.quit, self.copy)

    def Save(self):
        db = self.parent.db
        name = self.parent.name
        password = self.parent.password
        token = encryptDatabase(name, db, password)

        dbfile = 'src/' + name + '.db'
        with open(dbfile, 'wb') as file:
            file.write(token)


class DbWindow(QMainWindow):
    def __init__(self, windows, name, db, password):
        QMainWindow.__init__(self)
        self.resize(1000, 500)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('img/account.png'))
        self.name = name
        self.windows = windows
        self.ask = True

        self.db = db
        self.password = password

        helpTip = HelpTip(HELP_TIP_ACCS)
        if getAkiList(db):
            helpTip = HelpTip("Виберіть акаунт")
        helpTip.show()

        create_account_form = CreateAccForm(self.db, helpTip)
        edit_account_form = EditAccForm(self.db, helpTip)
        show_account_form = ShowAccForm(self.db)

        tips = {'help': helpTip}
        forms = {'create': create_account_form, 'edit': edit_account_form,
                 'show': show_account_form}

        splitter = QSplitter()
        for tip in tips:
            splitter.addWidget(tips[tip])

        for form in forms:
            splitter.addWidget(forms[form])

        accs = Accs(name, db, forms, tips, windows)
        accs.setMaximumWidth(200)
        splitter.addWidget(accs)
        accs.forms = forms
        accs.tips = tips
        self.accs = accs

        self.menu = DbMenuBar(self)
        self.setMenuBar(self.menu)

        self.setCentralWidget(splitter)
        self.show()

    def closeEvent(self, event):
        name = self.name
        password = self.password
        db = openDatabase(name, password)

        if isEqual(db, self.db) and self.ask:
            self.windows.remove(self)
            return

        if self.ask:
            action = QMessageBox.question(self, 'Увага!',
                                          'Ви певні що хочете вийти?\n'
                                          'Усі незбережені зміни буде втрачено!\n'
                                          'Натисніть Ctrl+S аби зберегти зміни.')
        else:
            action = QMessageBox.Yes

        if action == QMessageBox.Yes:
            self.windows.remove(self)
        else:
            event.ignore()


class About(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(300, 500)

        self.title = QLabel('<h3>About PyQtAccounts</h3>')
        self.title.setMinimumWidth(800)
        self.icon = QLabel()
        icon = QPixmap('img/icon.svg')
        self.icon.setPixmap(icon)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.icon)
        self.titleLayout.addWidget(self.title)

        version = str(getVersion())[1:]  # to prevent the appearance of the `v` symbol

        self.about = \
            '''<pre>


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
            </pre>'''.format(version)
        self.aboutLabel = QLabel(self.about)
        self.aboutLabel.setOpenExternalLinks(True)

        self.license = \
            '<pre>{}</pre>'.format(open('COPYING').read())
        self.licenseText = QTextEdit(self.license)
        self.licenseText.setReadOnly(True)

        self.credits = \
            '<pre>{}</pre>'.format(open('CREDITS').read())
        self.creditsText = QLabel(self.credits)

        self.content = QTabWidget()
        self.content.addTab(self.aboutLabel, 'About')
        self.content.addTab(self.licenseText, 'License')
        self.content.addTab(self.creditsText, 'Credits')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addLayout(self.titleLayout)
        self.layout.addWidget(self.content)


class Settings(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Settings - PyQtAccounts')
        self.settings = QSettings('PyTools', 'PyQtAccounts')

        header = QLabel('<h4>Швидке введення</h4>')
        label = QLabel('Головна база данних:')

        checkbox = QCheckBox('Показувати форму для введення пароля одразу після запуску')
        checkbox.setChecked(self.settings.value('advanced/is_main_db', False, type=bool))

        dbs = QComboBox()
        dbs.addItems(getDbList())
        main_db = self.settings.value('advanced/main_db', '', type=str)
        if main_db:
            dbs.setCurrentText(main_db)
        elif 'main' in getDbList():
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
        is_main_db = self.mainDbLayout.checkbox.isChecked()
        self.settings.setValue('advanced/is_main_db', is_main_db)
        main_db = self.mainDbLayout.dbs.currentText()
        self.settings.setValue('advanced/main_db', main_db)
        self.hide()
