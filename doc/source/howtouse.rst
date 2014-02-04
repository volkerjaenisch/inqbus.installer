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



Start Installation
^^^^^^^^^^^^^^^^^^