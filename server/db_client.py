# -*- coding: utf-8 -*-
from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from server import config


class DbClient(object):

    def __init__(self):
        self.cnx = None
        self.cursor = None
        try:
            self.cnx = mysql.connector.connect(user=config.user, password=config.password,
                                               host=config.host,
                                               database=config.database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = self.cnx.cursor()

    def get_connection(self):
        """
        Returns mysql connection
        :return: connection
        """
        return self.cnx

    def get_cursor(self):
        """
        Returns mysql connection cursor
        :return: cursor
        """
        return self.cursor

    def add_data(self, data_usr):
        success = False
        if self.cnx is not None and self.cursor is not None:
            if data_usr:
                add_usr = ("INSERT INTO clients"
                           "(ipclient, cpu, memory, uptime, sec_logs, email)"
                           "VALUES (%(ipclient)s, %(cpu)s, %(memory)s, %(uptime)s, %(sec_logs)s, %(email)s)")
                self.cursor.execute(add_usr, data_usr)
                self.cnx.commit()
                self.cursor.close()
                self.cnx.close()
                success = True
            else:
                print('The user data query is empty')
        else:
            print('Could not connect to the database')
        return success