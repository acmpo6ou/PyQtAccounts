#!/usr/bin/env python3

import unittest

class RunShTest(unittest.TestCase):
    '''
    We don't want to accidentally push run.sh with incorrect paths.
    '''
    def setUp(self):
        self.file = open('run.sh').read()

    def test_run_sh_path(self):
        self.assertIn('cd .', self.file)

    def test_run_sh_pythonpath(self):
        self.assertIn('export PYTHONPATH="$PYTHONPATH:./"', self.file)