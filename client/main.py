# -*- coding:utf-8 -*-
from __future__ import print_function
import os
import sys
import time
import psutil
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


"""
if sys.platform.startswith('win32'):
    import win32con
    import win32evtlog
    import win32evtlogutil
    import winerror
    import codecs
"""


def clean_screen():
    if psutil.POSIX:
        os.system('clear')
    else:
        os.system('cls')


class SystemInfo (object):

    def __init__(self):
        self.cpu = 0.0
        self.memory = 0.0
        self.uptime = 0
        self.logs = None

    def update(self):
        """
        Function to collect the client data
        :return:
        """
        self.cpu = self.get_cpu()
        self.memory = self.get_memory()
        self.uptime = self.get_uptime()
        # if not psutil.POSIX:
        #    self.get_logs()

    def get_cpu(self):
        """
        System usage
        :return: integer cpu usage (including all cores)
        """
        return psutil.cpu_percent(interval=1)

    def get_memory(self):
        """
        Total system memory usage
        :return: integer memory usage
        """
        memory = psutil.virtual_memory()
        return getattr(memory, 'percent')

    def get_uptime(self):
        """
        Get system uptime
        :return: integer (minutes)
        """
        seconds = int(time.time()) - int(psutil.boot_time())
        return seconds/60


def main():
    clean_screen()
    key = None
    # Open server public key
    f = open('temp/publickey.pem', 'r')
    key = RSA.importKey(f.read())
    # Get client computer info
    system_info = SystemInfo()
    cpu_load = system_info.get_cpu()
    mem_load = system_info.get_memory()
    uptime = system_info.get_uptime()
    msg = ' '.join([str(cpu_load), str(mem_load), str(uptime)])
    # cipher client computer info and save it into a file
    cipher = PKCS1_OAEP.new(key)
    ciphered = cipher.encrypt(msg)
    f = open('temp/results.txt', 'w')
    f.write(ciphered)
    f.close()


if __name__ == '__main__':
    main()