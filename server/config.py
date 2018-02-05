# -*- coding: utf-8 -*-
"""Project config and paths

Project paths.
"""
# Config (db)
user = 'root'
password = ''
host = '127.0.0.1' #local database
database = 'monitor'

# Mail
gmail_user = ''
gmail_pwd = ''

# Paths
encrypted_data_path = 'data/results.txt'
public_key_path = '../client/dependencies/publickey.pem'
clients_path = 'data/clients.xml'
# sftp get
get_server = ['../client/main.py', '../client/dependencies/requeriments.txt', '../client/dependencies/setup.py', '../client/dependencies/publickey.pem']
get_client = ['temp/mainClient.py', 'temp/requeriments.txt','temp/setup.py', 'temp/publickey.pem']

