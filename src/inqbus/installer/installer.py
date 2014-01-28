from task import TaskMixin


class Installer(object):

    def __init__(self):
        # dictionary to hold handler
        self.registered_handler = {}
        # list to hold all purposes for which a step can be added
        self.purposes = ['globalpackages', 'python', 'updatebashrc',
                         'virtualenv', 'pythonpackages', 'getcurrentproject']

    def install(self, registry_key):
        if registry_key in self.registered_handler:
            install_steps = self.registered_handler[registry_key]
            for purpose in self.purposes:
                print('Working on: %s' % purpose)
                # running handler
                for step in install_steps[purpose]:
                    if isinstance(step, TaskMixin):
                        step.runtask(step)
                    else:
                        step.install()
        else:
            print "No steps registered."

    def deinstall(self):
        pass

    def register(self, host, venv, p_version, os, versions, handlers):
        """Function to register handler in installing process."""
        if isinstance(versions, list):
            for version in versions:
                key = host + '_' + p_version + '_' + venv + '_' + os + version
                if key in self.registered_handler:
                    install_steps = self.registered_handler[key]
                else:
                    # initialise install_steps
                    install_steps = {}
                    for purpose in self.purposes:
                        install_steps[purpose] = []
                    self.registered_handler[key] = install_steps
                for handler, purpose in handlers:
                    install_steps[purpose].append(handler)
        else:
            key = host + '_' + p_version + '_' + venv + '_' + os + versions
            if key in self.registered_handler:
                install_steps = self.registered_handler[key]
            else:
                # initialise install_steps
                install_steps = {}
                for purpose in self.purposes:
                    install_steps[purpose] = []
                self.registered_handler[key] = install_steps
            for handler, purpose in handlers:
                install_steps[purpose].append(handler)
