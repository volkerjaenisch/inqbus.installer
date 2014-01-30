import platform
import os

from argparse import ArgumentParser

from fabric.api import env
from fabric import api
from fabric.context_managers import prefix
from fabric.operations import run


def get_registry_key(args):
    if args.venv_name:
        venv = 'y'
    else:
        venv = 'n'

    if args.host_ip and args.host_ip != 'localhost':
        host = 'remote'
        env.host_string = args.host_ip
    else:
        host = 'localhost'
        env.host_string = '127.0.0.1'

    os_name, os_version, os_id = platform.dist()
    os_key = os_name + os_version
    
    if args.python == 'system' and args.venv_name:
        home = os.path.join('/', 'home', api.env.user)
        with prefix('cd %s' % home):
            workon_home = run('cat .bashrc | grep WORKON_HOME')
        with prefix(workon_home):
            env.workon_home = run('echo $WORKON_HOME')
    else:
        env.workon_home = "~/.virtualenvs"
    
    if env.workon_home == '':
        env.workon_home = "~/.virtualenvs"
    
    print env.workon_home

    registry_key = host + '_' + args.python + '_' + venv + '_' + os_key
    return registry_key


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-p", "--python",
                        action="store",
                        help="select your Python [system|anaconda]",
                        dest="python", default='system')

    parser.add_argument("-v", "--virtuelenv",
                        action="store",
                        help="selct a virtualenv name",
                        dest="venv_name", default='')

    parser.add_argument("-H", "--host",
                        action="store",
                        help="select the host_ip",
                        dest="host_ip", default='')

    args = parser.parse_args()
    return args
