#!/usr/bin/env python3
import os
import signal

from bash import bash

pid = bash("pidof PyQtAccounts").stdout
pid = int(pid)
os.kill(pid, signal.SIGUSR1)
