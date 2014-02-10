The Handler
===========

A handler is a special class which provides the important code to do one step 
of the installation. You can use the included handlers or write your own ones.

Included Handlers
-----------------

There are a lot of included handlers in the installer-package. 
You can import them from *inqbus.installer.handler*. 

Some of them are inheriting from :doc:`taskmixin` which handles skipping 
already completed steps, when the installation is restarted.

Global(TaskMixin)
^^^^^^^^^^^^^^^^^
This class can be used to install different global packages. It takes two 
necessary parameters and one optional.

The first necessary argument is a string representing the name used by the
TaskMixin-Class.

The second necessary argument is a string which is the command that should
be used to install the package. This command should contain the string 
formatting operator '%s' on the place where the package-name should be
entered.

The optional argument is also a command containing the formatting operator
'%s' instead of the package-name. This command is used to check if the
package is installed before it is installed by the other command. If it is
not given, all packages will be installed without testing.

To add a package, you can use the add-method given by the class.

The following example shows, how this class is used to install the packages 
pip, virtualenv and the virtualenvwrapper with aptitude.

.. code-block:: python

  from inqbus.installer.handler import Global
  
  
  globalpackage = Global('global', 'su -c "aptitude update && aptitude install %s"', 
                         'dpkg -s %s')
  
  globalpackage.add('python-pip')
  globalpackage.add('python-virtualenv')
  globalpackage.add('virtualenvwrapper')

RunGlobal(TaskMixin)
^^^^^^^^^^^^^^^^^^^^
This class can be used to run single global commands. It takes two 
necessary parameters.

The first necessary argument is a string representing the name used by the
TaskMixin-Class.

The second necessary argument is a string representing the command.

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
This class can be used to add content to the *.bashrc*. It takes only
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
as the second one and the path to the anconda-installation as third one.

The following example shows, how it can be used in combination with the 
Anaconda-Class and parsed arguments.

.. code-block:: python

  from inqbus.installer.handler import Anaconda, AnacondaVenv
  from inqbus.installer.registration import args
  
  anaconda = Anaconda('anaconda')
      
  anavenv = AnacondaVenv('anavenv', args.venv_name, anaconda.install_dir)

AnacondaPip(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^
This handler can be used to install python-packages within a virtual
environment created with anaconda. As arguments it takes a name, the name
of the virtual environment and the path where Anaconda is installed.

You can add packages by using the add-method of this class. All given packages 
will be installed using pip.

The following example shows, how you can use this class in combination with the
parsed commandline-arguments and the class which installed Anaconda.

.. code-block:: python

  from inqbus.installer.handler import Anaconda, AnacondaPip
  from inqbus.installer.registration import args
  
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

It takes four arguments.

The first one is the name of the repository. The second one is the link from 
github, where the repository is located and the third one is the branch you want to
clone. The last argument is the path where the repository should be saved
on the computer. 

In the given directory another directory will be created with the given
repository-name and this directory will contain all the cloned files.   

.. _github: https://github.com/

AnacondaProject(object)
^^^^^^^^^^^^^^^^^^^^^^^
This handler can be used to install the packages of the current project in
python development-mode. The project is installed in the virtual environment 
created with Anaconda.

Therefore it takes four arguments.

The first two one specify the directory where your project is saved. The first 
argument is the name of your project and also the name of the project's 
root-directory. The second one is the path to the directory, where the 
root-directory is found.

The last two arguments specify your anaconda environment. The first one is the 
path, where your anaconda is installed and the second one is the name of the
virtual environment.

With the add-method of the class, you can add paths to the *setup.py*-files.

The following example shows, how it can be used.

.. code-block:: python

  from inqbus.installer.handler import Anaconda, AnacondaProject
  from inqbus.installer.registration import args
  
  anaconda = Anaconda('anaconda')
  
  project = AnacondaProject('~/projects/', 'currentproject',
                            anaconda.install_dir, args.venv_name)

  project.add('firstpackage')
  project.add('path/to/secondpackage')

VenvWrapper(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^
This handler can be used to create a virtual environment using the 
`virtualenvwrapper`_.

It just gets a name and the name of the virtual environment. You can use it 
this way:

.. code-block:: python

  from inqbus.installer.handler import VenvWrapper
  from inqbus.installer.registration import args
  
  createvenv = VenvWrapper('create_venv', args.venv_name)

.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/

WrapperPip(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^
This handler can be used to install python-packages in a virtual environment
which was created with the virtualenvwrapper.

It takes two necessary arguments and one optional. The first necessary argument
is the name used by the TaskMixin-Class. The second one is the name of the 
virtual environment.

The optional argument is a command which has to be executed before the 
installation of the packages starts.

You can add packages by using the add-method of this class. All given packages 
will be installed using pip.

You can use it this way:

.. code-block:: python

  from inqbus.installer.handler import WrapperPip
  from inqbus.installer.registration import args
  
  venv = WrapperPip('venv_pip', args.venv_name)
  
  venv.add('django')

VenvProject(object)
^^^^^^^^^^^^^^^^^^^
This handler can be used to install the packages of the current project in
python development-mode. The project is installed in the virtual environment 
created with the virtualenvwrapper.

Therefore it takes three necessary arguments and one optional. 

The first two arguments specify the directory where your project is saved. 
The first one is the name of the project and also the name of the project's 
root-directory. The second one is the path to the directory, where the 
root-directory is found.

The last necessary argument specifies your environment by giving the name.

The optional argument is a command which has to be executed before the 
installation of the packages starts.

With the add-method of the class, you can add paths to the *setup.py*-files.

The following example shows, how it can be used.

.. code-block:: python

  from inqbus.installer.handler import VenvProject
  from inqbus.installer.registration import args
  
  project = VenvProject('~/projects/', 'currentproject', args.venv_name)

  project.add('firstpackage')
  project.add('path/to/secondpackage')

VenvCommand(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^
This is a simple handler to run commands within the virtual environment
created by the virtualenvwrapper.

It just takes a name and the name of the virtual environment. The commands can
be added by using the add-method.

.. code-block:: python

  from inqbus.installer.handler import VenvCommand
  from inqbus.installer.registration import args
  
  command = VenvProject('venv_command', args.venv_name)
  
  command.add('echo "first command"')
  command.add('echo "second command"')

Adding own Handlers
-------------------
For your deployment you can create your own handlers and register them to the
installer. Therefore it has to fulfill some simple conditions.

Each handler has to provide a install-method. It can also provide additional
functions especially the __init__-method, if you need them.::

  class Handler(object):
  
      def install(self):
          # do something
          pass

Some special handlers can inherit from :doc:`taskmixin`. This class keeps care
of steps which are already done in the installation. So if the installation
breaks the completed steps will be skipped. Therefore you have to add an 
argument which is called self.name. One way to do this is setting it in the
__init__-method.::

  from inqbus.installer.task import TaskMixin
  
  
  class Handler(TaskMixin):
  
      def __init__(self, name):
          self.name = name
  
      def install(self):
          # do something
          pass
