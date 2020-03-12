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

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import glob
import os.path
import os
import genpass
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

class PasswordField(QHBoxLayout):
    def __init__(self, placeholder=''):
        QHBoxLayout.__init__(self)

        self.passInput = QLineEdit()
        self.passInput.setPlaceholderText(placeholder)
        self.passInput.setEchoMode(QLineEdit.Password)

        self.showButton = QPushButton()
        self.showButton.setIcon(QIcon('../img/show.svg'))
        self.showButton.setIconSize(QSize(25, 25))
        self.showButton.clicked.connect(self.toggleShow)

        self.addWidget(self.passInput)
        self.addWidget(self.showButton)

    def toggleShow(self):
        if self.passInput.echoMode() == QLineEdit.Password:
            self.passInput.setEchoMode(QLineEdit.Normal)
            self.showButton.setIcon(QIcon('../img/hide.svg'))
        else:
            self.passInput.setEchoMode(QLineEdit.Password)
            self.showButton.setIcon(QIcon('../img/show.svg'))

class Tip(QLabel):
    def __init__(self, text=''):
        QLabel.__init__(self, text)

        font = QFont('Ubuntu Mono', 18)

        self.setStyleSheet('color: #37FF91;')
        self.setFont(font)


class HelpTip(QLabel):
    def __init__(self, text=''):
        QLabel.__init__(self, text)
        self.setAlignment(Qt.AlignCenter)
        font = QFont('Ubuntu Mono', 18, QFont.StyleItalic)
        self.setFont(font)
        self.hide()

class WarningTip(HelpTip):
    def __init__(self, text=''):
        HelpTip.__init__(self, text)
        self.setStyleSheet('color: #be9117;')
        self.hide()

class Title(QLabel):
    def __init__(self, text=''):
        text = '<b>{}</b>'.format(text)
        QLabel.__init__(self, text)
        self.setAlignment(Qt.AlignHCenter)


class Error(QLabel):
    def __init__(self, text=''):
        QLabel.__init__(self, text)

        font = QFont('Ubuntu Mono', 18)

        self.setStyleSheet('color: #f26666;')
        self.setFont(font)


def validName(name):
    valid = ascii_letters + digits + '.()-_'
    result = ''
    for c in name:
        if c in valid:
            result += c
    return result


