import platform
import os

from argparse import ArgumentParser

from fabric.api import env
from fabric import api
from fabric.context_managers import prefix
from fabric.operations import run
from fabric.colors import green


def get_registry_key(args):
    if args.venv_name:
        venv = 'y'
    else:
        venv = 'n'

    if args.host_ip and args.host_ip != 'localhost':
        host = 'remote'
        hostdata = args.host_ip.split('@')
        env.host_string = hostdata[1]
        env.user = hostdata[0]
    else:
        host = 'localhost'
        env.host_string = '127.0.0.1'

    os_name = run('lsb_release -i').split().pop().lower()
    os_version = run('lsb_release -r').split().pop()
    os_key = os_name + os_version
    print(green("Operating System is %s" % os_key))
    
    if args.python == 'system' and args.venv_name:
        home = os.path.join('/', 'home', api.env.user)
        with api.settings(warn_only=True):
            with prefix('cd %s' % home):
                workon_home = run('cat .bashrc | grep WORKON_HOME')
    
    if workon_home:
        with prefix(workon_home):
            env.workon_home = run('echo $WORKON_HOME')
    else:
        env.workon_home = "~/.virtualenvs"
    
    print(green("WORKON_HOME is %s" % env.workon_home))

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
                        help="select the host user@host_ip",
                        dest="host_ip", default='')

    args = parser.parse_args()
    return args
