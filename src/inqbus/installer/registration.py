from handler import VirtualenvHandler, GlobalPackageLocalHandler, \
                    GlobalPackageRemoteHandler
from installer import Installer

from sys import argv

# reading parameter
if '-h' in argv:
    host_ip = argv[argv.index('-h') + 1]
    host = 'remote'
else:
    host = 'localhost'
    host_ip = None

if '-p' in argv:
    python = argv[argv.index('-p') + 1]
else:
    python = 'system'

if '-v' in argv:
    venv_name = argv[argv.index('-v') + 1]
    venv = 'y'
else:
    venv = 'n'
    venv_name = None


handler_to_register = {}
# add a combination for all supported parameters
handler_to_register['localhost_system_y'] = [VirtualenvHandler(venv_name).install,
                                             GlobalPackageLocalHandler().install]
handler_to_register['remote_anaconda_n'] = [GlobalPackageRemoteHandler(host_ip).install]

# create a installer
maininstaller = Installer()

# get the key out of the arguments given
registry_name = host + '_' + python + '_' + venv

# register all handlers for the given arguments
if registry_name in handler_to_register:
    for handler in handler_to_register[registry_name]:
        maininstaller.register(handler)
else:
    print('Parameters are not supported.')

maininstaller.install()