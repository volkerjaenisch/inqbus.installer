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