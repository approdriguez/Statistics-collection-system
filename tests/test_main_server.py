from unittest import TestCase
import unittest

class TestLoad_main(TestCase):

    def test_load_clients(self):
        from server import main

        clients, alerts = main.load_clients('../server/data/clients.xml')
        self.assertIsNotNone(clients) and self.assertIsNotNone(alerts)

    def test_generate_keys(self):
        from server import main
        keys = main.generate_keys()
        self.assertIsNotNone(keys)

    def test_validator(self):
        from server import main
        _list = [-2.0, 20.0, 40]
        cpu, mem, uptime, logs = main.validator(_list)
        self.assertEqual(cpu, 0.0)

    def test_create_db_data(self):
        from server import main
        db_data = dict(ipclient='127.0.0.0', cpu=10.0, memory=10.0, uptime=10, sec_logs='', email='')
        _list = [10.0, 10.0, 10]
        dictionay = {
            'ip': '127.0.0.0',
            'mail': ''
        }
        test_dict = main.create_db_data(dictionay, _list)
        self.assertEqual(db_data, test_dict)

    def test_send_email(self):
        from server import main
        success = main.send_email('memory', '50', '')
        self.assertTrue(success)

    def send_alerts(self):
        from server import main
        db_data = dict(ipclient='127.0.0.0', cpu=10.0, memory=10.0, uptime=10, sec_logs='', email='')
        _alert_list = [dict(type='cpu', limit='50%')]
        success = main.send_alerts(db_data, _alert_list)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()