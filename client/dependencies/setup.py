# -*- coding:utf-8 -*-
import os
from sys import platform


def main():
    """
    Server installation script and deploy for windows, linux and osx
    :return:
    """
    if platform.startswith('win32'):
        os.system('virtualenv ./env')
        os.system('/env/scripts/activate')
        os.system('pip install -r temp/requeriments.txt')
        os.system('pip install pypiwin32')
        os.system('pip install pycrypto')

    elif platform.startswith('linux2') or platform.startswith('darwin'):
        os.system('pip install virtualenv')
        os.system('virtualenv env')
        os.system('source env/bin/activate')
        os.system('pip install -r temp/requeriments.txt')
        os.system('pip install pycrypto')


if __name__ == '__main__':
    main()