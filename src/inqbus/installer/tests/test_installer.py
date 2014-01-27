from inqbus.installer.installer import Installer
from inqbus.installer.task import TaskMixin
from inqbus.installer.registration import get_registry_key

import platform
import unittest


class A(object):
    def __init__(self):
        self.installed = False
    
    def install(self):
        self.installed = True


class B(TaskMixin):
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


class TestInstaller(unittest.TestCase):
    
    def setUp(self):
        pass 
    
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
    
    def tearDown(self):
        pass