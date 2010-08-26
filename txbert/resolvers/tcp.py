# Copyright (c) 2010 <jonathan.stoppani@gmail.com>
# See LICENSE for details.

"""
TCP (host:port) resolver implementation.

@author: Jonathan Stoppani <jonathan.stoppani@edu.hefr.ch>
"""


from zope.interface import implements
from twisted.internet.protocol import ClientCreator

from txbert import resolvers, protocol


class TCPResolver(object):
    implements(resolvers.IResolver)
    
    def __init__(self, reactor):
        self.reactor = reactor
    
    def buildProtocol(self, addr):
        host, port = addr.split(':')
        port = int(port)
        
        s = ClientCreator(self.reactor, protocol.BERTProtocol)
        return s.connectTCP(host, port)

