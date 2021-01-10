#!/usr/bin/env python3

#  Copyright (c) 2020-2021. Kolvakh Bohdan
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
This module provides all widget for PyQtAccouts.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from core.testutils import QWidget

import core.genpass as genpass
from core.utils import *


class Tip(QLabel):
    """
    This class is a label that customized for tip, it has its own green color and font.
    """
    def __init__(self, text=''):
        QLabel.__init__(self, text)

        font = QFont('Ubuntu Mono', 18)
        self.setStyleSheet('color: #37FF91;')
        self.setFont(font)


class HelpTip(QLabel):
    """
    This class is a label that customized for help tip, it has its own font and centered text.
    """
    def __init__(self, text=''):
        QLabel.__init__(self, text)
        self.setAlignment(Qt.AlignCenter)
        font = QFont('Ubuntu Mono', 18, QFont.StyleItalic)
        self.setFont(font)
        self.hide()


class WarningTip(HelpTip):
    """
    This class is a label that customized for warning, it has its own yellow color.
    """
    def __init__(self, text=''):
        HelpTip.__init__(self, text)
        self.setStyleSheet('color: #be9117;')
        self.hide()


class Title(QLabel):
    """
    This class is a label that customized as title, it makes it text bold and centered.
    """
    def __init__(self, text=''):
        text = '<b>{}</b>'.format(text)
        QLabel.__init__(self, text)
        self.setAlignment(Qt.AlignHCenter)


class Error(QLabel):
    """
    This class is a label that customized for error, it has its own red color and font.
    """
    def __init__(self, text=''):
        QLabel.__init__(self, text)

        font = QFont('Ubuntu Mono', 18)
        self.setStyleSheet('color: #f26666;')
        self.setFont(font)


class PasswordField(QHBoxLayout):
    """
    This class is a password field that has button which shows and hides password.
    """
    def __init__(self, placeholder=''):
        QHBoxLayout.__init__(self)

        # the input itself
        self.passInput = QLineEdit()
        self.passInput.setPlaceholderText(placeholder)
        self.passInput.setEchoMode(QLineEdit.Password)

        # button that shows and hides password
        self.showButton = QPushButton()
        self.showButton.setIcon(QIcon('img/show.svg'))
        self.showButton.setIconSize(QSize(25, 25))
        self.showButton.clicked.connect(self.toggleShow)

        self.addWidget(self.passInput)
        self.addWidget(self.showButton)

    def toggleShow(self):
        """
        This method called when show-hide button is pressed, it toggles password visibility,
        and icon shown at the show-hide button.
        """
        if self.passInput.echoMode() == QLineEdit.Password:
            self.passInput.setEchoMode(QLineEdit.Normal)
            self.showButton.setIcon(QIcon('img/hide.svg'))
        else:
            self.passInput.setEchoMode(QLineEdit.Password)
            self.showButton.setIcon(QIcon('img/show.svg'))


