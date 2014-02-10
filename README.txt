Inqbus.installer
================

inqbus.installer is a modular framework for building installation routines for 
python based software.

It features:

* local and remote installation
* different python flavours
* different os/ os versions
* virtual env out of the box

So if you have a broad variety of platfforms, versions and python flavours 
your code has to support, inqbus.installer may be the framework to use.

How to install
--------------

This package can be downloaded from the PyPi.

Requirements
------------

This package requires:

* python>=2.7
* fabric

How it works
------------

The inqbus.installer follows a simple working order to install your 
python-project. This working order starts with preparing the Client with
all necessary global packages.

The next step is to install Anaconda-Python if it was chosen. 

After this it creates the virtual environment depending on the chosen python 
with all necessary Python-Packages. 

As last step it will clone or update your current project and install it in
development-mode.::

  $ python test.py -v elan
  ...
  Working on: globalpackages
  ...
  Working on: python
  ...
  Working on: updatebashrc
  ...
  Working on: virtualenv
  ...
  Working on: pythonpackages
  ...
  Working on: getcurrentproject
  ...

How to use inqbus.installer
---------------------------

Read Parameters
^^^^^^^^^^^^^^^

There are three optional parameters you can use:

* *-H [user@ip]* for a remote installation - default is *'localhost'*
* *-p [system|anaconda]* for using a special python - default is *'system'*
* *-v [name]* for using a virtual environment  with the given name - default 
  is not using one

All parameters are read in automatically. To use them, just import *args*
from the registration.

when the commandlinearguments are parsed, some fabric-settings are done, too.

The fabric-settings include setting the user and the host which are necessary
to install something with a fabric-script. On the other side it checks if the 
user has set a value for the environment-variable *WORKON_HOME*. If this is the
case has set this value, it is read and safed in *env.workon_home*. In the 
other case *env.workon_home* is set to a default value.

This example shows, how your deployment-file could look and how you can access
the value of *env.workon_home*.

.. code-block:: python

  from inqbus.installer.registration import args
  from fabric.api import env
  
  # to get WORKON_HOME
  workon_home = env.workon_home

Handlers
^^^^^^^^

One main part of inqbus.installer are the handlers. There are a lot of 
predefined handlers, e.g. to install global packages, like the following 
example.

.. code-block:: python

  from inqbus.installer.handler import Global
  
  
  globalpackage = Global('global', 'su -c "aptitude update && aptitude install %s"', 
                         'dpkg -s %s')
  
  globalpackage.add('python-pip')
  globalpackage.add('python-virtualenv')
  globalpackage.add('virtualenvwrapper')

On the other hand you can write your own handlers.

Each handler has to provide a install-method. It can also provide additional
functions especially the __init__-method, if you need them.

.. code-block:: python

  class Handler(object):
  
      def install(self):
          # do something
          pass

Some special handlers can inherit from the TaskMixin-Class. This class keeps 
care of steps which are already done in the installation. So if the 
installation breaks the completed steps will be skipped. Therefore you have 
to add an argument which is called self.name. One way to do this is setting 
it in the __init__-method.

.. code-block:: python

  from inqbus.installer.task import TaskMixin
  
  
  class Handler(TaskMixin):
  
      def __init__(self, name):
          self.name = name
  
      def install(self):
          # do something
          pass

Configure Handler
^^^^^^^^^^^^^^^^^

Configuring the handler means to build a valid instance of an handler-class.
Therefore you can use the predefined handler of this package or even build your
own ones. 

.. code-block:: python

  from inqbus.installer.handler import RunGlobal
  
  
  runglobal = RunGlobal('runglobal', 'su -c "pip uninstall virtualenvwrapper"')

The example above just shows how you can configure one build-in handler. 
this handler just takes a command and runs it globally.

Register Handler
^^^^^^^^^^^^^^^^

Configuring a handler does not mean that the handler will be exectuted.
Therefore you have to register it to the installer-instance. 

.. code-block:: python

  from inqbus.installer.installer import installer
  from inqbus.installer.handler import RunGlobal
  
  
  runglobal = RunGlobal('runglobal', 'su -c "pip uninstall virtualenvwrapper"')
  handler1 = SomeHandler()
  

  installer.register(host='localhost', venv='y', p_version='anaconda',
                     os='debian',
                     versions=['7.0', '7.1', '7.2', '7.3'],
                     handlers=[(runglobal, 'globalpackages'),
                               (handler1, 'python')])

The example above shows how to register handler.

For the handler-registration you first have to import the installer-instance.

Then you can register your handlers. For the registration you have to call the
register-method. This method takes a lot of arguments to specify when the
handlers should be run.

#. host: As host-argument you have to add the string 'localhost' or 'remote'.
#. venv: As virtualenv-argument you have to add 'y' for using
   one or 'n' for using no virtual environment.
#. p_version: The next argument represents the used python. You can add 'system' 
   or 'anaconda'.
#. os: The next argument is the name of the operating system,
   e.g. 'debian' or 'ubuntu'.
#. versions: This argument can be a list or a string. Here
   you can specify the different versions of the operating system like '7.3'
   or ['7.0', '7.1', '7.2', '7.3'] for debian.
#. handlers: The last argument is a list of handler. Each element of this
   list is a tuple with two values. The first one is the handler-instance and
   the second one is the purpose. If you use the default settings, there are 
   the following purposes:
                  
   * 'globalpackages',
   * 'python',
   * 'updatebashrc',
   * 'virtualenv',
   * 'pythonpackages',
   * 'getcurrentproject'

   You can register more than one handler for one purpose or even no handler 
   for not needed purposes.

Start Installation
^^^^^^^^^^^^^^^^^^

To start the installation, you just have to call the install-method.

.. code-block:: python
                      
  installer.install()

In this method the installer just takes the registered handlers which match the
settings automatically given by the registry_key. Then it goes through all 
purposes and starts their installation-process.

Complete Documentation
^^^^^^^^^^^^^^^^^^^^^^

The complete documentation can be found in the directory *doc* of this package.
