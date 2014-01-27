from inqbus.installer.installer import Installer
from inqbus.installer.registration import get_registry_key

import platform
import unittest


class A(object):
    def __init__(self):
        self.installed = False

    def install(self):
        self.installed = True


class B(object):
    def __init__(self):
        self.installed = False

    def install(self):
        self.installed = True


class C(object):
    def __init__(self):
        self.installed = False

    def install(self):
        self.installed = True


class Args(object):
    """Class to hold parameters which would be given by commandline"""
    def __init__(self):
        self.python = 'system'
        self.venv_name = ''
        self.host_ip = ''


class TestRegistration(unittest.TestCase):

    def test_get_registry_key(self):
        args = Args()
        generated_key = get_registry_key(args)
        os_name, os_version, os_id = platform.dist()

        expected_key = 'localhost_system_n_' + os_name + os_version

        self.assertEqual(expected_key, generated_key)

        args.host_ip = '192.168.2.1'
        args.python = 'anaconda'
        args.venv_name = 'test'
        generated_key = get_registry_key(args)
        os_name, os_version, os_id = platform.dist()

        expected_key = 'remote_anaconda_y_' + os_name + os_version

        self.assertEqual(expected_key, generated_key)


class TestInstaller(unittest.TestCase):

    def setUp(self):
        self.args_1 = Args()
        self.args_2 = Args()

        self.args_2.host_ip = '192.168.2.1'
        self.args_2.python = 'anaconda'
        self.args_2.venv_name = 'test'

        self.os_name, self.os_version, self.os_id = platform.dist()

        self.key_1 = get_registry_key(self.args_1)
        self.key_2 = get_registry_key(self.args_2)

        self.handler_a = A()
        self.handler_b = B()
        self.handler_c = C()

        self.installer = Installer()

    def test_register(self):
        self.installer.register('localhost', 'y', 'anaconda', self.os_name,
                                [self.os_version, '25.3'],
                                [(self.handler_a, 'python'),
                                 (self.handler_b, 'virtualenv')])

        self.installer.register('localhost', 'n', 'system', self.os_name,
                                [self.os_version],
                                [(self.handler_c, 'python'),
                                 (self.handler_a, 'virtualenv')])

        self.installer.register('remote', 'y', 'anaconda', self.os_name,
                                self.os_version,
                                [(self.handler_a, 'python'),
                                 (self.handler_b, 'python'),
                                 (self.handler_c, 'virtualenv')])

        handlers = self.installer.registered_handler[self.key_1]['python']
        assert(self.handler_c in handlers)
        assert(len(handlers) == 1)

        handlers = self.installer.registered_handler[self.key_2]['python']
        assert(self.handler_a in handlers)
        assert(self.handler_b in handlers)
        assert(len(handlers) == 2)

    def test_install(self):
        self.installer.register('localhost', 'n', 'system', self.os_name,
                                [self.os_version],
                                [(self.handler_c, 'python'),
                                 (self.handler_a, 'virtualenv')])

        self.installer.register('remote', 'y', 'anaconda', self.os_name,
                                self.os_version,
                                [(self.handler_a, 'python'),
                                 (self.handler_b, 'python'),
                                 (self.handler_c, 'virtualenv')])

        self.installer.install('unregistered_key')
        self.assertFalse(self.handler_a.installed)
        self.assertFalse(self.handler_b.installed)
        self.assertFalse(self.handler_c.installed)

        self.installer.install(self.key_1)
        self.assertTrue(self.handler_a.installed)
        self.assertTrue(self.handler_c.installed)
        self.assertFalse(self.handler_b.installed)

        self.handler_a.installed = False
        self.handler_c.installed = False

        self.installer.install(self.key_2)
        self.assertTrue(self.handler_a.installed)
        self.assertTrue(self.handler_b.installed)
        self.assertTrue(self.handler_c.installed)

    def tearDown(self):
        pass
