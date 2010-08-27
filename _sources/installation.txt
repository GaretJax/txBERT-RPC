============
Installation
============


Installation of the development version
=======================================

Using ``distutils``
-------------------

To install the development version using the ``distutils`` package, you have
first to download the package, unpack it, ``cd``-dir into it and the run::

   $ python setup.py install


Using ``pip``
-------------

To install the development version directly from the git repository you can
use the ``pip`` command in the following way::

   $ pip install git+http://github.com/GaretJax/txbert.git#egg=txbert

or, if you want the installed package to be editable, use the ``-e`` switch::

   $ pip install -e git+http://github.com/GaretJax/txbert.git#egg=txbert

