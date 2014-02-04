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

Register Handler
^^^^^^^^^^^^^^^^

Start Installation
^^^^^^^^^^^^^^^^^^