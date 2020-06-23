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
This is a PyQtAccounts installation wizard. It installs all pip program dependencies and initializes
PyQtAccounts, also it creates shortcuts in main menu and on desktop.
"""

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyshortcuts import make_shortcut

# Testing stuff
try:
    from core.testutils import QWidget
except ImportError:
    pass

# this is a lists of program dependencies: system (that we can't install through pip) and pip.
reqs_list = ('git', 'pip3', 'xclip')
reqs_pip = ('setuptools', 'cryptography', 'gitpython', 'pyshortcuts')

# this function is only for testing
testing = lambda *args: None


class Reqs:
    """
    This class stores 3 lists:
    first called `cant_install` - it stores dependencies that we can't install through pip.
    second called `to_install` - those are dependencies that we need to install with pip.
    third called `installed` - those that are already installed.
    """
    def __init__(self):
        """
        This constructor creates all lists.
        """
        self.cant_install = []
        self.to_install = []
        self.installed = []

        # here we iterate through all system dependencies and use `which` shell command
        # to determine whether it exists or not, if not os.system will return nonzero code
        for req in reqs_list:
            if os.system('which ' + req):
                # if `which` can't find dependency it will return nonzero status code, it
                # means that dependency isn't installed so we add it to cant_install list
                self.cant_install.append(req.replace('pip3', 'python3-pip'))
            else:
                # else we add it to installed list
                self.installed.append(req)

        # here we iterate through all pip dependencies and use `__import__` function
        # to determine whether it installed or not, if not __import__ will raise ImportError
        for req in reqs_pip:
            try:
                # this function call is only for testing because we can't mock __import__
                testing(req.replace('gitpython', 'git'))
                # we need to import `git` but it represents `gitpython` package
                __import__(req.replace('gitpython', 'git'))
            except ImportError:
                # if we catch ImportError we add dependency to `to_install` list.
                self.to_install.append(req)
            else:
                # else we add it to installed list
                self.installed.append(req)


class ReqsList(QListView):
    """
    This is a customized QListView widget, it represents list of dependencies.
    Icon near every dependency represents whether it installed or not.
    """
    def __init__(self, reqs):
        QListView.__init__(self)

        # here we create icons and model, also we don't want our list to be editable
        installed = QIcon('/usr/share/icons/Humanity/actions/48/gtk-yes.svg')
        not_installed = QIcon(
            '/usr/share/icons/Humanity/actions/48/stock_not.svg')
        self.model = QStandardItemModel()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # here we iterate through all 3 lists and add them to list model with appropriate icon
        for req in reqs.installed:
            item = QStandardItem(installed, req)
            self.model.appendRow(item)

        for req in reqs.to_install:
            item = QStandardItem(not_installed, req)
            self.model.appendRow(item)

        for req in reqs.cant_install:
            item = QStandardItem(not_installed, req)
            self.model.appendRow(item)

        # then we set model to list
        self.setModel(self.model)


class ReqsTips(QTextEdit):
    """
    This class is customized QTextEdit that will show tips about dependencies, for example how to
    install system and pip dependencies.
    """
    def __init__(self, reqs):
        QTextEdit.__init__(self)
        # we don't want our tips to be editable
        self.setReadOnly(True)

        # if `cant_install` and `to_install` lists are empty then every dependency is satisfied
        # and we show green message saying that all dependencies are installed.
        if not (reqs.cant_install or reqs.to_install):
            tips = '<p style="color: #37FF91;">Всі залежності встановленно!</p>'
        else:
            tips = ''

        # else we iterate through all not installed dependencies (both system and pip)
        # and we add tips for each dependency saying how to install it.
        if reqs.cant_install:
            tips += '''<p>Будь-ласка встановіть пакети <i><b>{0}</b></i> 
            самостійно.</p>
            <p>Для їх встановлення потрібні права адміністратора.</p>
            <p>Введіть в терміналі таку команду:</p>
            <p><b>sudo apt install {0}</b></p>'''.format(' '.join(
                [req for req in reqs.cant_install]))

        if reqs.to_install:
            tips += '''<p>Пакети <i><b>{}</b></i> ми можемо встановити для вас, для цього 
            натисніть кнопку "Встановити".</p>
            <p>Але спершу не забудьте перевірити наявність пакету 
            <i><b>pip3</b></i>!</p>'''.format(', '.join(
                [req for req in reqs.to_install]))

        self.setHtml(tips)


class Errors(QTextEdit):
    """
    This class is a error messages QTextEdit, it has red color of its text.
    """
    def __init__(self):
        QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.hide()
        self.setTextColor(QColor('#f26666'))


class Title(QLabel):
    """
    This class is a simple QLabel that wraps its text to <h4> tag and centers it.
    """
    def __init__(self, text=''):
        QLabel.__init__(self, '<h4>{}</h4>'.format(text))
        self.setAlignment(Qt.AlignHCenter)


class InstallationWizard(QWizard):
    """
    This is main component of the program - installation wizard, it connects all pages together.
    """
    def __init__(self, parent=None):
        """
        This constructor creates all the wizard pages adding all needed attributes to them,
        also it customizes installation wizard by specifying size and title.
        """
        super(InstallationWizard, self).__init__(parent)

        self.addPage(WelcomePage(self))
        self.addPage(RequirementsPage(parent=self))

        self.initPage = InitPage(self)
        self.addPage(self.initPage)
        finishPage = FinishPage(self)
        finishPage._parent = self
        self.addPage(finishPage)

        self.setWindowTitle("PyQtAccounts - Installation Wizard")
        self.resize(600, 600)


class WelcomePage(QWizardPage):
    """
    This is the first page of the wizard, it simply greets user.
    """
    def __init__(self, parent=None):
        super(WelcomePage, self).__init__(parent)
        # There is an icon of PyQtAccounts on the welcome page.
        self.setPixmap(
            QWizard.WatermarkPixmap,
            QPixmap(
                '/usr/share/icons/Mint-X/mimetypes/96/application-pgp-keys.svg'
            ))

        # Greetings
        self.title = Title(
            '<pre>Вітаємо у майстрі встановлення\n PyQtAccounts!</pre>')
        self.text = QLabel('<pre><br>Ми допоможемо вам пройти всі кроки \n'
                           'встановлення.</pre>')

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.text)
        self.setLayout(layout)


class PipInstall(QObject):
    """
    This object represents the process of installing pip dependencies.
    """
    # signals that are emit result of installing and fact that process has ended.
    result = pyqtSignal(int, str)
    finish = pyqtSignal()

    def __init__(self, reqs):
        """
        Constructor of the process, it saves Reqs instance.
        :param reqs:
        Reqs instance that contains to_install list which represents pip dependencies that we
        need to install.
        """
        QObject.__init__(self)
        self.reqs = reqs

    def run(self):
        """
        This method called to start installation process.
        """
        # here we iterate trough all not installed pip dependencies and install them emitting
        # results (i.e. success or failure)
        for req in self.reqs.to_install:
            res = os.system('pip3 install ' + req)
            self.result.emit(res, req)

        # at the end of the loop we emit finish signal to exit thread which contains our process
        self.finish.emit()


class RequirementsPage(QWizardPage):
    """
    This is a page that contains all information about requirements. Using ReqsList and ReqsTips
    we show user which dependencies he has installed, which has not and how to install them.
    It also contains install button to install unsatisfied pip dependencies.
    """
    def __init__(self, parent=None, reqs=Reqs()):
        super(RequirementsPage, self).__init__(parent)
        self._thread = None
        # Title and tip of the page
        self.title = Title('Залежності')
        self.text = QLabel('<pre>PyQtAccounts вимагає наявності\n'
                           'певних пакетів. Ось перелік тих які\n'
                           'встановлені, або не встановленні у вас:</pre>')

        # here we create requirements list and tips by instantiating ReqsList and ReqsTips.
        # also we create errors field for error messages that may occur in process of installation
        # of pip dependencies.
        self.reqs = reqs
        self.reqsList = ReqsList(reqs)
        self.reqsTips = ReqsTips(reqs)
        self.errors = Errors()

        # here are installation label and progressbar that we show during installation
        installation = QHBoxLayout()
        self.installLabel = QLabel('Інсталяція...')
        self.installProgress = QProgressBar()
        installation.addWidget(self.installLabel)
        installation.addWidget(self.installProgress)
        self.installLabel.hide()
        self.installProgress.hide()
        self.progress = 0

        # this is an `Install` button that user can use to install unsatisfied pip dependencies
        # if user already had satisfied all dependencies this button will be disabled.
        self.installButton = QPushButton("Встановити")
        self.installButton.clicked.connect(self.install)
        if not reqs.to_install:
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
        """
        This method called when user presses `Install` button. It validates whether pip is
        installed and starts installation process.
        """
        # here we hide and clear installation errors if they are shown
        self.errors.setText('')
        self.errors.hide()

        # if user hasn't installed pip then we can't perform the installation of pip dependencies
        # so here we check whether pip installed or not and if its not we show appropriate error.
        if 'pip3' in self.reqs.cant_install:
            self.errors.show()
            self.errors.setText('Встановіть пакет pip3!')
            return

        # here we disable install button to prevent user from pressing it again while last
        # installation process hasn't finished yet, if we start another thread when last hasn't
        # finished then we will override it (i.e. it will be destroyed) and it will crash the
        # program with error `QThread destroyed while thread is still running`.
        self.installButton.setEnabled(False)

        # here we start installation process in another thread to prevent blocking of GUI
        thread = QThread(parent=self)
        self.install = PipInstall(self.reqs)
        self.install.moveToThread(thread)
        self.install.result.connect(self.install_progress)
        self.install.finish.connect(self.install_finish)
        thread.started.connect(self.install.run)
        thread.start()
        self.installLabel.show()
        self.installProgress.show()

        # we must first check does last thread finished yet, if it not we must finish it
        # before writing another to _thread variable
        if self._thread and not self._thread.isFinished():
            self._thread.exit()

        # here we save our thread to _thread variable otherwise garbage collector will destroy it
        # (after method returns all its variables are destroyed).
        self._thread = thread

    def install_progress(self, res, req):
        """
        This method is a progress signal handler, it receives result code of installing each
        dependency and name of the dependency itself.
        It shows errors if result code is nonzero and updates progressbar if there is no errors.
        :param res:
        result code of the dependency
        :param req:
        name of the dependency
        """
        # here we update progress attribute which represents current state of installation
        self.progress += 100 / len(self.reqs.to_install)

        # if there are any errors during installation we show appropriate error message
        if res:
            text = self.errors.toPlainText()
            self.errors.setText(text + 'Не вдалося встановити ' + req + '\n')
            self.errors.show()
            return

        # if not we update progressbar and list of requirements
        self.installProgress.setValue(self.progress)
        reqs = Reqs()
        self.layout().removeWidget(self.reqsList)
        self.reqsList = ReqsList(reqs)
        self.layout().insertWidget(2, self.reqsList)

        # if progress is greater than or equal 100% then installation has finished.
        # so here we hide tips and show successful installation label.
        if self.progress >= 100:
            self.installLabel.setText(
                '<p style="color: #37FF91;">Встановлено!</p>')
            self.reqsTips.hide()

        # at the end we emit completeChanged signal to check have we installed everything yet or
        # we don't, if we have then we will enable `Next` button.
        self.completeChanged.emit()

    def install_finish(self):
        """
        This method is handler of `finish` signal of the PipInstall process. It simply exits
        thread to prevent errors such as `QThread destroyed while thread is still running` on exit.
        """
        self._thread.exit()

    def isComplete(self):
        """
        This method is handler of completeChanged signal, it simply checks whether every dependency
        is satisfied or not.
        :return:
        if every dependency is satisfied returns True and `Next` button will become available.
        """
        reqs = Reqs()
        return not (reqs.cant_install or reqs.to_install)


class Initialize(QObject):
    """
    This object represents the process of downloading the program itself from our github repository.
    """
    # signals that are emit result of initialization, fact that process has ended and progress of
    # initialization (downloading PyQtAccounts from repository).
    result = pyqtSignal(int)
    progress = pyqtSignal(int)
    finish = pyqtSignal()

    def __init__(self, folder):
        """
        In this constructor we simply save folder where we will download PyQtAccounts.
        :param folder:
        path to folder where we will download PyQtAccounts
        """
        QObject.__init__(self)
        self.folder = folder + '/PyQtAccounts'

    def run(self):
        """
        This method called to start initialization process.
        """
        import git

        class Progress(git.remote.RemoteProgress):
            """
            This class handles progress of clone operation, it receives number of objects already
            downloaded and total number of objects, then it calculates how much percents of objects
            are already downloaded.
            """
            def __init__(self, progress):
                """
                In this constructor we just save `progress` variable.
                :param progress:
                signal of initialization progress using which we will emit progress of cloning.
                """
                git.remote.RemoteProgress.__init__(self)
                self.progress = progress

            def update(self, op_code, cur_count, max_count=None, message=''):
                """
                This method does all calculation of progress percents and emits them using progress
                signal.
                :param cur_count:
                number of objects already downloaded
                :param max_count:
                total number of objects
                """
                # here we calculate progress percents and emit them using progress signal.
                progress = cur_count * 100 / max_count
                self.progress.emit(progress)

        try:
            # here we trying to clone our stable github repository in folder that user gave us
            # also we want to track the progress of clone process to show it on progressbar.
            git.Repo.clone_from('https://github.com/Acmpo6ou/PyQtAccounts',
                                self.folder,
                                progress=Progress(self.progress))
        except RecursionError:  # to prevent fatal python error
            raise
        except Exception:
            # if there are any errors we emit the nonzero result
            self.result.emit(1)
        else:
            # else we emit zero result
            self.result.emit(0)

        # at the end we emit that progress is finished to exit it normally
        self.finish.emit()


class InitPage(QWizardPage):
    """
    This page contains `Browse...` widget, progressbar, `Initialize` button, and checkboxes
    that represent whether user wants to create program shortcuts in system menu and on desktop
    or not.
    Initialization page provides everything that we need to clone PyQtAccounts from github
    repository.
    """
    def __init__(self, parent=None):
        super(InitPage, self).__init__(parent)
        # here we define _thread attribute where we will store an instance of our thread in which
        # we will start initialization progress
        self._thread = None

        # folder attribute which stores directory where we will clone PyQtAccounts
        self.folder = os.getenv('HOME')

        # title of the page, errors field for errors of initialization, progressbar to represent
        # the process of initializing
        self.title = Title('Ініціалізація')
        self.errors = Errors()
        self.progress = QProgressBar()

        # this is the `Browse...` widget:
        # label that explains purpose of it (i.e. that here user need to chose the folder
        #   where we will clone PyQtAccounts)
        # button that says `Browse...`, the chose folder dialog popups when user clicks it
        # label that represents path to directory being chosen
        self.initLabel = QLabel(
            'Виберіть папку в яку ви хочете встановити PyQtAccounts:')
        self.browseButton = QPushButton('Browse...')
        self.browseButton.clicked.connect(self.browse)
        self.browseLabel = QLabel(self.folder)

        # here is layout that holds all this together
        browseLayout = QHBoxLayout()
        browseLayout.addWidget(self.browseButton)
        browseLayout.addWidget(self.browseLabel)

        # `Initialize` button that starts initialization process when user clicks it
        self.initButton = QPushButton('Ініціалізувати')
        self.initButton.clicked.connect(self.init)

        # here we define system menu and desktop checkboxes (and helpful labels for them)
        # that will represent whether to create shortcuts or not
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
        """
        This method called when user clicks on the `Browse...` button
        """
        # here we obtain installation wizard, it is the parent of the page
        wizard = self.parent()

        # here we show directory dialog with appropriate title and opened directory.
        folder = QFileDialog.getExistingDirectory(wizard,
                                                  'Installation directory',
                                                  self.folder,
                                                  QFileDialog.ShowDirsOnly)

        # if user chose folder we save its path to `folder` attribute of the page and update
        # text of browse label.
        # Note: that if user hasn't chose folder (e.g. he pressed `Cancel`) folder will store
        # an empty string, so in that case we have to do nothing
        if folder:
            self.folder = folder
            self.browseLabel.setText(folder)

    def isComplete(self):
        """
        This method is called when completeChanged signal emits, here we check progressbar value
        if it is on 100% then we return True, so `Next` button will become enabled.
        """
        return self.progress.value() == 100

    def init(self):
        """
        This method called when user press `Initialize` button, it verifies is everything ready
        for initialization and if it is then he starts initialization process in another thread.
        """
        # if PyQtAccounts folder in the path that is chosen by user already exist then we can't
        # clone repository there, so we just pretend that initialization is already complete
        # showing 100% on the progressbar
        if 'PyQtAccounts' in os.listdir(self.folder):
            self.progress.setValue(100)

        # if progress attribute of the page doesn't equals 100 we start initialization process in
        # another thread
        if self.progress.value() != 100:
            thread = QThread(parent=self)
            self.initialize = Initialize(self.folder)
            self.initialize.moveToThread(thread)
            self.initialize.result.connect(self.check_result)
            self.initialize.progress.connect(self.init_progress)
            self.initialize.finish.connect(self.init_finish)
            thread.started.connect(self.initialize.run)
            thread.start()

            # we must first check does last thread finished yet, if it not we must finish it
            # before writing another to _thread variable
            if self._thread and not self._thread.isFinished():
                self._thread.exit()

            # here we save our thread to _thread variable otherwise garbage collector will destroy
            # it (after method returns all its variables are destroyed).
            self._thread = thread

    def check_result(self, res):
        """
        This method is handler of the result signal of initialization process, it checks `res`
        variable, if it contains nonzero code we show appropriate error message.
        :param res:
        result code of the initialization process
        """
        # here we clear and hide errors field if it already displayed
        self.errors.hide()
        self.errors.setText('')

        # here we check result code and if it is nonzero we show error message advising
        # user to check his internet connection and rights to write to folder that he defined
        # as directory in which we clone github repository
        if res:
            self.errors.show()
            self.errors.setText(
                'Помилка ініціалізації!\n'
                "Відсутнє мережеве з'єднання, або відмовлено у доступі на "
                "запис у папку інсталяції.")

    def init_progress(self, progress):
        """
        This method is handler of progress signal of the initialization progress.
        It receives progress in % of initialization process.
        :param progress:
        progress of initialization process.
        """
        # here we update our progressbar according to received progress
        self.progress.setValue(progress)

        # if progress equals to 100% then we emit completeChanged signal to enable `Next` button
        if progress >= 100:
            self.completeChanged.emit()

    def init_finish(self):
        """
        This method is handler of `finish` signal of the PipInstall process. It simply exits
        thread to prevent errors such as `QThread destroyed while thread is still running` on exit.
        """
        self._thread.exit()


class FinishPage(QWizardPage):
    """
    This page simply shows message saying that installation is successful (regardless of is it
    really successful or not though, technically user will not reach this page if installation
    is unsuccessful). Also page creates shortcuts in system menu and on desktop according to
    checkbox states on the initialization page, it also creates run.sh file which will initialize
    environment for PyQtAccounts and will run it.
    """
    def __init__(self, parent=None):
        """
        This constructor simply creates title and success label.
        """
        super(FinishPage, self).__init__(parent)

        self.title = Title('Finish')
        self.text = QLabel('Успішно установлено PyQtAccounts!')

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.text)
        self.setLayout(layout)

    def initializePage(self):
        """
        This method called when we show this page, it creates system menu, desktop shortcuts
        and run.sh script.
        """
        # here we obtain states of the shortcuts checkboxes on the initialization page and path
        # to program folder
        initPage = self._parent.initPage
        cwd = initPage.folder + '/PyQtAccounts/'
        desktop = initPage.desktopCheckbox.isChecked()
        startmenu = initPage.menuCheckbox.isChecked()

        # here we create shortcuts if at least one of shortcut checkboxes are checked
        if desktop or startmenu:
            # we use make_shortcut function from pyshortcuts module for this.
            make_shortcut(name='PyQtAccounts',
                          script=cwd + '/run.sh',
                          description='Simple account database manager.',
                          icon=cwd + '/img/icon.svg',
                          terminal=False,
                          desktop=desktop,
                          startmenu=startmenu,
                          executable='/bin/bash')

            # fixing .ico icon issue, make_shortcut function adds .ico extension to icon path
            # (i.e. our '/img/icon.svg' becomes '/img/icon.svg.ico'), so we remove .ico from our
            # icon path
            home = os.getenv('HOME')
            if desktop:
                desktop = open(home + '/Desktop/PyQtAccounts.desktop').read()
                with open(home + '/Desktop/PyQtAccounts.desktop', 'w') as file:
                    file.write(desktop.replace('.ico', ''))

            if startmenu:
                menu = open(
                    home +
                    '/.local/share/applications/PyQtAccounts.desktop').read()
                with open(
                        home +
                        '/.local/share/applications/PyQtAccounts.desktop',
                        'w') as file:
                    file.write(menu.replace('.ico', ''))

        # here we create run.sh script which will start our application
        run = ('#!/bin/bash\n\n'
               f'cd {cwd}\n'
               f'export PYTHONPATH="$PYTHONPATH:{cwd}"\n'
               'python3 PyQtAccounts.py')

        with open(cwd + 'run.sh', 'w') as runfile:
            runfile.write(run)

        # here we give the script permissions for execution
        os.chmod(cwd + 'run.sh', 0o755)


if __name__ == '__main__':
    # here we create application instance, set normal font size and icon
    app = QApplication(sys.argv)
    app.setStyleSheet('''
    *{
        font-family: Ubuntu, Ubuntu Mono;
        font-size: 24px;
    }
    ''')
    app.setWindowIcon(
        QIcon('/usr/share/icons/Mint-X/mimetypes/96/application-pgp-keys.svg'))
    wizard = InstallationWizard()
    wizard.show()
    sys.exit(app.exec_())
