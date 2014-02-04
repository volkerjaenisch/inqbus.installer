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
#. The second necessary argument is a string is the command which should be
   used to install the package. This command should contain the string 
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

  global = Global('global',
                  'su -c "aptitude update && aptitude install %s"',
                  'dpkg -s %s')
  
  global.add('python-pip')
  global.add('python-virtualenv')
  global.add('virtualenvwrapper')

RunGlobal(TaskMixin)
^^^^^^^^^^^^^^^^^^^^

Anaconda(TaskMixin)
^^^^^^^^^^^^^^^^^^^

UpdateBashrc(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^^

AnacondaVenv(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^^

AnacondaPip(TaskMixin)
^^^^^^^^^^^^^^^^^^^^^^

GitClone(object)
^^^^^^^^^^^^^^^^

AnacondaProject(object)
^^^^^^^^^^^^^^^^^^^^^^^

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
