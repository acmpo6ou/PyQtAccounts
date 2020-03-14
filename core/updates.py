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
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import git
import widgets
from const import *

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
    if DEBUG:
        commits = repo.iter_commits('dev..origin/dev')
    else:
        commits = repo.iter_commits('master..origin/master')
    res = []
    for commit in commits:
        res.append(commit.message)
    return res

class Updating(QObject):
    progress = pyqtSignal(int)
    result = pyqtSignal(int)

    import git
    class Progress(git.remote.RemoteProgress):
        def __init__(self, progress):
            git.remote.RemoteProgress.__init__(self)
            self.progress = progress

        def update(self, op_code, cur_count, max_count=None, message=''):
            progress = cur_count * 100 / max_count
            self.progress.emit(progress)

    def run(self):
        repo = git.Repo('../')
        repo.git.fetch(progress=self.Progress(self.progress))
        repo.git.pull()

class UpdatingWindow(QWidget):
    def __init__(self, parent):
        print('here')
        QWidget.__init__(self, parent=parent)
        self.setWindowTitle('Оновлення')
        self.progress = QProgressBar()
        self.errors = widgets.Errors()

        self.thread = QThread()
        self.updating = Updating()
        self.updating.moveToThread(self.thread)
        self.updating.result.connect(self.result)
        self.updating.progress.connect(self.update_progress)
        self.thread.started.connect(self.updating.run)
        self.thread.start()

    def update_progress(self, progress):
        self.progress.setValue(progress)

    def result(self, res):
        self.errors.setText('')
        if res:
            self.errors.setText('Помилка підключення! Перевірте мережеве з\'єднання.')
            self.errors.show()
        else:
            self.hide()
            QMessageBox.information('Оновлення', 'Успішно оновлено!')

class UpdatesAvailable(QWidget):
    def __init__(self, parent):
        super().__init__()
        repo = git.Repo('../')
        self.setParent(parent)
        self.setWindowTitle('Доступно нове оновлення')
        self.setWindowFlags(Qt.Dialog)
        self.resize(1000, 500)
        self.show()

        self.title = widgets.Title('<h3>Доступно нове оновлення</h3>')
        self.title.setMinimumWidth(800)
        self.icon = QLabel()
        self.icon.setPixmap(QPixmap('../img/update-available.svg'))

        header = QHBoxLayout()
        header.addWidget(self.icon)
        header.addWidget(self.title)

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
        layout.addLayout(header)
        layout.addWidget(self.text)
        layout.addWidget(self.changelogLabel)
        layout.addLayout(buttonsLayout)
        self.setLayout(layout)

    def applyUpdate(self):
        self.hide()
        self.updating = UpdatingWindow(self.parent())
