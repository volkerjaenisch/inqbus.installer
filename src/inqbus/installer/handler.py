import os
import sys
import subprocess

from task import TaskMixin

from fabric.colors import green, red, yellow
from fabric import api
from fabric.context_managers import prefix, cd
from fabric.contrib import files
from fabric.operations import run, prompt


class BaseHandler(object):
    """Baseclass for all handlers"""

    def __init__(self, name):
        self.name = name

    def install(self):
        pass


class LGP(TaskMixin):
    """Handlerclass to install global packages on the local system."""

    def __init__(self, name, install_command, check_cmd):
        self.name = name
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


class Anaconda(TaskMixin):
    """Handler to install anaconda"""

    def __init__(self, name):
        self.name = name
        self.home_dir = os.path.join('/', 'home', api.env.user)
        self.install_dir = os.path.join(self.home_dir, 'anaconda')
        self.install_url = '09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b0' + \
                           '0b39d1d3.r79.cf1.rackcdn.com/Anaconda-1.8.0-' + \
                           'Linux-x86_64.sh'

    def install(self):
        print(green('Installing Anaconda'))
        path = prompt('Please enter the path where Anaconda should be' +
                      ' installed (default is %s): ' % self.install_dir)
        if path:
            self.install_dir = path

        with api.settings(warn_only=True):
            ls_anaconda = run('ls %s' % self.install_dir)
            if ls_anaconda.return_code == 0:
                print(yellow('It seems that Anaconda is already installed ' +
                             'or the target directory already exists. ' +
                             'Skipping installation'))
                return
            elif ls_anaconda.return_code == 2:
                pass
            else:
                # print error to User and Exit
                print ls_anaconda
                raise System.Exit()

        prefix_parent = os.path.abspath(os.path.join(self.install_dir,
                                                     os.pardir))
        with cd(prefix_parent):
            run('wget %s' % self.install_url)
            run('chmod 755 Anaconda*')
            # FIXME: looks ugly; bash script name can be extracted from url
            run('./Anaconda* -b -p %s' % env.ac_prefix)
        print(green('Successfully installed Anaconda'))


class UpdateBashrc(TaskMixin):
    """Handler to add content to the .bashrc"""

    def __init__(self, name):
        self.name = name
        self.home_dir = os.path.join('/', 'home', api.env.user)
        self.bashdir = os.path.join(self.home_dir, '.bashrc')
        self.content_to_add = []

    def install(self):
        for testline, addline in self.content_to_add:
            if not files.contains(self.bashdir, testline) or not testline:
                print(green('Going to add\n:' + addline))
                files.append(self.bashdir, addline)
            else:
                print('Seems like the file was already updated.')
                print(yellow('Please check, if settings are correct.'))
                print('.bashrc should contain:')
                print(addline)
        self.updatebash()

    def updatebash(self):
        run('source %s' % self.bashdir)

    def add(self, addline, testline=None):
        self.content_to_add.append((testline, addline))
