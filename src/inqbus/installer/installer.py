class Installer(object):

    def __init__(self):
        # dictionary to hold handler
        self.install_steps = {}
        # list to hold all purposes for which a step can be added
        self.purposes = ['globalpackages', 'python', 'virtualenv', 'pythonpackages',
                         'getcurrentproject', 'updatebashrc']
        # initialise install_steps
        for purpose in self.purposes:
            self.install_steps[purpose] = []

    
    def install(self):
        for purpose in self.purposes:
            print('Working on: %s' % purpose)
            # running handler
            for step in self.install_steps[purpose]:
                step()


    def deinstall(self):
        pass


    def register(self, install_step, purpose):
        if purpose in self.purposes:
            # add the handler install_step to the list of handlers
            self.install_steps[purpose].append(install_step)
        else:
            print('Could not register step for purpose: %s' % purpose)