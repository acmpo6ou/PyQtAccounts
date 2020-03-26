#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import unittest
import pytest
import sys
import os

sys.path.append('./core')

from PyQtAccounts import main, window

def test_main_db(qtbot):
    main()
    assert window