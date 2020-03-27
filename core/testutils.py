#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

init = QWidget.__init__
show = QWidget.show
hide = QWidget.hide

def _show_(self, *args, **kwargs):
    self.vis = True
    show(self, *args, **kwargs)

def _hide_(self, *args, **kwargs):
    self.vis = False
    hide(self, *args, **kwargs)

def _init_(self, *args, **kwargs):
    self.vis = False
    init(self, *args, **kwargs)

QWidget.__init__ = _init_
QWidget.show = _show_
QWidget.hide = _hide_