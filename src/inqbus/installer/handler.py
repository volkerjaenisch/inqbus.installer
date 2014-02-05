from task import TaskMixin

import os
from contextlib import contextmanager

from fabric.colors import green, red, yellow
from fabric import api
from fabric.api import env
from fabric.context_managers import prefix, cd
from fabric.contrib import files
from fabric.operations import run, prompt


@contextmanager
def prepare_venv():
    """Function to prepare working with virtualenvironment."""
    with prefix("source /etc/bash_completion.d/virtualenvwrapper"):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix("export WORKON_HOME=%s" % env.workon_home):
                yield


class BaseHandler(object):
    """Baseclass for all handlers"""

    def __init__(self, name):
        self.name = name

    def install(self):
        pass


class Global(TaskMixin):
    """Handlerclass to install global packages."""

    def __init__(self, name, install_command, check_cmd=None):
        self.name = name
        self.packages = []
        self.install_command = install_command
        self.check_cmd = check_cmd

    def add(self, package):
        self.packages.append(package)

    def install(self):
        packages_to_install = []
        for package in self.packages:
            if self.check_cmd:
                with api.settings(warn_only=True):
                    output = run(self.check_cmd % package)
                if output.return_code != 0:
                    packages_to_install.append(package)
            else:
                packages_to_install = self.packages
        if len(packages_to_install) > 0:
                print(red('Installation of global packages ' +
                          'requires root password.'))
                run(self.install_command % ' '.join(packages_to_install))


class RunGlobal(TaskMixin):

    def __init__(self, name, command):
        self.name = name
        self.command = command

    def install(self):
        print(red('Running global command:\n%s' % self.command))
        with api.settings(warn_only=True):
            run(self.command)


class Anaconda(TaskMixin):
    """Handler to install anaconda"""

    def __init__(self, name):
        self.name = name
        self.home_dir = os.path.join('/', 'home', api.env.user)
        self.install_dir = os.path.join(self.home_dir, 'anaconda')
        self.system = prompt('Do you want to install 64-bit-version[64] or ' +
                             '32-bit-version[32]? (default is 64): ')
        if '32' in self.system:
            self.install_url = '09c8d0b2229f813c1b93-c95ac804525aac4b6dba' + \
                               '79b00b39d1d3.r79.cf1.rackcdn.com/' + \
                               'Anaconda-1.8.0-Linux-x86.sh'
        else:
            self.install_url = '09c8d0b2229f813c1b93-c95ac804525aac4b6dba' + \
                               '79b00b39d1d3.r79.cf1.rackcdn.com/' + \
                               'Anaconda-1.8.0-Linux-x86_64.sh'

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
            run('rm ./Anaconda*')
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
                print(green('Going to add:\n' + addline))
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
        self.anaconda_path = anaconda_path
        self.workon_home = os.path.join(anaconda_path, 'envs')

    def install(self):
        print(green('Creating virtualenv "%s"' % self.env_name))
        if files.exists(os.path.join(self.workon_home, self.env_name)):
            print(yellow('Virtual environment already exists. ' +
                         'Skipping creation.'))
        else:
            with prefix('export PATH=%s/bin:$PATH' % self.anaconda_path):
                run('conda create -n %s anaconda' % self.env_name)


class AnacondaPip(TaskMixin):
    """Handler to install pip-packages in virtualenv using Anaconda"""

    def __init__(self, name, env_name, anaconda_path):
        self.name = name
        self.env_name = env_name
        self.packages = []
        self.anaconda_path = anaconda_path
        self.workon_cmd = 'source activate %s' % env_name

    def install(self):
        with prefix('export PATH=%s/bin:$PATH' % self.anaconda_path):
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
        self.path = path

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
            with prefix('cd %s' % self.path):
                run('git clone -b %s %s' % (self.branch, self.repo))


class AnacondaProject(object):
    """Handler install a project in AnacondaVenv"""

    def __init__(self, name, repo_name, repo_path, ana_path, env_name):
        self.name = name
        self.repo_path = os.path.join(repo_path, repo_name)
        self.repo_name = repo_name
        self.workon_cmd = 'source activate %s' % env_name
        self.anaconda_path = ana_path

        self.packages = []

    def install(self):
        print(green('Installing %s packages' % self.repo_name))
        for package in self.packages:
            print(green('Installing %s package: %s' % (self.repo_name,
                                                       package)))
            with prefix('export PATH=%s/bin:$PATH' % self.anaconda_path):
                with prefix(self.workon_cmd):
                    with prefix("cd " + self.repo_path):
                        with prefix("cd " + package):
                            run('python setup.py develop')
        print(green('%s Installation successfull' % self.repo_name))

    def add(self, package):
        self.packages.append(package)


class VenvWrapper(TaskMixin):
    """Handler to create a virtualenv using Virtualenv-Wrapper"""

    def __init__(self, name, env_name):
        self.name = name
        self.env_name = env_name
        self.env_path = os.path.join(env.workon_home, env_name)

    def install(self):
        print(green('Creating virtualenv "%s"' % self.env_name))
        if files.exists(self.env_path):
            print(yellow('Virtual environment already exists. ' +
                         'Skipping creation.'))
        else:
            with prepare_venv():
                run('mkvirtualenv %s' % self.env_name)


class WrapperPip(TaskMixin):
    """Handler to install Python-Packages using Virtualenv-Wrapper"""

    def __init__(self, name, env_name, additionalcmd=None):
        self.name = name
        self.packages = []
        self.workon_cmd = 'workon %s' % env_name
        self.additionalcmd = additionalcmd

    def install(self):
        for package in self.packages:
            print(green('Installing %s via pip' % package))
            with prepare_venv():
                with prefix(self.workon_cmd):
                    if self.additionalcmd:
                        with prefix(self.additionalcmd):
                            run('pip install %s' % package)
                    else:
                        run('pip install %s' % package)

    def add(self, package):
        self.packages.append(package)


class VenvProject(object):
    """Handler install a project using Virtualenv-Wrapper"""

    def __init__(self, name, repo_name, repo_path, env_name,
                 additionalcmd=None):
        self.name = name
        self.repo_path = os.path.join(repo_path, repo_name)
        self.repo_name = repo_name
        self.workon_cmd = 'workon %s' % env_name
        self.additionalcmd = additionalcmd

        self.packages = []

    def install(self):
        print(green('Installing %s packages' % self.repo_name))
        for package in self.packages:
            print(green('Installing %s package: %s' % (self.repo_name,
                                                       package)))
            with prepare_venv():
                with prefix(self.workon_cmd):
                    with prefix("cd " + self.repo_path):
                        with prefix("cd " + package):
                            if self.additionalcmd:
                                with prefix(self.additionalcmd):
                                    run('python setup.py develop')
                            else:
                                run('python setup.py develop')
        print(green('%s Installation successfull' % self.repo_name))

    def add(self, package):
        self.packages.append(package)


class VenvCommand(TaskMixin):
    """Handler to run commands within the virtualenv"""

    def __init__(self, name, env_name):
        self.name = name
        self.commands = []
        self.workon_cmd = 'workon %s' % env_name

    def add(self, command):
        self.commands.append(command)

    def install(self):
        for command in self.commands:
            with prepare_venv():
                with prefix(self.workon_cmd):
                    run(command)
