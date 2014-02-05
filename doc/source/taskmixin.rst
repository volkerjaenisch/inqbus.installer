The TaskMixin-Class
===================

The TaskMixin-Class cares about installation steps which are already done. So
if a installation breaks, you can correct it and restart at the point where it
stops.

This class uses a file called *fabric_tasks.txt* to store the names of all 
steps after they have finished. If this file already exists, it checks how long
the file doesn't has changed. If the file wasn't changed for a longer time, all
stored names will be deleted. If the file does not exist, it will be created.

For each step inheriting from the TaskMixin-Class, the installer first checks
if the name is included in the file. If that's the case, the step will be 
skipped. In the other case it will be executed.

You can use the TaskMixin-Class for your own handlers. Such handlers have to
provide a attribute *self.name* and a install-method. They could look like
this.

.. code-block:: python

  from inqbus.installer.task import TaskMixin
  
  
  class Handler(TaskMixin):
  
      def __init__(self, name):
          self.name = name
  
      def install(self):
          # do something
          pass