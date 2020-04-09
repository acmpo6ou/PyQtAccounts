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
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Testing stuff
try:
    from core.testutils import QWidget
except ImportError:
    pass

reqs_list = ('git', 'pip3', 'xclip')
reqs_pip = ('setuptools', 'cryptography', 'gitpython', 'pyshortcuts')


class Reqs:
    def __init__(self):
        self.cant_install = []
        self.to_install = []
        self.installed = []

        for req in reqs_list:
            if os.system('which ' + req):
                self.cant_install.append(req.replace('pip3', 'python3-pip'))
            else:
                self.installed.append(req)

        for req in reqs_pip:
            try:
                __import__(req.replace('gitpython', 'git'))
            except ImportError:
                self.to_install.append(req)
            else:
                self.installed.append(req)


class ReqsList(QListView):
    def __init__(self, reqs):
        QListView.__init__(self)

        installed = QIcon('/usr/share/icons/Humanity/actions/48/gtk-yes.svg')
        not_installed = QIcon('/usr/share/icons/Humanity/actions/128/stock_not.svg')
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
            tips += '''<p>Будь-ласка встановіть пакети <i><b>{0}</b></i> 
            самостійно.</p>
            <p>Для їх встановлення потрібні права адміністратора.</p>
            <p>Введіть в терміналі таку команду:</p>
            <p><b>sudo apt install {0}</b></p>'''.format(
                ' '.join([req for req in reqs.cant_install]))

        if reqs.to_install:
            tips += '''<p>Пакети <i><b>{}</b></i> ми можемо встановити для вас, для цього 
            натисніть кнопку "Встановити".</p>
            <p>Але спершу не забудьте перевірити наявність пакету 
            <i><b>pip3</b></i>!</p>'''.format(
                ', '.join([req for req in reqs.to_install]))

        self.setHtml(tips)


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

        self.initPage = InitPage(self)
        self.addPage(self.initPage)
        finishPage = FinishPage(self)
        finishPage._parent = self
        self.addPage(finishPage)

        self.setWindowTitle("PyQtAccounts - Installation Wizard")
        self.resize(600, 600)


class WelcomePage(QWizardPage):
    def __init__(self, parent=None):
        super(WelcomePage, self).__init__(parent)
        self.setPixmap(QWizard.WatermarkPixmap,
                       QPixmap('/usr/share/icons/Mint-X/mimetypes/96/application-pgp-keys.svg'))

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
            res = os.system('pip3 install ' + req)
            self.result.emit(res, req)


class RequirementsPage(QWizardPage):
    def __init__(self, parent=None):
        super(RequirementsPage, self).__init__(parent)
        self._thread = None
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
        self.errors.hide()

        if not 'pip3' in self.reqs.installed:
            self.errors.show()
            self.errors.setText('Встановіть пакет pip3!')
            return

        self.installButton.setEnabled(False)

        if self._thread and not self._thread.isFinished():
            self._thread.exit()

        thread = QThread(parent=self)
        self.install = PipInstall(self.reqs)
        self.install.moveToThread(thread)
        self.install.result.connect(self.install_progress)
        thread.started.connect(self.install.run)
        thread.start()
        self.installLabel.show()
        self.installProgress.show()

        self._thread = thread

    def install_progress(self, res, req):
        self.progress += 100 / len(self.reqs.to_install)

        if res:
            text = self.errors.toPlainText()
            self.errors.setText(text + 'Не вдалося встановити ' + req + '\n')
            self.errors.show()
            return

        self.installProgress.setValue(self.progress)

        reqs = Reqs()
        self.layout().removeWidget(self.reqsList)
        self.reqsList = ReqsList(reqs)
        self.layout().insertWidget(2, self.reqsList)

        if self.progress >= 100:
            self.installLabel.setText('<p style="color: #37FF91;">Встановлено!</p>')
            self.reqsTips.hide()

        self.completeChanged.emit()

    def isComplete(self):
        reqs = Reqs()
        if not (reqs.cant_install or reqs.to_install):
            return True
        else:
            return False

class Initialize(QObject):
    result = pyqtSignal(int)
    progress = pyqtSignal(int)

    def __init__(self, folder):
        QObject.__init__(self)
        self.folder = folder + '/PyQtAccounts'

    def run(self):
        import git

        class Progress(git.remote.RemoteProgress):
            def __init__(self, progress):
                git.remote.RemoteProgress.__init__(self)
                self.progress = progress

            def update(self, op_code, cur_count, max_count=None, message=''):
                progress = cur_count * 100 / max_count
                self.progress.emit(progress)

        try:
            git.Repo.clone_from('https://github.com/Acmpo6ou/PyQtAccounts', self.folder,
                                progress=Progress(self.progress))
        except:
            self.result.emit(1)
        else:
            self.result.emit(0)


