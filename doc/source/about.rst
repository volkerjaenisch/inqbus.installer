About
=====

The Inqbus.installer is written to setup an installation which can decide
between different settings like which operating system is used or is it a
remote or a local installation.

On the other hand, this installer is also able to skip steps which are already
done. This is very helpfull for long installations when it stops in the middle
of the process, because instead of testing all packages, which are already
installed, the installer just skips this steps. This can make the whole process
much faster.

It is written in Python and based on `Fabric`_.

.. _Fabric: http://docs.fabfile.org/en/1.8/