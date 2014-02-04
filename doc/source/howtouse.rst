How to use
==========

How to install
--------------

How to setup an installation
----------------------------

Read Parameters
^^^^^^^^^^^^^^^

Before you can start setting up your installation, you have to read the
commandline parameters. There are three optional parameters you can use:

  * *-H [user@ip]* for a remote installation - default is *localhost*
  * *-p [system|anaconda]* for using a special python - default is *system*
  * *-v [name]* for using a virtual environment  with the given name - default 
  is not using one

You can read these parameters using the method *parse_arguments*.

After this you have to run the method *get_registry_key*. This method takes
the arguments given by the commandline and returns a registry_key, which
describes the system, where the installation is running. It configures some
fabric-settings, too.

Your deployment-file should look like this to do these things.::

  from inqbus.installer.registration import parse_arguments, get_registry_key
  
  
  args = parse_arguments()
  
  registry_key = get_registry_key(args)

Configure Handler
^^^^^^^^^^^^^^^^^

Configuring the handler means to build a valid instance of an handler-class.
Therefore you can use the predefined handler of this package or even build your
own ones. For more information about this, read the part: :doc:`handler`.

Register Handler
^^^^^^^^^^^^^^^^

Configuring a handler does not mean that the handler will be exectuted.
Therefore you have to register it to your installer-instance. More information
about the installer-class you can find here: :doc:`installer`.

For the handler-registration you first have to build an installer-instance.::

  from inqbus.installer.installer import Installer
  
  
  installer = Installer()

then you can register your handlers. For the registration you have to call the
register-method. This method takes a lot of arguments to specify the when the
handlers should be run.

#. Host: As host-argument you have to add the string 'localhost' or 'remote'.
#. Virtual environment: As virtualenv-argument you have to add 'y' for using
   one or 'n' for using no virtual environment.
#. Python: The next argument represents the used python. You can add 'system
   'or 'anaconda'.
#. Operating System: The next argument is the name of the operating system,
   e.g. 'debian' or 'ubuntu'.
#. Operating System Versions: This argument can be a list or a string. Here
   you can specify the different versions of the operating system like '7.3'
   or ['7.0', '7.1', '7.2', '7.3'] for debian.
#. The Handler: The last argument is a list of handler. Each element of this
   list is a tuple with two values. The first one is the handler-instance and
   the second one is the purpose. If you use the default settings, there the
   following purposes:
                  
   * 'globalpackages',
   * 'python',
   * 'updatebashrc',
   * 'virtualenv',
   * 'pythonpackages',
   * 'getcurrentproject'

   You can register more than one handler for one purpose or even no handler 
   for not needed purposes.

A total registration could look like this: ::

  from inqbus.installer.installer import Installer
  
  
  installer = Installer()
  
  handler1 = SomeHandler()
  handler2 = AnotherHandler('test')

  installer.register('localhost', 'y', 'anaconda', 'debian',
                     ['7.0', '7.1', '7.2', '7.3'],
                     [(handler1, 'globalpackages'),
                      (handler2, 'python')])

Start Installation
^^^^^^^^^^^^^^^^^^

To start the installation, you just have to call the install-method with the 
key as argument.::

  from inqbus.installer.registration import parse_arguments, get_registry_key
  from inqbus.installer.installer import Installer
  
  
  args = parse_arguments()
  
  registry_key = get_registry_key(args)
  
  installer = Installer()
  
  handler1 = SomeHandler()
  handler2 = AnotherHandler('test')

  installer.register('localhost', 'y', 'anaconda', 'debian',
                     ['7.0', '7.1', '7.2', '7.3'],
                     [(handler1, 'globalpackages'),
                      (handler2, 'python')])
                      
  installer.install(registry_key)

In this method the installer just takes the registered handlers which match the
settings given by the registry_key. Then it goes through all purposes and
starts their installation-process.
