`txBERT <http://github.com/GaretJax/txBERT>`_ is a python library offering both
client and server implementations to easily deploy and access remote services
using the `BERT-RPC <http://bert-rpc.org>`_ protocol and the `Twisted
networking engine <http://twistedmatrix.com>`_.

The provided libraries can be exploited both using low-level API method calls
or by taking advantage of the many shortcuts and utilities provided by the
high-level API.

The most simple way to deploy a remotely-accessible BERT service is by using
the shortcuts provided by the ``txbert`` module::

   import txbert
   from twisted.internet import reactor
   
   class Calculator(txbert.Module):
       def add(self, a, b):
           return a + b
    
       def sub(self, a, b):
           return a - b
   
   txbert.serve(9999, Calculator())
   reactor.run()

Similarly, it is possible to create a client with very little effort::

   from twisted.internet import defer, reactor
   import txbert
   
   @defer.inlineCallbacks
   def test():
       service = yield txbert.service('localhost', 9999)
       result = yield service.calculator.add(1, 2)
       print result
   
   reactor.callWhenRunning(test)
   reactor.run()

But probably you want to use the high-level APIs instead of the shortcuts to
be able to customize and exploit all features provided by the library.
Refer to the complete documentation for the HOW-TOs and the detailed
instructions about how to use them.