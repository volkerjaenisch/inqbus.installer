class Installer(object):

    def __init__(self):
        # list to hold handler
        self.install_steps = []

    
    def install(self):
        for install_step in self.install_steps:
            install_step()


    def deinstall(self):
        pass


    def register(self, install_step):
        # add the handler install_step to the list of handlers
        self.install_steps.append(install_step)