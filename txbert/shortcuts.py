# Copyright (c) 2010 <jonathan.stoppani@gmail.com>
# See LICENSE for details.

"""
Shortcuts to rapidly deploy and access remote services over BERT-RPC.

@author: Jonathan Stoppani <jonathan.stoppani@edu.hefr.ch>
"""


import re

from txbert import server, client
from txbert.resolvers.tcp import TCPResolver


def serve(port, module, module_name=None, resolvers=None, reactor=None):
    if not reactor:
        from twisted.internet import reactor
    
    if not module_name:
        name = module.__class__.__name__
        module_name = re.sub(r'([^A-Z])([A-Z]+)', r'\1_\2', name).lower()
    
    if resolvers is None:
        resolvers = (TCPResolver(reactor),)
    
    factory = server.BERTFactory(resolvers=resolvers)
    factory.registerModule(module_name, module)
    reactor.listenTCP(port, factory)


def service(host, port, reactor=None):
    if not reactor:
        from twisted.internet import reactor
    
    s = client.BERTClientCreator(reactor)
    return s.connectTCP(host, port)

