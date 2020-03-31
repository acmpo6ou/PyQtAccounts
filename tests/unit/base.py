#!/usr/bin/env python3

from PyQt5.QtWidgets import *
import unittest
import pytest
import sys
import os

sys.path.append('.')

from PyQtAccounts import *


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.window = Window()
        self.dbs = self.window.dbs

    def tearDown(self):
        self.window.destroy = True
        self.window.close()

    @pytest.fixture(autouse=True)
    def monkeypatching(self, monkeypatch):
        self.monkeypatch = monkeypatch

    def file_dialog(self, result):
        def file_dialog(caption, filter, directory):
                assert caption == 'Імпортувати базу данних'
                assert filter == 'Tarball (*.tar)'
                assert directory == os.getenv('HOME')
                return result
        return file_dialog

    def save_file_dialog(self, name, result):
        def save_file_dialog(caption, filter, directory):
                home = os.getenv('HOME')
                assert caption == 'Експортувати базу данних'
                assert filter == 'Tarball (*.tar)'
                assert directory == f'{home}/{name}.tar'
                return result
        return save_file_dialog

    def mess(self, head, text, button=QMessageBox.Ok):
        def mess(parent, this_head, this_text, *args, **kwargs):
                assert this_head == head
                assert this_text == text
                return button
        return mess

    def critical(self, parent, head, text):
        assert head == 'Помилка!'
        return QMessageBox.Ok
