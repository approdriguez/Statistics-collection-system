# -*- coding:utf-8 -*-
from __future__ import print_function
import os
import paramiko
import xml.etree.ElementTree as ET
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from server import config, db_client
import smtplib


def load_clients(path):
    """
    Load clients from an xml file
    :param path:
    :return: list of clients
    """
    clients = []
    alerts = []
    alerts_client = []
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(path, parser=parser)
    if tree is None:
        print('Could not find :', path)
    else:
        root = tree.getroot()
        for user in root:
            print(user.tag, user.attrib)
            for alert in user:
                print(alert.tag, alert.attrib)
                alerts_client.append(alert)
            alerts.append(alerts_client)
            clients.append(user)

    return clients, alerts


def connect(client):
    """
    Make a ssh conection with each client
    :param client: dictionary
    :return:
    """
    hostname = client.get('ip')
    username = client.get('username')
    password = client.get('password')
    port = client.get('port')
    if port is not None:
        port = int(port)

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())

        client.connect(hostname=hostname, port=port, username=username, password=password)
        stdin, stdout, stderr = client.exec_command('mkdir temp')
        stdin, stdout, stderr = client.exec_command('cd temp')
        sftp = client.open_sftp()
        # copy files
        copy_files_client(sftp, config.get_server, config.get_client)
        # execute setup
        print('Installing and downloading dependencies...this may take a while')
        stdin, stdout, stderr = client.exec_command('python temp/setup.py')
        print(stdout.read(), stderr.read())
        # execute client info
        stdin, stdout, stderr = client.exec_command('python temp/mainClient.py')
        print(stdout.read(), stderr.read())

    except paramiko.ssh_exception.NoValidConnectionsError:
        print('Couldnt establish connection to client ', hostname)

    finally:

        sftp.get('temp/results.txt', 'data/results.txt')
        client.exec_command('del temp/publickey.pem')
        client.exec_command('del temp/results.txt')
        client.exec_command('rd /s /q temp')
        sftp.close()
        client.close()


def copy_files_client(sftp, _paths_server, _paths_client):
    """
    Copy files from a server to a client using sftp
    :param sftp:
    :param _paths_server:
    :param _paths_client:
    :return:
    """
    for path_server, path_client in zip(_paths_server, _paths_client):
        sftp.put(path_server, path_client)


def generate_keys():
    """
    Generate a pair RSA keys
    :return: key
    """
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    private_key = key.exportKey()
    public_key = key.publickey()
    f = open('../client/dependencies/publickey.pem', 'w')
    f.write(public_key.exportKey(format='PEM'))
    f.close()
    return key


def decrypt(key, msgpath):
    """
    Decrypt the message from the client (RSA)
    :param key:
    :param msgpath:
    :return: (String) Decrypted message
    """
    cipher = PKCS1_OAEP.new(key)
    f = open(msgpath, 'r')
    encrypted_message = f.read()
    message = cipher.decrypt(encrypted_message)
    return message


def validator(sysinfo):
    """
    Client info validator
    :param sysinfo:
    :return:
    """
    cpu = 0.0
    mem = 0.0
    uptime = 0
    logs = ''
    if len(sysinfo) >= 3:
        cpu = float(sysinfo[0])
        mem = float(sysinfo[1])
        uptime = sysinfo[2]
        logs = ''
        if len(sysinfo) == 4:
            logs = str(sysinfo[3])
        try:
            float(cpu)
            float(mem)
            int(uptime)
        except ValueError:
            print('Invalid info received from the client')
        finally:
            if cpu < 0.0:
                cpu = 0.0
            if mem < 0.0:
                mem = 0.0
            if uptime < 0:
                uptime = 0
    return cpu, mem, uptime, logs


def create_db_data(client, sysinfo):
    """
    Validate decrypted client info and creates a db dictionary
    :param client:
    :param sysinfo:
    :return:
    """
    db_data = {}

    cpu, mem, uptime, logs = validator(sysinfo)

    db_data = {
        'ipclient': client.get('ip'),
        'cpu': cpu,
        'memory': mem,
        'uptime': uptime,
        'sec_logs': logs,
        'email': client.get('mail'),
    }

    return db_data


def clean_temp_files(data_path, key_path):
    """
    Clean server temp files
    :param data_path:
    :param key_path:
    :return:
    """
    os.system('rm ' + data_path)
    os.system('rm ' + key_path)


def send_email(type, limit, email):
    """
    Send email alert to a given adress
    :param type: string
    :param limit: int
    :param email: string
    :return:
    """
    gmail_user = config.gmail_user
    gmail_pwd = config.gmail_pwd
    FROM = gmail_user
    TO = email
    SUBJECT = 'System alert'
    TEXT = 'Your ' + str(type) + 'has exceded the limit ' + str(limit) + ', please close some apps'
    sucess = False
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
      """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
        sucess = True
    except:
        print('failed to send mail')

    return sucess


def send_alerts(data_usr, alert_list):
    success = True
    email = data_usr.get('email')
    limit = 0.0
    print('CPU: ', data_usr.get('cpu'))
    print('Memory: ',data_usr.get('memory'))
    for alert in alert_list:
        sys_data = data_usr.get(alert.get('type'))
        type = alert.get('type')
        # convert percentage string i.e '50%' to 50.0
        limit = float(alert.get('limit').strip('%'))
        # check if the limit has been exceeded
        if sys_data > limit:
            print('The limit has been exceded, sending email')
            success = send_email(type, limit, email)
    return success


def main():
    clean_temp_files(config.encrypted_data_path, config.public_key_path)
    print('Generating keys...')
    key = generate_keys()
    print('Loading targets...')
    clients, alerts = load_clients('data/clients.xml')
    for client, alert_list in zip(clients, alerts):
        # connecting to the client
        connect(client)
        # decrypting client message
        message_decrypted = decrypt(key, config.encrypted_data_path)
        sysinfo = message_decrypted.split()
        data_usr = create_db_data(client, sysinfo)
        # storing client info into the database
        db = db_client.DbClient()
        db.add_data(data_usr)
        # sending alerts
        send_alerts(data_usr, alert_list)
    clean_temp_files(config.encrypted_data_path, config.public_key_path)


if __name__ == '__main__':
    main()
