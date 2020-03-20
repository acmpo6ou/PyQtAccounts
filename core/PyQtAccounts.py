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
import sys
import os

def main():
    window = QMainWindow()
    window.setWindowTitle("PyQtAccounts - PyQt5")
    window.resize(1000, 500)

    window.name = ''
    window.setWindowIcon(QIcon('../img/icon.svg'))
    windows = [window]

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

    create_db_form = CreateDbForm(helpTip, parent=window)
    open_db_form = OpenDbForm(helpTip, windows, parent=window)
    edit_db_form = EditDbForm(tips, windows, parent=window)

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
    window.dbs = dbs

    def onClose(event):
        # Do not show the close confirmation popup if there is no opened
        # databases.
        if len(windows) == 1:
            event.accept()
            return

        action = QMessageBox.question(window, 'Увага!', 'Ви певні що хочете '
                                                        'вийти?')
        if action == QMessageBox.No:
            event.ignore()
        else:
            for win in windows:
                win.ask = False
                win.close()

    menuBar = AppMenuBar(window)
    window.setMenuBar(menuBar)
    window.closeEvent = onClose

    window.setCentralWidget(splitter)
    window.show()

    if not '.git' in os.listdir('../'):
        WarningWindow('''
        <h3>Програму не ініціалізовано!</h3>
        <p>Завантажте файл <b><i>setup.py</i></b> з нашого github репозиторія.</p>
        <p>Запустіть його і пройдіть всі кроки інсталяції.</p>
        <p>Ініціалізація потрібна, аби система оновлення PyQtAccounts працювала.</p>
        <p>Система оновлення автоматично перевіряє, завантажує і встановлює оновлення.</p>
        ''')

    if time_for_updates():
        thread = QThread(parent=window)
        updating = Updating()
        updating.moveToThread(thread)
        updating.result.connect(lambda changes: changes and UpdatesAvailable(window))
        thread.started.connect(updating.run)
        thread.start()

    settings = Settings(window)
    window.settings = settings

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

    main()
except ImportError as err:
    if 'cryptography' in err.msg:
        mess = '''Здається не всі бібліотеки встановлені.
Переконайтеся що ви встановили бібліотеку cryptography.
Якщо ні, спробуйте ввести в термінал цю кофманду:
            pip3 install cryptography'''
        ErrorWindow(mess, err)
        sys.exit()
except Exception as err:
    mess = '''Вибачте програма повинна припинити роботу через помилку.'''
    ErrorWindow(mess, err)
    raise
    sys.exit()

sys.exit(app.exec_())