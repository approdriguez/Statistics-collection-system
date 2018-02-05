from unittest import TestCase


class TestSystemInfo(TestCase):

    def test_get_cpu(self):
        from client import main
        obj_test = main.SystemInfo()
        cpu = obj_test.get_cpu()
        self.assertIsInstance(cpu, float)

    def test_get_memory(self):
        from client import main
        obj_test = main.SystemInfo()
        memory = obj_test.get_memory()
        self.assertIsInstance(memory, float)

    def test_get_uptime(self):
        from client import main
        obj_test = main.SystemInfo()
        uptime = obj_test.get_uptime()
        self.assertIsInstance(uptime, int)

    def test_update(self):
        self.test_get_cpu()
        self.test_get_memory()
        self.test_get_uptime()
