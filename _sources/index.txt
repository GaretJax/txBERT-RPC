============
Introduction
============


About
=====

.. include:: ../README.rst


Installation
============

Stable releases of txBERT will be easy installable directly from the cheese-shop
(using either ``easy_install`` or ``pip``), but until then you can checkout
the development version from the git repository and install it using
the ``distutils`` package.

Detailed instructions and links may be found on the :doc:`installation` page.


Documentation
=============

The complete documentation is divided in three main parts: an Overview
containing a collection of mini HOW-TOs and Tutorials to get started, an
High-level API specification and a Low-level API specification. Additionally
some more specific sections are provided for completeness and to better
explain advanced features.

For new users, and/or for an overview of txBERT's basic functionality, please
read the :doc:`overview`. All the documentation assumes that you're already
familiar with the Twisted core architecture and with the complete BERT-RPC
specification.

.. toctree::
    :maxdepth: 1
    
    overview
    high-level
    low-level
    protocol-extensions
    testing
    development


