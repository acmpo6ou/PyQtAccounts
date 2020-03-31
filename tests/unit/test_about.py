#!/usr/bin/env python3

from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
from unittest.mock import Mock
import pytest
import sys

sys.path.append('.')

from .base import BaseTest
from core.utils import *
from PyQtAccounts import *
from core.windows import About
import git


class AboutTest(BaseTest):
    def setUp(self):
        super().setUp()

    def test_about_version(self):
        class Tag:
            def __init__(self, name, date):
                self.name = name
                self.commit = Mock()
                self.commit.committed_datetime = date
            def __str__(self):
                return self.name

        class Repo:
            def __init__(self, *args):
                pass
            tags = []
            for i, name in enumerate(['v1.0.0', 'v1.0.2', 'v2.0.6']):
                tags.append(Tag(name, i))

        self.monkeypatch.setattr(git, 'Repo', Repo)
        about = About()
        self.assertIn('Version 2.0.6', about.about)
