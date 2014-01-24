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


# create a installer
maininstaller = Installer()

# register Handler
maininstaller.register_handler('localhost', 'y', 'system', 'debian', ['7.0', '7.1', '7.2', '7.3'],
                                [(VirtualenvHandler(args.venv_name), 'virtualenv'),
                                 (GlobalPackageLocalHandler(), 'globalpackages')])

maininstaller.register_handler('remote', 'n', 'anaconda', 'debian', ['7.0', '7.1', '7.2', '7.3'],
                                [(GlobalPackageRemoteHandler(args.host_ip), 'globalpackages')])

# parse commandline arguments
args = parse_arguments()

# get key from commandlinarguments
registry_key = get_registry_key(args)

maininstaller.install(registry_key)