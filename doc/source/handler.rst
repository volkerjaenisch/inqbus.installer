The Handler
===========

A handler is a special class which provides the important code to do one step 
of the installation. You can use the included handlers or write your own ones.

Included Handlers
-----------------

There are a lot of included handlers included in the installer-package. 
You can import from *inqbus.installer.handler*. 

Some of them are inheriting from :doc:`taskmixin` which handles skipping 
already completed steps, when the installation is restarted.

Global(TaskMixin)
^^^^^^^^^^^^^^^^^
This class can be used to install different global packages. It takes two 
necessary parameters and one optional.

#. The first necessary argument is a string representing the name used by the
   TaskMixin-Class.
#. The second necessary argument is a string which is the command which should
   be used to install the package. This command should contain the string 
   formatting operator '%s' on the place where the package-name should be
   entered.
#. The optional argument is also a command containing the formatting operator
   '%s' instead of the package-name. This command is used to check if the
   package is installed before it is installed by the other command. If it is
   not given, all packages will be installed without testing.

To add a package, you can use the add-method given by the class.

The following example shows, how this class is used to install pip, virtualenv
and the virtualenvwrapper with aptitude.

.. code-block:: python

  from inqbus.installer.handler import Global
  
  
  global = Global('global', 'su -c "aptitude update && aptitude install %s"', 
                  'dpkg -s %s')
  
  global.add('python-pip')
  global.add('python-virtualenv')
  global.add('virtualenvwrapper')

RunGlobal(TaskMixin)
^^^^^^^^^^^^^^^^^^^^
This class can be used to run single global commands. It takes two 
necessary parameters.

#. The first necessary argument is a string representing the name used by the
   TaskMixin-Class.
#. The second necessary argument is a string which is the command.

The following example shows, how this class is used to uninstall the 
virtualenvwrapper via pip.

.. code-block:: python

  from inqbus.installer.handler import RunGlobal
  
  
  runglobal = RunGlobal('runglobal', 'su -c "pip uninstall virtualenvwrapper"')

Anaconda(TaskMixin)
^^^^^^^^^^^^^^^^^^^
This class can be used to install `Anacona`_. It just takes the name used by
TaskMixin-Class, but during the installation it asks the user where anaconda
should be installed.
This information is required by other handlers, too. You can receive it by
asking for the value of the attribute *install_dir*.

.. code-block:: python

  from inqbus.installer.handler import Anaconda
  
  
  anaconda = Anaconda('anaconda')
  
  # handler uses the path to anaconda
  
  handler = Handler('test', anaconda.install_dir)

.. _Anaconda: https://store.continuum.io/cshop/anaconda/

UpdateBashrc(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^^
This class can be used to add content to the *.bashrc*. This class takes only
the name used for the TaskMixin-Class as argument.

To add a line to the *.bashrc* you can use the add-method of this class.
This method takes two arguments. The first one is the line which should be
added. The second one is optional and is a string. This parameter is a
testline.

If the *.bashrc* contains the testline, then the line would not be added. In
the other case it would.

The following example shows, how this class is used to add the
WORKON_HOME-setting for the virtualenvwrapper.

.. code-block:: python

  from inqbus.installer.handler import UpdateBashrc
  
  
  bash = UpdateBashrc('bashrc')
  
  bash.add('export WORKON_HOME=~/.virtualenvs', 'WORKON_HOME')

AnacondaVenv(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^^
This class can be used to create a virtual environment with Anaconda. It takes
a name for the TaskMixin as first argument, the name of the virtual environment
as the second one and the path to the anconda-installation.

The following example shows, how it can be used in combination with the 
Anaconda-Class and parsed arguments.

.. code-block:: python

  from inqbus.installer.handler import Anaconda, AnacondaVenv
  from inqbus.installer.registration import parse_arguments
  
  
  args = parse_arguments()
  
  anaconda = Anaconda('anaconda')
      
  anavenv = AnacondaVenv('anavenv', args.venv_name, anaconda.install_dir)

AnacondaPip(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^
This handler can be used to install python-packages within a virtual
environment created with anaconda. As arguments it takes a name, the name
of the virtual environment and the path where your Anaconda is installed.

You can add packages by using the add-method of this class. All given packages 
will be installed using pip.

The following example shows, how you can use this class in combination with the
parsed commandline-arguments and the class which installed Anaconda.

.. code-block:: python

  from inqbus.installer.handler import Anaconda, AnacondaPip
  from inqbus.installer.registration import parse_arguments
  
  
  args = parse_arguments()
  
  anaconda = Anaconda('anaconda')
      
  anapip = AnacondaPip('anapip', args.venv_name, anaconda.install_dir)
  
  anapip.add('django')
  anapip.add('django-debug-toolbar')

GitClone(object)
^^^^^^^^^^^^^^^^
This handler can be used to clone or to update a project from `github`_.

When this handler is used, the installer first checks if the directory already
exists. If that's the case, the project just will be updated by running
*git pull*. In the other case the project will be cloned.

This handler takes five arguments.

The first one is the name. The second one is the name of the repository. The 
third one is the link from github, where the repository is and the fourth one
is the branch you want to clone. The last argument is the path where the 
repository should be saved on the computer. 

In the given directory will be a directory created with the given
repository-name and this directory will contain all the important files.   

.. _github: https://github.com/

AnacondaProject(object)
^^^^^^^^^^^^^^^^^^^^^^^
This handler can be used to install the packages of the current project in
python development-mode. The project is installed in the virtual environment 
created with Anaconda.

Therefore it takes five arguments. The first one is the name. 

The next to one specify the directory where your project is saved. The second 
argument is the name of your project and also the name of the project's 
root-directory. The third one is the path to the directory, where the 
root-directory is found.

The last two arguments specify your anaconda environment. The first one is the 
path, where your anaconda is installed and the second one is the name of the
virtual environment.

With the add-method of the class, you can add paths to the *setup.py*-files.

The following example shows, how it can be used.

.. code-block:: python

  from inqbus.installer.handler import Anaconda, AnacondaProject
  from inqbus.installer.registration import parse_arguments
  
  
  args = parse_arguments()
  
  anaconda = Anaconda('anaconda')
  
  project = AnacondaProject('ana_pro', '~/projects/', 'currentproject',
                            anaconda.install_dir, args.venv_name)

  project.add('firstpackage')
  project.add('path/to/secondpackage')

VenvWrapper(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^

WrapperPip(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^

VenvProject(object)
^^^^^^^^^^^^^^^^^^^

VenvCommand(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^

Adding own Handlers
-------------------

Each handler has to provide a install-method. It can also provide additional
functions especially the __init__-method.::

  class Handler(object):
  
      def install(self):
          # do something
          pass

Some special handlers can inherit from :doc:`taskmixin`. This class keeps care
of steps which are already done in the installation. So if the installation
breaks the completed steps will be skipped. Therefore you have to add the
__init__-method to take an argument which is called self.name.::

  from inqbus.installer.task import TaskMixin
  
  
  class Handler(TaskMixin):
  
      def __init__(self, name):
          self.name = name
  
      def install(self):
          # do something
          pass
