#!/usr/bin/env python3

import unittest

class RunShTest(unittest.TestCase):
    '''
    We don't want to accidentally push run.sh with incorrect path.
    '''
    def setUp(self):
        self.file = open('run.sh')

    def tearDown(self):
        self.file.close()