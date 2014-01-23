from argparse import ArgumentParser

from handler import VirtualenvHandler, GlobalPackageLocalHandler, \
                    GlobalPackageRemoteHandler
from installer import Installer

def get_registry_key(args):
    if args.venv_name:
        venv = 'y'
    else:
        venv = 'n'
    
    if args.host_ip:
        host = 'remote'
    else:
        host = 'localhost'
    
    registry_key = host + '_' + args.python + '_' + venv
    return registry_key

# reading parameter
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


handler_to_register = {}
# add a combination for all supported parameters
handler_to_register['localhost_system_y'] = [VirtualenvHandler(args.venv_name).install,
                                             GlobalPackageLocalHandler().install]
handler_to_register['remote_anaconda_n'] = [GlobalPackageRemoteHandler(args.host_ip).install]

# create a installer
maininstaller = Installer()

# get the key out of the arguments given
registry_key = get_registry_key(args)

# register all handlers for the given arguments
if registry_key in handler_to_register:
    for handler in handler_to_register[registry_key]:
        maininstaller.register(handler)
else:
    print('Parameters are not supported.')

maininstaller.install()