class InitPage(QWizardPage):
    def __init__(self, parent=None):
        super(InitPage, self).__init__(parent)
        self._thread = None
        self.folder = os.getenv('HOME')
        self.title = Title('Ініціалізація')
        self.errors = Errors()
        self.progress = QProgressBar()

        self.initLabel = QLabel('Виберіть папку в яку ви хочете встановити PyQtAccounts:')
        self.browseButton = QPushButton('Browse...')
        self.browseButton.clicked.connect(self.browse)
        self.browseLabel = QLabel(self.folder)

        browseLayout = QHBoxLayout()
        browseLayout.addWidget(self.browseButton)
        browseLayout.addWidget(self.browseLabel)
        self.initButton = QPushButton('Ініціалізувати')
        self.initButton.clicked.connect(self.init)

        desktopIcon = QHBoxLayout()
        self.desktopCheckbox = QCheckBox()
        self.desktopCheckbox.setChecked(True)
        desktopLabel = QLabel('додати ярлик запуску на робочий стіл')
        desktopIcon.addWidget(self.desktopCheckbox)
        desktopIcon.addWidget(desktopLabel)

        menuIcon = QHBoxLayout()
        self.menuCheckbox = QCheckBox()
        self.menuCheckbox.setChecked(True)
        menuLabel = QLabel('додати пункт запуску в меню')
        menuIcon.addWidget(self.menuCheckbox)
        menuIcon.addWidget(menuLabel)

        icons = QVBoxLayout()
        icons.addLayout(desktopIcon)
        icons.addLayout(menuIcon)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.initLabel)
        layout.addLayout(browseLayout)
        layout.addWidget(self.progress)
        layout.addWidget(self.initButton)
        layout.addLayout(icons)
        layout.addWidget(self.errors)
        self.setLayout(layout)

    def browse(self):
        folder = QFileDialog.getExistingDirectory(wizard, 'Installation directory',
                                                  self.folder, QFileDialog.ShowDirsOnly)
        if folder:
            self.folder = folder
            self.browseLabel.setText(folder)

    def isComplete(self):
        if self.progress.value() == 100:
            return True
        else:
            return False

    def init(self):
        if 'PyQtAccounts' in os.listdir(self.folder):
            self.progress.setValue(100)

        if self.progress.value() != 100:

            if self._thread and not self._thread.isFinished():
                self._thread.exit()

            thread = QThread(parent=self)
            self.init = Initialize(self.folder)
            self.init.moveToThread(thread)
            self.init.result.connect(self.check_result)
            self.init.progress.connect(self.init_progress)
            thread.started.connect(self.init.run)
            thread.start()

            self._thread = thread

    def check_result(self, res):
        self.errors.hide()
        self.errors.setText('')

        if res:
            self.errors.show()
            self.errors.setText('Помилка ініціалізації!\n'
                                "Відсутнє мережеве з'єднання, або відмовлено у доступі на "
                                "запис у папку інсталяції.")

    def init_progress(self, progress):
        self.progress.setValue(progress)

        if progress >= 100:
            self.completeChanged.emit()

class FinishPage(QWizardPage):
    def __init__(self, parent=None):
        super(FinishPage, self).__init__(parent)

        self.title = Title('Finish')
        self.text = QLabel('Успішно установлено PyQtAccounts!')

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.text)
        self.setLayout(layout)

    def initializePage(self):
        initPage = self._parent.initPage
        cwd = initPage.folder + '/PyQtAccounts/'
        desktop = initPage.desktopCheckbox.isChecked()
        startmenu = initPage.menuCheckbox.isChecked()
        from pyshortcuts import make_shortcut

        if desktop or startmenu:
            make_shortcut(
                name='PyQtAccounts',
                script=cwd + '/run.sh',
                description='Simple account database manager.',
                icon=cwd+'/img/icon.svg',
                terminal=False,
                desktop=desktop,
                startmenu=startmenu,
                executable='/bin/bash'
            )

            # fixing .ico icon issue
            home = os.getenv('HOME')
            if desktop:
                desktop = open(home+'/Desktop/PyQtAccounts.desktop').read()
                with open(home+'/Desktop/PyQtAccounts.desktop', 'w') as file:
                    file.write(desktop.replace('.ico', ''))

            if startmenu:
                menu = open(home+'/.local/share/applications/PyQtAccounts.desktop').read()
                with open(home+'/.local/share/applications/PyQtAccounts.desktop', 'w') as file:
                    file.write(menu.replace('.ico', ''))

        run = open(cwd+'run.sh').read()
        run = run.replace('cd .', f'cd {cwd}')
        run = run.replace('export PYTHONPATH="$PYTHONPATH:./"',
                          f'export PYTHONPATH="$PYTHONPATH:{cwd}"')
        with open(cwd+'run.sh', 'w') as runfile:
            runfile.write(run)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
    *{
        font-family: Ubuntu, Ubuntu Mono;
        font-size: 24px;
    }
    ''')
    app.setWindowIcon(QIcon('/usr/share/icons/Mint-X/mimetypes/96/application-pgp-keys.svg'))
    wizard = InstallationWizard()
    wizard.show()
    sys.exit(app.exec_())