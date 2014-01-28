from task import TaskMixin

import os
import platform
import sys
from contextlib import contextmanager

from fabric.colors import green, red, yellow
from fabric import api
from fabric.api import env
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
            run('./Anaconda* -b -p %s' % self.install_dir)
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


class AnacondaVenv(TaskMixin):
    """Handler to create a virtualenv using Anaconda"""

    def __init__(self, name, env_name, anaconda_path):
        self.name = name
        self.env_name = env_name
        self.workon_home = os.path.join(anaconda_path, 'envs')

    def install(self):
        print(green('Creating virtualenv "%s"' % self.env_name))
        if files.exists(os.path.join(self.workon_home, self.env_name)):
            print(yellow('Virtual environment already exists. ' +
                         'Skipping creation.'))
        else:
            run('conda create -n %s anaconda' % self.env_name)


class AnacondaPip(TaskMixin):
    """Handler to install pip-packages in virtualenv using Anaconda"""

    def __init__(self, name, env_name, ana_path):
        self.name = name
        self.env_name = env_name
        self.packages = []
        self.workon_cmd = 'source activate %s' % env_name
        self.env_bin_path = os.path.join(ana_path, 'bin')

    def install(self):
        with prefix('cd %s' % self.env_bin_path):
            with prefix(self.workon_cmd):
                for package in self.packages:
                    print(green('Installing %s via pip' % package))
                    run('pip install %s' % package)

    def add(self, package):
        self.packages.append(package)


class GitClone(object):
    """Handler to clone project from github"""

    def __init__(self, name, repo_name, repo, branch, path):
        self.name = name
        self.repo_path = os.path.join(path, repo_name)
        self.repo = repo
        self.branch = branch
        self.repo_name = repo_name

        self.packages = []

    def install(self):
        # check if we may already have a cloned repo here
        if files.exists(self.repo_path):
            print(yellow('Found existing %s repository' % self.repo_name))
            # check if the repo is valid by trying to pull
            print(yellow('Try to update it'))
            with prefix("cd " + self.repo_path):
                run('git pull')
            print(green('%s update successfull' % self.repo_name))
        else:
            print(green('Fetching %s repository from github' % self.repo_name))
            run('git clone -b %s %s' % (self.branch, self.repo))


class AnacondaProject(object):
    """Handler install a github-project in AnacondaVenv"""

    def __init__(self, name, repo_name, ana_path, env_name):
        self.name = name
        self.repo_path = os.path.join(ana_path, 'envs', env_name, repo_name)
        self.repo_name = repo_name
        self.workon_cmd = 'source activate %s' % env_name
        self.env_bin_path = os.path.join(ana_path, 'bin')

        self.packages = []

    def install(self):
        print(green('Installing %s packages' % self.repo_name))
        for package in self.packages:
            print(green('Installing %s package: %s' % (self.repo_name,
                                                       package)))
            with prefix('cd %s' % self.env_bin_path):
                with prefix(self.workon_cmd):
                    with prefix("cd " + self.repo_path):
                        with prefix("cd " + package):
                            run('python setup.py develop')
        print(green('%s Installation successfull' % self.repo_name))

    def add(self, package):
        self.packages.append(package)
