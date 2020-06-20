#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("PyQt5")
window.resize(1000, 500)
box = QHBoxLayout()
box.addWidget()
window.setLayout(box)
window.show()
sys.exit(app.exec_())