The Installer-Class
===================

Main Functions
--------------

The Installer-Class is the main part of the installer. It coordinates the
installation process and starts all steps registered for a special key.

Therefore this class provides two functions. 

The first function is *Installer.register*. You can read about it in the
section: :doc:`howtouse`.

The second function is *Installer.install* which is used to start the whole 
process.

Purposes
--------

During the Installation the installer follows the order given in the list
*Installer.purposes*. The default order would be:

* 'globalpackages',
* 'python',
* 'updatebashrc',
* 'virtualenv',
* 'pythonpackages',
* 'getcurrentproject'

But you can change this list if you want. If you change it, you have to be
carefull when you register new handler. Each handler has to be registered for
at least one purpose an this purpose has to be in the list.

The Key
-------

When the installation is started the *Installer.install* function is called
with a special key. This key is build by the Function *get_registry_key* which 
is part of *inqbus.installer.registration*.

The key contains all information the process needs including:

* which python should be used,
* is it a remote or a local installation,
* should a virtual environment be created,
* and what kind of operating system has the host.

With these information the installer decides which of the registered handlers
are the ones to execute.