#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from testutils import QWidget

import genpass
from utils import *


class Tip(QLabel):
    def __init__(self, text=''):
        QLabel.__init__(self, text)

        font = QFont('Ubuntu Mono', 18)

        self.setStyleSheet('color: #37FF91;')
        self.setFont(font)


class HelpTip(QLabel):
    def __init__(self, text=''):
        QLabel.__init__(self, text)
        self.setAlignment(Qt.AlignCenter)
        font = QFont('Ubuntu Mono', 18, QFont.StyleItalic)
        self.setFont(font)
        self.hide()


class WarningTip(HelpTip):
    def __init__(self, text=''):
        HelpTip.__init__(self, text)
        self.setStyleSheet('color: #be9117;')
        self.hide()


class Title(QLabel):
    def __init__(self, text=''):
        text = '<b>{}</b>'.format(text)
        QLabel.__init__(self, text)
        self.setAlignment(Qt.AlignHCenter)


class Error(QLabel):
    def __init__(self, text=''):
        QLabel.__init__(self, text)

        font = QFont('Ubuntu Mono', 18)

        self.setStyleSheet('color: #f26666;')
        self.setFont(font)


class Errors(QTextEdit):
    def __init__(self):
        QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.hide()
        self.setTextColor(QColor('#f26666'))


class PasswordField(QHBoxLayout):
    def __init__(self, placeholder=''):
        QHBoxLayout.__init__(self)

        self.passInput = QLineEdit()
        self.passInput.setPlaceholderText(placeholder)
        self.passInput.setEchoMode(QLineEdit.Password)

        self.showButton = QPushButton()
        self.showButton.setIcon(QIcon('../img/show.svg'))
        self.showButton.setIconSize(QSize(25, 25))
        self.showButton.clicked.connect(self.toggleShow)

        self.addWidget(self.passInput)
        self.addWidget(self.showButton)

    def toggleShow(self):
        if self.passInput.echoMode() == QLineEdit.Password:
            self.passInput.setEchoMode(QLineEdit.Normal)
            self.showButton.setIcon(QIcon('../img/hide.svg'))
        else:
            self.passInput.setEchoMode(QLineEdit.Password)
            self.showButton.setIcon(QIcon('../img/show.svg'))


class GenPassDialog(QDialog):
    def __init__(self, form):
        QDialog.__init__(self, form.parent())
        self.form = form
        self.setModal(True)
        self.setSizeGripEnabled(True)
        self.setWindowTitle('Згенерувати пароль')
        self.resize(700, 300)

        self.symLabel = QLabel('Довжина пароля: ')
        self.symNum = QSpinBox()
        self.symNum.setMinimum(8)
        self.symNum.setValue(16)
        self.symTip = Tip("Рекомендуємо вибирати число не меншне 16")

        self.symLayout = QHBoxLayout()
        self.symLayout.addWidget(self.symLabel)
        self.symLayout.addWidget(self.symNum)

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

        self.buttonCancel = QPushButton('Скасувати')
        self.buttonGenerate = QPushButton('Згенерувати')
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
        symbs = ''
        for box in self.digitsFlag, self.upperFlag, self.lowerFlag, self.punctuationFlag:
            flag = box.isChecked()
            if flag:
                symbs += box.name
        password = genpass.main(symbs, self.symNum.value())
        self.form.passField.passInput.setText(password)
        self.form.passRepeatField.passInput.setText(password)
        self.hide()
