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
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

reqs_list = ['git', 'pip3']
reqs_pip = ['cryptography', 'git'] # git is GitPython module

class Reqs:
    def __init__(self):
        self.cant_install = []
        self.to_install = []
        self.installed = []

        for req in reqs_list:
            if os.system('which ' + req):
                self.cant_install.append(req)
            else:
                self.installed.append(req)

        for req in reqs_pip:
            try:
                __import__(req)
            except ImportError:
                self.to_install.append(req)
            else:
                self.installed.append(req)

class ReqsList(QListView):
    def __init__(self, reqs):
        QListView.__init__(self)

        installed = QIcon('img/installed.svg')
        not_installed = QIcon('img/not_installed.svg')
        self.model = QStandardItemModel()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for req in reqs.installed:
            item = QStandardItem(installed, req)
            self.model.appendRow(item)

        for req in reqs.to_install:
            item = QStandardItem(not_installed, req)
            self.model.appendRow(item)

        for req in reqs.cant_install:
            item = QStandardItem(not_installed, req)
            self.model.appendRow(item)

        self.setModel(self.model)

class ReqsTips(QTextEdit):
    def __init__(self, reqs):
        QTextEdit.__init__(self)
        self.setReadOnly(True)

        if not (reqs.cant_install or reqs.to_install):
            tips = '<p style="color: #37FF91;">Всі залежності встановленно!</p>'
        else:
            tips = ''

        if reqs.cant_install:
            tips += '''Бедь-ласка встановіть пакети <i><b>{0}</b></i> 
            самостійно. 
            Для їх встановлення потрібні адміністратора. Введіть в терміналі таку команду:
            <b>sudo apt install {0}</b>'''.format(' '.join([req for req in
                                                   reqs.cant_install]))

        if reqs.to_install:
            tips += '''Пакети {} ми можемо встановити для вас, для цього 
            натисніть кнопку "Встановити". Але спершу не забудьте перевірити 
            наявність пакету <i><b>pip3</b></i>!'''.format(', '.join([req for
                                                                      req in
                                                             reqs.to_install]))

        self.setText(tips)

class Errors(QTextEdit):
    def __init__(self):
        QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.hide()
        self.setTextColor(QColor('#f26666'))

class Title(QLabel):
    def __init__(self, text=''):
        QLabel.__init__(self, '<h4>{}</h4>'.format(text))
        self.setAlignment(Qt.AlignHCenter)

class InstallationWizard(QWizard):
    def __init__(self, parent=None):
        super(InstallationWizard, self).__init__(parent)
        self.addPage(WelcomePage(self))
        self.addPage(RequirementsPage(self))
        self.addPage(InitPage(self))
        self.setWindowTitle("PyQtAccounts - Installation Wizard")
        self.resize(640,480)

class WelcomePage(QWizardPage):
    def __init__(self, parent=None):
        super(WelcomePage, self).__init__(parent)
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap('img/icon.svg'))

        self.title = Title('<pre>Вітаємо у майстрі встановлення\n PyQtAccounts!</pre>')
        self.text = QLabel('<pre><br>Ми допоможемо вам пройти всі кроки \n'
                           'встановлення.</pre>')

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.text)
        self.setLayout(layout)

class PipInstall(QObject):
    result = pyqtSignal(int, str)
    def __init__(self, reqs):
        QObject.__init__(self)
        self.reqs = reqs

    def run(self):
        for req in self.reqs.to_install:
            res = os.system('pip3 install ' + req.replace('git', 'GitPython'))
            self.result.emit(res, req)

class RequirementsPage(QWizardPage):
    def __init__(self, parent=None):
        super(RequirementsPage, self).__init__(parent)
        self.title = Title('Залежності')
        self.text = QLabel('<pre>PyQtAccounts вимагає наявності\n'
                           'певних пакетів. Ось перелік тих які\n'
                           'встановлені, або не встановленні у вас:</pre>')
        reqs = Reqs()
        self.reqs = reqs
        self.reqsList = ReqsList(reqs)
        self.reqsTips = ReqsTips(reqs)
        self.errors = Errors()

        installation = QHBoxLayout()
        self.installLabel = QLabel('Інсталяція...')
        self.installProgress = QProgressBar()
        installation.addWidget(self.installLabel)
        installation.addWidget(self.installProgress)
        self.installLabel.hide()
        self.installProgress.hide()
        self.progress = 0

        self.installButton = QPushButton("Встановити")
        self.installButton.clicked.connect(self.install)
        if not len(reqs.to_install):
            self.installButton.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.text)
        layout.addWidget(self.reqsList)
        layout.addWidget(self.reqsTips)
        layout.addWidget(self.errors)
        layout.addLayout(installation)
        layout.addWidget(self.installButton)
        self.setLayout(layout)

    def install(self, event):
        self.errors.setText('')

        if not 'pip3' in self.reqs.installed:
            self.errors.setText('Встановіть пакет pip3!')
            return

        self.thread = QThread()
        self.install = PipInstall(self.reqs)
        self.install.moveToThread(self.thread)
        self.install.result.connect(self.install_progress)
        self.thread.started.connect(self.install.run)
        self.thread.start()

    def install_progress(self, res, req):
        self.progress += 100 / len(self.reqs.to_install)
        self.installProgress.setValue(self.progress)

        if res:
            text = self.errors.toPlainText()
            self.errors.setText(text + 'Не вдалося встановити ' + req + '\n')
            self.errors.show()
            return

        if self.progress >= 100:
            self.installLabel.setText('<p style="color: ;">Встановлено!</p>')

class InitPage(QWizardPage):
    def __init__(self, parent=None):
        super(InitPage, self).__init__(parent)
        self.title = Title('Ініціалізація')

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        self.setLayout(layout)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wizard = InstallationWizard()
    wizard.show()
    sys.exit(app.exec_())