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
import sys
import os


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtAccounts - PyQt5")
        self.resize(1000, 500)
        self.show()

        self.name = ''
        self.setWindowIcon(QIcon('../img/icon.svg'))
        windows = [self]

        helpTip = HelpTip(HELP_TIP_DB)
        if getDbList():
            helpTip = HelpTip("Виберіть базу данних")
        helpTip.show()

        alreadyOpen = HelpTip('Базу данних вже відкрито')

        editTip = WarningTip('Ви повинні відкрити базу данних перед тим як '
                             'редагувати її!')

        exportTip = WarningTip("Виберіть базу данних яку хочете експортувати.")

        tips = {
            'help': helpTip,
            'already-open': alreadyOpen,
            'edit-w': editTip,
            'export': exportTip
        }

        create_db_form = CreateDbForm(helpTip, parent=self)
        open_db_form = OpenDbForm(helpTip, windows, parent=self)
        edit_db_form = EditDbForm(tips, windows, parent=self)

        forms = {
            'create': create_db_form,
            'edit': edit_db_form,
            'open': open_db_form
        }
        dbs = Dbs(forms, windows, tips)
        dbs.setMaximumWidth(200)

        splitter = QSplitter()
        for tip in tips:
            splitter.addWidget(tips[tip])

        for form in forms:
            splitter.addWidget(forms[form])

        splitter.addWidget(dbs)
        self.dbs = dbs

        sets = QSettings('PyTools', 'PyQtAccounts')
        is_main_db = sets.value('advanced/is_main_db', False, type=bool)
        main_db = sets.value('advanced/main_db', '', type=str)
        if is_main_db and main_db in getDbList():
            self.dbs.list.selected(Index(main_db))

        def onClose(event):
            # Do not show the close confirmation popup if there is no opened
            # databases.
            if len(windows) == 1:
                event.accept()
                return

            action = QMessageBox.question(self, 'Увага!', 'Ви певні що хочете '
                                                          'вийти?')
            if action == QMessageBox.No:
                event.ignore()
            else:
                for win in windows:
                    win.ask = False
                    win.close()

        menuBar = AppMenuBar(self)
        self.setMenuBar(menuBar)
        self.closeEvent = onClose

        self.setCentralWidget(splitter)
        self.show()

        if not '.git' in os.listdir('../'):
            WarningWindow('''
            <h3>Програму не ініціалізовано!</h3>
            <p>Завантажте файл <b><i>setup.py</i></b> з нашого github репозиторія.</p>
            <p>Запустіть його і пройдіть всі кроки інсталяції.</p>
            <p>Ініціалізація потрібна, аби система оновлення PyQtAccounts працювала.</p>
            <p>Система оновлення автоматично перевіряє, завантажує і встановлює оновлення.</p>
            ''')

        reqs_list = ['git', 'pip3', 'xclip']
        for req in reqs_list:
            if os.system(f'which {req}'):
                WarningWindow('''
                    <h3>Не всі пакети встановлено!</h3>
                    <p>Пакет {0} не встановлено, без певних пакетів PyQtAccounts буде працювати 
                    некоректно!</p>
                    <p>Встановіть {0} такою командою:</p>
                    <p>sudo apt install {0}</p>
                    '''.format(req))

        if time_for_updates():
            thread = QThread(parent=self)
            updating = Updating()
            updating.moveToThread(thread)
            updating.result.connect(lambda changes, log: changes and UpdatesAvailable(self, log))
            thread.started.connect(updating.run)
            thread.start()

        settings = Settings(self)
        self.settings = settings

def main():
    window = Window()
    sys.exit(app.exec_())


class ErrorWindow(QMessageBox):
    def __init__(self, text, err, parent=None):
        super().__init__()
        self.setWindowTitle('Помилка!')
        self.setIcon(super().Critical)
        self.setDetailedText(str(err))
        self.setText(text)
        self.exec()


class WarningWindow(QMessageBox):
    def __init__(self, text, parent=None):
        super().__init__()
        self.setWindowTitle('Увага!')
        self.setIcon(super().Warning)
        self.setText(text)
        self.exec()


app = QApplication(sys.argv)

app.setStyleSheet('''
*{
    font-size: 24px;
}
''')

try:
    from db_forms import *
    from account_forms import *
    from utils import *
    from widgets import *
    from windows import *
    from updates import *
    from const import *

    import git

    if __name__ == '__main__':
        main()
except ImportError as err:
    reqs_pip = ['setuptools', 'cryptography', 'git', 'pyshortcuts']  # git is gitpython module
    for req in reqs_pip:
        if req in err.msg:
            req = req.replace('git', 'gitpython')
            mess = ('<p>Здається не всі бібліотеки встановлені.</p>'
                    f'<p>Переконайтеся що ви встановили бібліотеку {req}.</p>'
                    '<p>Якщо ні, спробуйте ввести в термінал цю кофманду:</p>'
                    f'<p><b>pip3 install {req}</b></p>')
            ErrorWindow(mess, err)
    sys.exit()
except Exception as err:
    mess = '''Вибачте програма повинна припинити роботу через помилку.'''
    ErrorWindow(mess, err)
    raise
    sys.exit()

if __name__ == '__main__':
    sys.exit(app.exec_())