#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os

init = QWidget.__init__
show = QWidget.show
_hide = QWidget.hide

def _show_(self, *args, **kwargs):
    self.visibility = True
    if not os.getenv('TESTING'):
        show(self, *args, **kwargs)

def _hide_(self, *args, **kwargs):
    self.visibility = False
    if not os.getenv('TESTING'):
        _hide(self)

def _init_(self, *args, **kwargs):
    self.visibility = False
    init(self, *args, **kwargs)

QWidget.__init__ = _init_
QWidget.show = _show_
QWidget.hide = _hide_