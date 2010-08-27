# Copyright (c) 2010 <jonathan.stoppani@gmail.com>
# See LICENSE for details.

"""
Classes to transparently work on remote BERT modules.

@author: Jonathan Stoppani <jonathan.stoppani@edu.hefr.ch>
"""


import bert
import uuid

from twisted.internet.protocol import ClientCreator
from twisted.internet import defer
from twisted.python import log

from txbert import server, protocol, module


__all__ = ('BERTClientCreator', 'BERTClient',)


class BERTClientCreator(ClientCreator, module.WhitelistModuleMixin('callback')):
    """
    A service instance which provides means to access functions offered by the
    remotely hosted modules.
    """
    
    def __init__(self, reactor, incoming=0):
        super(BERTClientCreator, self).__init__(reactor, BERTClient, self)
        
        service = server.BERTFactory()
        service.registerModule('bert', self)
        port = reactor.listenTCP(incoming, service)
        # @todo: Check that this works for calls from the outside world too
        self.incoming = '%s:%d' % (port.getHost().host, port.getHost().port)
        self.callbacks = {}
    
    def callback(self, resid, result):
        try:
            self.callbacks.pop(resid)(result)
        except KeyError:
            log.err('Invalid callback response ID')
    
    def registerCallback(self, callback, resid=None):
        resid = resid or str(uuid.uuid4())
        self.callbacks[resid] = callback
        return resid


class BERTClient(protocol.BERTProtocol):
    """
    Provides a remote interface to a selected module with the name passed to
    the constructor.
    
    This protocol subclass is intended to be instantiated by
    the C{Service} class only.
    """
    
    def __init__(self, service):
        super(BERTClient, self).__init__()
        
        self.service = service
    
    def __repr__(self):
        return "CLIENT"
        #peer = self.transport.getPeer()
        #return '<%s instance on %s:%s>' % (self.name, peer.host, peer.port)
    
    def __getattr__(self, name):
        try:
            return getattr(super(BERTClient, self), name)
        except AttributeError:
            if name.startswith('_'):
                raise
            return Module(self, name)
    
    def sendCast(self, module, function, args, callback=False):
        if callback:
            deferred = defer.Deferred()
            resid = self.service.registerCallback(deferred.callback)
            service = (bert.Atom('service'), self.service.incoming)
            mfa = (bert.Atom('mfa'), bert.Atom('bert'), bert.Atom('callback'), [resid])
            callback = [service, mfa]
            self.sendInfo('callback', callback)
            super(BERTClient, self).sendCast(module.name, function.name, args)
        else:
            deferred = super(BERTClient, self).sendCast(module.name, function.name, args)
        
        return deferred


class Module(object):
    def __init__(self, client, name):
        self.client = client
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        peer = self.client.transport.getPeer()
        return '<%s instance on %s:%s>' % (self.name, peer.host, peer.port)
    
    def __getattr__(self, name):
        try:
            return getattr(super(Module, self), name)
        except AttributeError:
            if name.startswith('_'):
                raise
            return Function(self.client, self, name)


class Function(object):
    def __init__(self, client, module, name):
        self.client = client
        self.module = module
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __call__(self, *args):
        return self.client.sendCast(self.module, self, args, True)

