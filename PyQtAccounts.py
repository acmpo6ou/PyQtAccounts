#!/usr/bin/env python3

#  Copyright (c) 2020-2021. Bohdan Kolvakh
#  This file is part of PyQtAccounts.
#
#  PyQtAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyQtAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.
#
#  PyQtAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyQtAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.

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
This is the main module of the application, it connects everything into complete program -
PyQtAccounts.
"""

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
import core.const

SRC_DIR = core.const.SRC_DIR


class Window(QMainWindow):
    """
    This class is a main window.
    """
    def __init__(self):
        """
        This constructor creates everything that application needs.
        It builds main window of PyQtAccounts.
        """
        super().__init__()
        self.setWindowTitle("PyQtAccounts - PyQt5")
        self.resize(1000, 500)
        self.show()

        # main window doesn't have a name, this way we can differ it in between other windows.
        self.name = ''
        self.setWindowIcon(QIcon('img/icon.svg'))

        # main window is always the first window
        windows = [self]
        self.windows = windows
        self.res = None

        # here we create all tips
        helpTip = HelpTip(HELP_TIP_DB)
        if getDbList():
            helpTip = HelpTip("Виберіть базу данних")
        helpTip.show()

        # and warnings
        alreadyOpen = HelpTip('Базу данних вже відкрито')
        editTip = WarningTip('Ви повинні відкрити базу данних перед тим як '
                             'редагувати її!')
        exportTip = WarningTip("Виберіть базу данних яку хочете експортувати.")
        deleteTip = WarningTip("Виберіть базу данних яку хочете видалити.")

        tips = {
            'help': helpTip,
            'already-open': alreadyOpen,
            'edit-w': editTip,
            'export': exportTip,
            'delete': deleteTip
        }

        # and here we create all forms
        create_db_form = CreateDbForm(helpTip, parent=self)
        open_db_form = OpenDbForm(helpTip, windows, parent=self)
        edit_db_form = EditDbForm(tips, windows, parent=self)

        forms = {
            'create': create_db_form,
            'edit': edit_db_form,
            'open': open_db_form
        }

        # settings
        sets = QSettings(f'{os.getenv("HOME")}/PyTools', 'PyQtAccounts')

        # here we instantiate Dbs class and add it to splitter which will split Dbs and forms
        dbs = Dbs(forms, windows, tips)
        list_width = sets.value('advanced/list_width', 200, type=int)
        dbs.setMaximumWidth(list_width)

        splitter = QSplitter()
        for tip in tips:
            splitter.addWidget(tips[tip])

        for form in forms:
            splitter.addWidget(forms[form])

        splitter.addWidget(dbs)
        self.dbs = dbs

        # here we obtain the main database feature settings
        is_main_db = sets.value('advanced/is_main_db', False, type=bool)
        main_db = sets.value('advanced/main_db', '', type=str)

        # if user has main database feature turned on we auto select main database
        if is_main_db and main_db in getDbList():
            self.dbs.list.selected(Index(main_db))

        # here we create about dialog and menu bar of the main window
        self.about = About()
        menuBar = AppMenuBar(self)
        self.setMenuBar(menuBar)
        self.setCentralWidget(splitter)

        # here we check for updates
        def mess(changes, log):
            if changes:
                self.res = UpdatesAvailable(self, log)
            thread.exit()

        # we start the checking process in another thread to prevent blocking of UI
        thread = QThread(parent=self)
        updating = Updating()
        updating.moveToThread(thread)
        updating.result.connect(mess)
        thread.started.connect(updating.run)
        thread.start()

        # here we create settings dialog
        self.settings = Settings(self)

    def closeEvent(self, event):
        """
        This method called when user tries to close window.
        Here we can warn him about opened databases (i.e. does he really wants to quit
        because he may be accidentally pressed close button).
        """
        # Do not show the close confirmation popup if there is no opened
        # databases.
        if len(self.windows) == 1:
            self.visibility = False
            event.accept()
            return

        # here we show confirm message
        action = QMessageBox.question(self, 'Увага!',
                                      'Ви певні що хочете вийти?')

        if action == QMessageBox.No:
            # if user answered no we do nothing (i.e ignore close event)
            event.ignore()
        else:
            self.visibility = False

            # here we close all database windows together with main window and without
            # confirmation popups
            for win in self.windows:
                win.ask = False
                win.close()


class ErrorWindow(QMessageBox):
    """
    This class is a window that we show if program caused some errors.
    """
    def __init__(self, text, err):
        super().__init__()
        # here we set window title, icon and text. We also have detailed description which
        # contains error message.
        self.setWindowTitle('Помилка!')
        self.setIcon(super().Critical)
        self.setDetailedText(str(err))
        self.setText(text)
        self.exec()


class WarningWindow(QMessageBox):
    """
    This class is a window that we show if we want to warn user about something.
    """
    def __init__(self, text):
        super().__init__()
        # here we set window title, icon and text.
        self.setWindowTitle('Увага!')
        self.setIcon(super().Warning)
        self.setText(text)
        self.exec()


def main():
    """
    This is the main function of PyQtAccounts, it creates main window and handles errors and
    some problems that are detected on startup.
    :return:
    None if there is no errors.
    Warning or Error window if there are some errors.
    """

    # here we check whether program is initialized by checking does .git dir exists in program
    # folder, if it doesn't we show initialization warning
    if '.git' not in os.listdir('.'):
        return WarningWindow('''
            <h3>Програму не ініціалізовано!</h3>
            <p>Завантажте файл <b><i>setup.py</i></b> з нашого github репозиторія.</p>
            <p>Запустіть його і пройдіть всі кроки інсталяції.</p>
            <p>Ініціалізація потрібна, аби система оновлення PyQtAccounts працювала.</p>
            <p>Система оновлення автоматично перевіряє, завантажує і встановлює оновлення.</p>
            ''')

    # here we check whether all dependencies are installed, if not we show warning
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
        # here we create application window, if any errors occur during lifetime of the program
        # we will catch them below
        import git
        window = Window()
    except ImportError as err:
        # if we caught import error it means that not all dependencies are satisfied
        # so we show error message and give user proper advice about how to install dependencies
        # that aren't satisfied yet
        for req in reqs_pip:
            if req in err.msg:
                req = req
                mess = (
                    '<p>Здається не всі бібліотеки встановлені.</p>'
                    f'<p>Переконайтеся що ви встановили бібліотеку {req}.</p>'
                    '<p>Якщо ні, спробуйте ввести в термінал цю кофманду:</p>'
                    f'<p><b>pip3 install {req}</b></p>')
                return ErrorWindow(mess, err)
    except RecursionError:  # to prevent fatal python error
        raise
    except Exception as err:
        # if there are any other errors we show error message.
        mess = 'Вибачте програма повинна припинити роботу через помилку.'
        win = ErrorWindow(mess, err)

        # during testing we want to return error window (to test it), so if TESTING is true we do so
        if os.getenv('TESTING'):
            return win
        else:
            raise


# here we create application instance and set proper font size, because by default it might be small
app = QApplication(sys.argv)
app.setStyleSheet('''
*{
    font-size: 24px;
}

QLineEdit, QLabel, QLineEdit{
    font-family: Ubuntu Mono, Ubuntu;
}
''')
# also above we set monospace font for all line edit fields, so user could read passwords from them
# easily

if __name__ == '__main__':
    # here we check whether user runs PyQtAccounts under sudo
    if os.getuid() == 0:
        # if yes, then we show appropriate warning, because launched with sudo
        # PyQtAccounts will create and edit databases, but owner of them is root
        # and normal user wont be able to edit or open those databases
        QMessageBox.warning(
            None, 'Увага!',
            "PyQtAccounts запущено з адміністративними привілеями, не "
            "рекомендовано робити це, адже PyQtAccounts буде створювати і "
            "редагувати бази данних, але їх власник буде root і нормальний "
            "користувач вже не зможе відкривати і редагувати такі бази данних "
            "без рут приівлеїв.")

    main()
    sys.exit(app.exec_())
