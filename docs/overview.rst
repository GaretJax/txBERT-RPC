========
Overview
========


Preamble
========

This documentation assumes that you have a working installation of the
``txbert`` package and its dependencies. You should also be comfortable with
Twisted's philosophy, concepts and coding guidelines.


Shortcuts
=========

The ``txbert`` package offers a small set of shortcuts used to rapidly deploy
or access services over BERT-RPC.

These functions make some assumptions about the exposed/accessed services and
do not offer an high degree of flexibility. Nevertheless they offer a valid
alternative to a more verbose solution and are a valid alternative for basic
deployments.

All of the shortcuts are contained in the ``txbert.shortcuts`` module, but can
be accessed from the ``txbert`` module for the sake of brevity.


A simple server
---------------

The ``serve`` shortcut can be used to expose all methods of an arbitrary
object over BERT-RPC.

Basic (but complete) example::

   import txbert
   from twisted.internet import reactor
   
   class Calculator(txbert.Module):
      def add(self, a, b):
         return a + b
      
      def sub(self, a, b):
         return a - b
   
   txbert.serve(9999, Calculator())
   reactor.run()

