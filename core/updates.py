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

from utils import Title


def time_for_updates():
    settings = QSettings('PyTools', 'PyQtAccounts')
    frequency = settings.value('updates/frequency', 'always')

    if frequency == 'always':
        return True
    else:
        last_checked = settings.value('updates/last', None)
        current = QDate.currentDate()

        if not last_checked or last_checked.addDays(frequency.toInt()) <= current:
            settings.setValue('updates/last', current)
            return True
        else:
            return False

def getChangeLog(repo):
    commits = repo.iter_commits('master..origin/master')
    res = []
    for commit in commits:
        res.append(commit.message)
    return res

class UpdatesAvailable(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.show()
        self.setWindowTitle('Доступно нове оновлення')
        self.title = Title('Доступно нове оновлення')
        tip = "Доступно нове оновлення PyQtAccounts.\n" \
              "Після оновлення програма перезапуститься.\n" \
              "Переконайтеся що ви зберігли всі зміни до ваших баз данних перед оновленням.\n"
        self.text = QLabel(tip)
        changelog = '<h4>Що нового:</h4><ul>'
        for change in getChangeLog(repo):
            changelog += '<li>{}</li>\n'.format(change)
        changelog += '</ul>'
        self.changelogLabel = QLabel(changelog)

        self.laterButton = QPushButton('Пізніше')
        self.updateButton = QPushButton('Оновити')
        self.laterButton.clicked.connect(self.hide)
        self.updateButton.clicked.connect(self.applyUpdate)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.laterButton)
        buttonsLayout.addWidget(self.updateButton)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.text)
        layout.addWidget(self.changelogLabel)
        layout.addLayout(buttonsLayout)
        self.setLayout(layout)