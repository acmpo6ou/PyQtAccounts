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
from core.testutils import QWidget
import sys
import os

from core.db_forms import *
from core.account_forms import *
from core.utils import *
from core.widgets import *
from core.windows import *
from core.updates import *
from core.const import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtAccounts - PyQt5")
        self.resize(1000, 500)
        self.show()

        self.name = ''
        self.setWindowIcon(QIcon('img/icon.svg'))
        windows = [self]
        self.windows = windows
        self.destroy = False
        self.res = None

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

        # to avoid test side effects
        mode = 'PyToolsTest' if os.getenv('TESTING') else 'PyTools'
        sets = QSettings(mode, 'PyQtAccounts')

        is_main_db = sets.value('advanced/is_main_db', False, type=bool)
        main_db = sets.value('advanced/main_db', '', type=str)
        if is_main_db and main_db in getDbList():
            self.dbs.list.selected(Index(main_db))

        self.about = About()

        menuBar = AppMenuBar(self)
        self.setMenuBar(menuBar)
        self.setCentralWidget(splitter)

        if time_for_updates():
            def mess(changes, log):
                if changes:
                    self.res = UpdatesAvailable(self, log)
            thread = QThread(parent=self)
            updating = Updating()
            updating.moveToThread(thread)
            updating.result.connect(mess)
            thread.started.connect(updating.run)
            thread.start()

        settings = Settings(self)

        self.settings = settings

    def closeEvent(self, event):
        # Do not show the close confirmation popup if there is no opened
        # databases.
        if len(self.windows) == 1:
            self.visibility = False
            event.accept()
            return

        if self.destroy:
            action = QMessageBox.Yes
        else:
            action = QMessageBox.question(self, 'Увага!', 'Ви певні що хочете вийти?')

        if action == QMessageBox.No:
            event.ignore()
        else:
            self.visibility = False
            for win in self.windows:
                win.ask = False
                win.close()


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


def main():
    if not '.git' in os.listdir('.'):
        return WarningWindow(
            '''
            <h3>Програму не ініціалізовано!</h3>
            <p>Завантажте файл <b><i>setup.py</i></b> з нашого github репозиторія.</p>
            <p>Запустіть його і пройдіть всі кроки інсталяції.</p>
            <p>Ініціалізація потрібна, аби система оновлення PyQtAccounts працювала.</p>
            <p>Система оновлення автоматично перевіряє, завантажує і встановлює оновлення.</p>
            ''')

    for req in sys_reqs:
        if os.system(f'which {req}'):
            return WarningWindow('''
                <h3>Не всі пакети встановлено!</h3>
                <p>Пакет {0} не встановлено, без певних пакетів PyQtAccounts буде працювати 
                некоректно!</p>
                <p>Встановіть {0} такою командою:</p>
                <p>sudo apt install {0}</p>
                '''.format(req))


    try:
        import git
        window = Window()
    except ImportError as err:
        for req in reqs_pip:
            if req in err.msg:
                req = req
                mess = ('<p>Здається не всі бібліотеки встановлені.</p>'
                        f'<p>Переконайтеся що ви встановили бібліотеку {req}.</p>'
                        '<p>Якщо ні, спробуйте ввести в термінал цю кофманду:</p>'
                        f'<p><b>pip3 install {req}</b></p>')
                return ErrorWindow(mess, err)
    except RecursionError: # to prevent fatal python error
        raise
    except Exception as err:
        mess = 'Вибачте програма повинна припинити роботу через помилку.'
        if os.getenv('TESTING'):
            return ErrorWindow(mess, err)
        else:
            raise


app = QApplication(sys.argv)

app.setStyleSheet('''
*{
    font-size: 24px;
}
''')


if __name__ == '__main__':
    main()
    sys.exit(app.exec_())
