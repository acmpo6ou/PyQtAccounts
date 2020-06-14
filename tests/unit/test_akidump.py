#!/usr/bin/env python3

# Copyright (c) 2020 Kolvakh B.
# This file is part of PyQtAccounts.

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

from core.akidump import *

from unittest.mock import Mock
import pytest
import os
import json

from tests.base import UnitTest


class AkidumpTest(UnitTest):
    def setUp(self):
        """
        Here we reassign some widely used variables.
        """
        # Tom has database with gmail account
        account = Account(account='gmail',
                          name='Tom',
                          email='tom@gmail.com',
                          password=b'123',
                          date='01.01.1990',
                          comment='My gmail account.',
                          copy_email=True)
        self.db = {'gmail': account}

    def test_account_serialization(self):
        """
        Here we test how json will serialize our Account class.
        """
        dump = json.dumps(self.db['gmail'].to_dict())
        self.assertEqual(dump, '{}')

    def test_dumps(self):
        """
        Here we test dumps function from akidump.py module.
        """

        # here we use dumps function for akidump.py module to serialize his
        # account
        dump = dumps(self.db)

        # then we check that it is dumped appropriately
        self.assertEqual(
            dump, '{"gmail": {"account": "gmail", "name": "Tom", "email": '
            '"tom@gmail.com", "password": "123", "date": "01.01.1990"}}',
            "Serialization of `dumps` function from core.akidump module is incorrect!"
        )
