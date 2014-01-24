from installer import Installer
from registration import parse_arguments, get_registry_key

# define some Handler who only print some lines
class VirtualenvHandler(object):
    
    def __init__(self, env_name):
        self.env_name = env_name
    
    def install(self):
        print('virtualenv would be created. Name: %s' % self.env_name)

class GlobalPackageLocalHandler(object):

    def install(self):
        print('Global packages would be installed locally.')
        
class GlobalPackageRemoteHandler(object):
    
    def __init__(self, host):
        self.host = host

    def install(self):
        print('Global packages would be remote installed. Host: %s' % self.host)


# reading parameter
args = parse_arguments()


handler_to_register = {}
# add a combination for all supported parameters
handler_to_register['localhost_system_y'] = [
                            (VirtualenvHandler(args.venv_name).install, 'virtualenv'),
                            (GlobalPackageLocalHandler().install, 'globalpackages')]
handler_to_register['remote_anaconda_n'] = [
                            (GlobalPackageRemoteHandler(args.host_ip).install, 'globalpackages')]

# create a installer
maininstaller = Installer()

# get the key out of the arguments given
registry_key = get_registry_key(args)

# register all handlers for the given arguments
if registry_key in handler_to_register:
    for handler, purpose in handler_to_register[registry_key]:
        maininstaller.register(handler, purpose)
else:
    print('Parameters are not supported.')

maininstaller.install()