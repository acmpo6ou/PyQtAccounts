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

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtCore


from unittest.mock import Mock
import pytest
import os

from tests.base import UnitTest, init_accounts_folder
from setup import *

# this is text of initialization error message
INIT_ERROR = (
    "Помилка ініціалізації!\n"
    "Відсутнє мережеве з'єднання, або відмовлено у доступі"
    " на запис у папку інсталяції."
)


class InitPageTest(UnitTest):
    """
    This test class provides all tests for initialization page.
    """
    def test_page(self):
        """
        This test tests page itself.
        """
        # here we set environment variable to fake in-memory folder and create
        # initialization page
        self.monkeypatch.setenv('HOME', '/home/accounts')
        page = InitPage()

        # here we check some default attributes of init page.
        self.assertIsNone(page._thread, 
                          '_thread must be set to None when constructing instance')
        self.assertEqual(page.folder, '/home/accounts',
                         'folder attribute of InitPage must be set to'
                         '`/home/accounts` by default!')

        self.assertEqual(page.title.text(), '<h4>Ініціалізація</h4>',
                         'Page title is incorrect!')
        self.assertEqual(page.initLabel.text(),
                         'Виберіть папку в яку ви хочете встановити PyQtAccounts:',
                         'Browse tip is incorrect!')
        self.assertEqual(page.browseLabel.text(), '/home/accounts', 'Browse label is incorrect!')

        self.assertTrue(page.menuCheckbox.isChecked(),
                        'Menu shortcut checkbox at initialization page must be checked!')
        self.assertTrue(page.desktopCheckbox.isChecked(),
                        'Desktop shortcut checkbox at initialization page must be checked!')

    def test_browse(self):
        """
        This test tests browse widget of init page.
        """
        def mock_browse(parent, title, folder, dirs_only_flag):
            """
            This function is a mock for for getExistingDirectory from QFileDialog.
            We use it to prevent directory dialog from appearing during testing, also to check
            parameters that are passed to directory dialog function.
            :param parent:
            parent of directory dialog
            :param title:
            title of dialog
            :param folder:
            default folder that dialog shows
            :param dirs_only_flag:
            flag that forces dialog to show directories only
            :return:
            path to fake directory that we simulate is chosen by user
            """
            # here we check parameters listed above
            assert title == 'Installation directory', 'Directory dialog title is incorrect.'
            assert folder == os.getenv('HOME'), 'Default directory of directory dialog must be ' \
                                                'a home folder (i.e. /home/accounts)!'
            assert dirs_only_flag == QFileDialog.ShowDirsOnly
            return '/home/accounts/myprograms'

        # here we patch getExistingDirectory
        self.monkeypatch.setattr(QFileDialog, 'getExistingDirectory', mock_browse)

        # then we create init page and click on button of browse widget
        page = InitPage()
        page.browseButton.click()

        # here we check does `folder` attribute and label of browse widget have changed to
        # directory hat we chose in dialog
        self.assertEqual(page.folder, '/home/accounts/myprograms',
                         'folder of init page is incorrect, must change after we chose another'
                         ' in browse dialog!')
        self.assertEqual(page.browseLabel.text(), '/home/accounts/myprograms',
                         'folder of browse label is incorrect, must change after we chose another'
                         ' in browse dialog!')

    def test_is_complete(self):
        """
        The `Next` button of installation wizard must be enabled only if initialization is
        complete, this test tests such behavior.
        """
        # here we create init page then set progress value to 0% (just to be sure that init
        # process is not complete)
        page = InitPage()
        page.progress.setValue(0)
        # then we check that `Next` button is disabled
        self.assertFalse(page.isComplete(), '`Next` button must be disabled when init progress is'
                                            'not complete!')

        # here we set progress to 100% (i.e. to represent that init process is complete
        page.progress.setValue(100)
        # then we check is `Next` button enabled
        self.assertTrue(page.isComplete(), '`Next` button must be enabled when init progress is'
                                           'complete!')

    def test_init_already(self):
        """
        This test tests installation wizards behavior when program already installed in specified
        by user folder, in such cases we must set init process progressbar to 100% and enable
        `Next` button.
        """
        # here we monkeypatch os.listdir so it will return `PyQtAccounts` in list of current
        # directory and program will think that PyQtAccounts is already installed
        self.monkeypatch.setattr('os.listdir', lambda path: ['PyQtAccounts'])

        # then we create init page and click init button
        page = InitPage()
        page.initButton.click()

        # here we check that progressbar displays 100% now

        # here we check that progressbar displays 100% now
        self.assertEqual(page.progress.value(), 100,
                         'Progressbar must display 100% when program is already installed and '
                         'user clicks on initialize button!')

    def test_init(self):
        # Tom wants to initialize PyQtAccounts in his home directory
        init_accounts_folder()
        page = InitPage()
        self.assertEqual(page.browseLabel.text(), '/home/accounts')

        # Everything seems fine so he presses `Initialize` button
        page.initButton.click()

        # some time passes and initialization is complete
        def is_finished():
            assert page._thread.isFinished()
        self.qbot.waitUntil(is_finished, timeout=3000)

        # Progressbar shows 100% and program initialized with all its folder structure
        self.assertEqual(page.progress.value(), 100)
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/src'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/core'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/COPYING'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/CREDITS'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/change.log'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/setup.py'))
        self.assertTrue(os.path.exists('/home/accounts/PyQtAccounts/img'))

    def test_init_fail_when_no_permissions(self):
        """
        This test tests how installation wizard would react when user tries to install program
        somewhere where we don't have permissions to write. In that case program must show
        appropriate error message.
        """
        # Tom wants to install PyQtAccounts in `/` folder
        page = InitPage()
        page.folder = '/'  # we have no permissions to write in root folder

        # so he presses init button
        page.initButton.click()

        # error message appears saying that he has no permission to write in `/` folder
        def errors_visible():
            assert page.errors.visibility, "Initialization error message is not displayed!"
        self.qbot.waitUntil(errors_visible)
        self.assertEqual(page.errors.toPlainText(), INIT_ERROR, 'Error message of initialization '
                                                                'is incorrect!')