class GenPassDialog(QDialog):
    """
    This class is a dialog for password generation.
    """
    def __init__(self, form):
        """
        This is constructor of dialog.
        :param form:
        form that contains password fields that dialog will fill when it generates password.
        """
        QDialog.__init__(self, form.parent())
        self.form = form
        self.setModal(True)
        self.setSizeGripEnabled(True)
        self.setWindowTitle('Згенерувати пароль')
        self.resize(700, 300)

        # This is label, tip and spinbox that are define password length
        self.symLabel = QLabel('Довжина пароля: ')
        self.symNum = QSpinBox()
        self.symNum.setMinimum(8)
        self.symNum.setValue(16)
        self.symTip = Tip("Рекомендуємо вибирати число не меншне 16")

        self.symLayout = QHBoxLayout()
        self.symLayout.addWidget(self.symLabel)
        self.symLayout.addWidget(self.symNum)

        # There are 4 sections that create 4 flags and labels, that define what symbols to use
        # in password
        self.digitsLabel = QLabel('Цифри')
        self.digitsFlag = QCheckBox()
        self.digitsFlag.setChecked(True)
        self.digitsFlag.name = 'd'
        self.digitsLabel.setBuddy(self.digitsFlag)

        self.lowerLabel = QLabel('Малі англійські букви')
        self.lowerFlag = QCheckBox()
        self.lowerFlag.setChecked(True)
        self.lowerFlag.name = 'l'
        self.lowerLabel.setBuddy(self.lowerFlag)

        self.upperLabel = QLabel('Великі англійські букви')
        self.upperFlag = QCheckBox()
        self.upperFlag.setChecked(True)
        self.upperFlag.name = 'u'
        self.upperLabel.setBuddy(self.upperFlag)

        self.punctuationLabel = QLabel('Знаки пунктуації')
        self.punctuationFlag = QCheckBox()
        self.punctuationFlag.setChecked(True)
        self.punctuationFlag.name = 'p'
        self.punctuationLabel.setBuddy(self.punctuationFlag)

        self.checkGrid = QGridLayout()
        self.checkGrid.addWidget(self.digitsFlag, 0, 0)
        self.checkGrid.addWidget(self.digitsLabel, 0, 1, 1, 10)
        self.checkGrid.addWidget(self.upperFlag, 1, 0)
        self.checkGrid.addWidget(self.upperLabel, 1, 1, 1, 10)
        self.checkGrid.addWidget(self.lowerFlag, 2, 0)
        self.checkGrid.addWidget(self.lowerLabel, 2, 1, 1, 10)
        self.checkGrid.addWidget(self.punctuationFlag, 3, 0)
        self.checkGrid.addWidget(self.punctuationLabel, 3, 1, 1, 10)

        self.includeTip = Tip("Не рекомендуємо змінювати ці параметри,\n"
                              "адже вони можуть вплинути на силу пароля.")

        self.buttonCancel = GTKButton(DELETE_BUTTON, 'Скасувати')
        self.buttonGenerate = GTKButton(APPLY_BUTTON, 'Згенерувати')
        self.buttonCancel.clicked.connect(self.hide)
        self.buttonGenerate.clicked.connect(self.generate)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.buttonCancel)
        self.buttonsLayout.addWidget(self.buttonGenerate)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.symLayout)
        self.layout.addWidget(self.symTip)
        self.layout.addLayout(self.checkGrid)
        self.layout.addWidget(self.includeTip)
        self.layout.addLayout(self.buttonsLayout)
        self.setLayout(self.layout)

    def generate(self, event):
        """
        This method called when user presses `Generate` button, it fills forms password fields
        with generated password.
        """
        symbs = ''
        for box in self.digitsFlag, self.upperFlag, self.lowerFlag, self.punctuationFlag:
            flag = box.isChecked()
            if flag:
                symbs += box.name

        password = genpass.main(symbs, self.symNum.value())
        self.form.passField.passInput.setText(password)
        self.form.passRepeatField.passInput.setText(password)
        self.hide()


# here are constants that define styles of GTK buttons for GTKButton class

BUTTON_TEMPLATE = """
    QPushButton {{
        border-radius: 4px;
        color: #ffffff;
        background-color: #{};
        font-size: 24px;
        min-height: 40px;
        min-width: 128px;
        outline: none;
    }}
    QPushButton:hover {{
        background-color: #{};
    }}
    QPushButton:pressed {{
        background-color: #{};
    }}
"""

APPLY_BUTTON = BUTTON_TEMPLATE.format("6db442", "8ad064", "5a9a37")
APPLY_BUTTON_DISABLED = ""
DELETE_BUTTON = BUTTON_TEMPLATE.format("f04a50", "e96b7c", "d60326")
INFO_BUTTON = BUTTON_TEMPLATE.format("4a90d9", "4EA5E6", "417EBF")


class GTKButton(QPushButton):
    """
    This is a gtk styled button.
    """
    def __init__(self, button_type, *args, **kwargs):
        """
        :param button_type:
        The type of the button, i.e. red, green, blue. Defined by a constant
        """
        super().__init__(*args, **kwargs)
        self.setStyleSheet(button_type)
