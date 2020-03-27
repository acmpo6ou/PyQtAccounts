#!/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtTest import QTest
import unittest
import pytest
import sys

sys.path.append('.')

from PyQtAccounts import *

@pytest.fixture()
def win():
    return Window()