class GenPassDialog(QDialog):
    def __init__(self, form):
        QDialog.__init__(self, form.parent())
        self.form = form
        self.setModal(True)
        self.setSizeGripEnabled(True)
        self.setWindowTitle('Згенерувати пароль')
        self.resize(700, 300)

        self.symLabel = QLabel('Довжина пароля: ')
        self.symNum = QSpinBox()
        self.symNum.setMinimum(8)
        self.symNum.setValue(16)
        self.symTip = Tip("Рекомендуємо вибирати число не меншне 16")

        self.symLayout = QHBoxLayout()
        self.symLayout.addWidget(self.symLabel)
        self.symLayout.addWidget(self.symNum)

        self.digitsLabel = QLabel('Цифри')
        self.digitsFlag = QCheckBox()
        self.digitsFlag.setChecked(True)
        self.digitsFlag.name = 'd'
        self.digitsLabel.setBuddy(self.digitsFlag)
        self.lowerLabel = QLabel('Малі англійські букви')
        self.lowerFlag = QCheckBox()
        self.lowerFlag.setChecked(True)
        self.lowerFlag.name = 'l'
        self.lowerLabel.setBuddy(self.lowerFlag)
        self.upperLabel = QLabel('Великі англійські букви')
        self.upperFlag = QCheckBox()
        self.upperFlag.setChecked(True)
        self.upperFlag.name = 'u'
        self.upperLabel.setBuddy(self.upperFlag)
        self.punctuationLabel = QLabel('Знаки пунктуації')
        self.punctuationFlag = QCheckBox()
        self.punctuationFlag.setChecked(True)
        self.punctuationFlag.name = 'p'
        self.punctuationLabel.setBuddy(self.punctuationFlag)

        self.checkGrid = QGridLayout()
        self.checkGrid.addWidget(self.digitsFlag, 0, 0)
        self.checkGrid.addWidget(self.digitsLabel, 0, 1, 1, 10)
        self.checkGrid.addWidget(self.upperFlag, 1, 0)
        self.checkGrid.addWidget(self.upperLabel, 1, 1, 1, 10)
        self.checkGrid.addWidget(self.lowerFlag, 2, 0)
        self.checkGrid.addWidget(self.lowerLabel, 2, 1, 1, 10)
        self.checkGrid.addWidget(self.punctuationFlag, 3, 0)
        self.checkGrid.addWidget(self.punctuationLabel, 3, 1, 1, 10)

        self.includeTip = Tip("Не рекомендуємо змінювати ці параметри,\n"
                              "адже вони можуть вплинути на силу пароля.")

        self.buttonCancel = QPushButton('Скасувати')
        self.buttonGenerate = QPushButton('Згенерувати')
        self.buttonCancel.clicked.connect(self.hide)
        self.buttonGenerate.clicked.connect(self.generate)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.buttonCancel)
        self.buttonsLayout.addWidget(self.buttonGenerate)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.symLayout)
        self.layout.addWidget(self.symTip)
        self.layout.addLayout(self.checkGrid)
        self.layout.addWidget(self.includeTip)
        self.layout.addLayout(self.buttonsLayout)
        self.setLayout(self.layout)

    def generate(self, event):
        symbs = ''
        for box in self.digitsFlag, self.upperFlag, self.lowerFlag, self.punctuationFlag:
            flag = box.isChecked()
            if flag:
                symbs += box.name
        password = genpass.main(symbs, self.symNum.value())
        self.form.passField.passInput.setText(password)
        self.form.passRepeatField.passInput.setText(password)
        self.hide()


class Panel(QHBoxLayout):
    def __init__(self, add, edit):
        QHBoxLayout.__init__(self)

        self.addButton = QPushButton()
        self.addButton.setIcon(QIcon('../img/list-add.png'))
        self.addButton.setIconSize(QSize(22, 22))
        self.addButton.clicked.connect(add)

        self.editButton = QPushButton()
        self.editButton.setIcon(QIcon('../img/edit.svg'))
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


