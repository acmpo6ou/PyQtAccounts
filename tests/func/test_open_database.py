#!/usr/bin/env python3

import unittest
import pytest
import sys

sys.path.append('.')

from .base import BaseTest
from utils import *
from PyQtAccounts import *


class OpenDbTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.form = self.dbs.forms['open']
        self.list = self.dbs.list

    def test_form_show(self):
        # Bob wants to open his database, so he clicks at the `crypt` on the database list
        self.list.selected(Index('crypt'))

        # open database form appears
        self.checkOnlyVisible(self.form, self.dbs)

        # There is title that says `Відкрити базу данних crypt`
        self.assertIn('crypt', self.form.title.text())
