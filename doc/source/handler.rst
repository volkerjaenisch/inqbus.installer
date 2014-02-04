The Handler
===========

A handler is a special class which provides the important code to do one step 
of the installation. You can use the included handlers or write your own ones.

Included Handlers
-----------------

Adding own Handlers
-------------------

Each handler has to provide a install-method. It can also provide additional
functions especially the __init__-method.::

  class Handler(object):
  
      def install(self):
  	      # do something
  	      pass

Some special handlers can inherit from :doc:taskmixin. This class keeps care
of steps which are already done in the installation try before. So if the
installation breaks the completed steps will be skipped. Therefore you have to
add the __init__-method to take an argument which is called self.name.::

  from inqbus.installer.task import TaskMixin
  
  
  class Handler(TaskMixin):
  
      def __init__(self, name):
          self.name = name
  
      def install(self):
  	      # do something
  	      pass