class Dbs(QVBoxLayout):
    def __init__(self, forms, windows, tips):
        QVBoxLayout.__init__(self)
        self.forms = forms
        self.windows = windows
        self.tips = tips

        self.panel = Panel(self.add, self.edit)
        self.list = List(sorted(getDbList()), '../img/icon.svg', forms, windows,
                         tips, selectDb)

        self.forms['edit'].model = self.list.model
        self.forms['edit'].list = self.list
        self.forms['edit'].tips = tips
        self.forms['edit'].forms = forms

        self.forms['create'].list = self.list
        self.forms['create'].tips = tips

        self.addLayout(self.panel)
        self.addWidget(self.list)

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
        self.list = List(sorted(getAkiList(db)), '../img/account.png', forms,
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

class MenuBar(QMenuBar):
    def __init__(self, parent):
        QMenuBar.__init__(self, parent)
        self.parent = parent

        self.File = self.addMenu('&File')
        self.quit = self.File.addAction(QIcon('../img/quit.svg'), '&Quit',
                                       parent.close, QKeySequence('Ctrl+Q'))

        self.Edit = self.addMenu('&Edit')
        self.Edit.addAction(QIcon('../img/preferences.png'), '&Preferences',
                            self.preferences, QKeySequence('Ctrl+P'))

        self.Help = self.addMenu('&Help')
        self.Help.addAction(QIcon('../img/info.png'), 'About', about.exec,
                            QKeySequence('F1'))
        self.Help.addAction(QIcon('../img/qt5.png'), 'PyQt5',
                            lambda: QMessageBox.aboutQt(parent))

    def preferences(self):
        QMessageBox.information(self.parent, 'Preferences',
                                'Вибачте налаштування ще не готові, '
                                'але будуть доступні у пізніших версіях.')

class AppMenuBar(MenuBar):
    def __init__(self, parent):
        MenuBar.__init__(self, parent)

        self.new = QAction(QIcon('../img/list-add.svg'), '&New database...')
        self.new.triggered.connect(parent.dbs.layout().panel.addButton.click)
        self.new.setShortcut(QKeySequence('Ctrl+N'))

        self._import = QAction(QIcon('../img/import.png'), '&Import database...')
        self._import.triggered.connect(self.Import)
        self._import.setShortcut(QKeySequence('Ctrl+I'))

        self.export = QAction(QIcon('../img/export.png'), '&Export database...')
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
        name = self.parent.dbs.layout().list.index
        if name:
            home = os.getenv('HOME')
            path = QFileDialog.getSaveFileName(
                    caption='Експортувати базу данних',
                    filter='Tarball (*.tar)',
                    directory=home)[0]
            if not path:
                return
            if not path.endswith('.tar'):
                path += '.tar'
            export(name, path, self.parent)
        else:
            tips = self.parent.dbs.layout().tips
            forms = self.parent.dbs.layout().forms
            hide(tips, forms)
            tips['export'].show()

class DbMenuBar(MenuBar):
    def __init__(self, parent):
        MenuBar.__init__(self, parent)

        self.new = QAction(QIcon('../img/list-add.svg'), '&New account...')
        self.new.triggered.connect(parent.accs.panel.addButton.click)
        self.new.setShortcut(QKeySequence('Ctrl+N'))

        self.save = QAction(QIcon('../img/save.png'), '&Save')
        self.save.triggered.connect(self.Save)
        self.save.setShortcut(QKeySequence('Ctrl+S'))

        self.copy = QAction(QIcon('../img/copy.png'), '&Copy')
        self.copy.triggered.connect(parent.accs.forms['show'].copyAcc)
        self.copy.setShortcut(QKeySequence('Ctrl+C'))

        self.File.insertAction(self.quit, self.new)
        self.File.insertAction(self.quit, self.save)
        self.File.insertAction(self.quit, self.copy)

    def Save(self):
        db = self.parent.db
        name = self.parent.name
        password = self.parent.password
        encryptDatabase(name, db, password)


class DbWindow(QMainWindow):
    def __init__(self, windows, name, db, password):
        QMainWindow.__init__(self)
        self.resize(1000, 500)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('../img/account.png'))
        self.name = name
        self.windows = windows
        self.ask = True

        self.db = db
        self.password = password

        helpTip = HelpTip(HELP_TIP)
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
        self.accs = accs

        self.menu = DbMenuBar(self)
        self.setMenuBar(self.menu)

        self.setCentralWidget(splitter)
        self.show()

    def closeEvent(self, event):
        if self.ask:
            action = QMessageBox.question(self, 'Увага!',
                'Ви певні що хочете вийти?\n'
                'Усі не збережені зміни буде втрачено!\n'
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
        icon = QPixmap('../img/icon.svg')
        self.icon.setPixmap(icon)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.icon)
        self.titleLayout.addWidget(self.title)

        self.about = \
        '''<pre>
        
        
        Version 1.0.2
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
        </pre>'''
        self.aboutLabel = QLabel(self.about)
        self.aboutLabel.setOpenExternalLinks(True)

        self.license = \
        '''<pre>
        {}
        </pre>'''.format(open('../COPYING').read())
        self.licenseText = QTextEdit(self.license)
        self.licenseText.setReadOnly(True)

        self.credits = \
        '''<pre>{}</pre>'''.format(open('../CREDITS').read())
        self.creditsText = QLabel(self.credits)

        self.content = QTabWidget()
        self.content.addTab(self.aboutLabel, 'About')
        self.content.addTab(self.licenseText, 'License')
        self.content.addTab(self.creditsText, 'Credits')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addLayout(self.titleLayout)
        self.layout.addWidget(self.content)

about = About()