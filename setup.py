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
reqs_pip = ['cryptography', 'GitPython']

class Reqs:
    def __init__(self):
        self.cant_install = []
        self.to_install = []
        self.installed = []

        for req in reqs_list:
            if os.system(req):
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

class ReqsList(QTextEdit):
    def __init__(self, reqs):
        QTextEdit.__init__(self)
        self.setReadOnly(True)

class ReqsTips(QTextEdit):
    def __init__(self, reqs):
        QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setTextColor(QColor('#37FF91'))
        self.setText('Всі залежності встановленно!')

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
        self.addPage(RequairmentsPage(self))
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

class RequairmentsPage(QWizardPage):
    def __init__(self, parent=None):
        super(RequairmentsPage, self).__init__(parent)
        self.title = Title('Залежності')
        self.text = QLabel('<pre>PyQtAccounts вимагає наявності\n'
                           'певних пакетів. Ось перелік тих які\n'
                           'встановлені, або не встановленні у вас:</pre>')
        reqs = Reqs()
        self.reqs = reqs
        self.reqsList = ReqsList(reqs)
        self.reqsTips = ReqsTips(reqs)
        self.errors = Errors()
        self.installButton = QPushButton("Встановити")
        self.installButton.clicked.connect(self.install)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.text)
        layout.addWidget(self.reqsList)
        layout.addWidget(self.reqsTips)
        layout.addWidget(self.errors)
        layout.addWidget(self.installButton)
        self.setLayout(layout)

    def install(self, event):
        for req in self.reqs.to_install:
            res = os.system('pip3 install ' + req)
            if res:
                text = self.errors.text()
                self.errors.setText(text + 'Не вдалося встановити ' + req)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wizard = InstallationWizard()
    wizard.show()
    sys.exit(app.exec_())