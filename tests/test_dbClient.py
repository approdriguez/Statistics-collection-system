from unittest import TestCase


class TestDbClient(TestCase):

    def test_get_connection(self):
        from server import db_client
        test_client = db_client.DbClient()
        connection = test_client.get_connection()
        self.assertIsNotNone(connection)

    def test_get_cursor(self):
        from server import db_client
        test_client = db_client.DbClient()
        cursor = test_client.get_cursor()
        self.assertIsNotNone(cursor)

    def test_add_data(self):
        db_data = {
            'ipclient': '127.0.0.0',
            'cpu': 0.0,
            'memory': 0.0,
            'uptime': 0,
            'sec_logs': '',
            'email': 'test@test.com',
        }
        from server import db_client
        test_client = db_client.DbClient()
        sucess = test_client.add_data(db_data)
        self.assertTrue(sucess)

