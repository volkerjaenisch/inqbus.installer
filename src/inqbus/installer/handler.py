from task import Task

from fabric.colors import green, red, yellow
from fabric import api
from fabric.context_managers import prefix, cd
from fabric.contrib import files
from fabric.operations import run, prompt

import os
import sys
import subprocess

class LocalGlobalPackageHandler(object):
    
    def __init__(self, install_command, check_cmd):
        self.packages = []
        self.install_command = install_command
        self.check_cmd = check_cmd
    
    def add(self, package):
        self.packages.append(package)
    
    def install(self):
        packages_to_install = []
        for package in self.packages:
            with api.settings(warn_only=True):
                output = run(self.check_cmd % package)
            if output.return_code != 0:
                packages_to_install.append(package)
        if len(packages_to_install) > 0:
                print(red('Installation of global packages' +
                          'requires root password.'))
                run(self.install_command % ' '.join(packages_to_install))
        
    