from installer import Installer
from task import TaskMixin
from registration import parse_arguments, get_registry_key


# define some Handler who only print some lines
class Venv(TaskMixin):
    """Pseudohandler representing the Handler to install the virtual
    environment"""

    def __init__(self, env_name):
        self.env_name = env_name

    def install(self):
        print('virtualenv would be created. Name: %s' % self.env_name)


class GLP(TaskMixin):
    """Pseudohandler representing the Handler to install global packages on
    the local system"""

    def install(self):
        print('Global packages would be installed locally.')


class GPR(object):
    """Pseudohandler representing the Handler to install global packages on
    the remote system"""

    def __init__(self, host):
        self.host = host

    def install(self):
        print('Global packages would be remote installed. Host: %s' %
              self.host)


# create a installer
maininstaller = Installer()

# parse commandline arguments
args = parse_arguments()

# register Handler
maininstaller.register('localhost', 'y', 'system', 'debian',
                        ['7.0', '7.1', '7.2', '7.3'],
                        [(Venv(args.venv_name), 'virtualenv'),
                         (GLP(), 'globalpackages')])

maininstaller.register('remote', 'n', 'anaconda', 'debian',
                       ['7.0', '7.1', '7.2', '7.3'],
                       [(GPR(args.host_ip), 'globalpackages')])

# get key from commandlinarguments
registry_key = get_registry_key(args)

maininstaller.install(registry_key)
