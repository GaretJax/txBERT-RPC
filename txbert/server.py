# Copyright (c) 2010 <jonathan.stoppani@gmail.com>
# See LICENSE for details.

"""
Server implementation of a BERT-based communication architecture.

@author: Jonathan Stoppani <jonathan.stoppani@edu.hefr.ch>
"""


from twisted.internet import defer, protocol
from twisted.python import log

from txbert import error, resolvers, module
from txbert.protocol import BERTProtocol


class BERTChannel(BERTProtocol):
    """
    A single BERT channel.
    
    Each channel instance is bound to a connection and handles requests from
    one and only one client.
    """
    
    def __init__(self):
        self.callbacks = []
        """List of callbacks to be called when the response to a cast request
        is returned."""
    
    def infoReceived(self, command, options):
        if command == 'callback':
            self.callbacks.append((
                options[0][1],
                options[1][1],
                options[1][2],
                options[1][3],
            ))
    
    @defer.inlineCallbacks
    def callReceived(self, module, function, arguments):
        if self.callbacks:
            self.callbacks = []
            log.err("Some callbacks were set but a 'call' request was received.")
        
        result = yield self.factory.dispatch(module, function, arguments)
        self.sendReply(result)
    
    @defer.inlineCallbacks
    def castReceived(self, module, function, arguments):
        callbacks, self.callbacks = self.callbacks, []
        
        d = self.factory.dispatch(module, function, arguments)
        self.sendNoreply()
        result = yield d
        
        for service, mod, func, args in callbacks:
            args = list(args + [result])
            protocol = yield self.factory.resolve(service)
            yield protocol.sendCast(mod, func, args)
            protocol.transport.loseConnection()


class BERTFactory(protocol.ServerFactory):
    
    protocol = BERTChannel
    
    def __init__(self, modules=None, resolvers=None):
        self.modules = {}
        self.resolvers = set()
        
        if modules:
            self.registerModules(**modules)
        
        if resolvers:
            for r in resolvers:
                self.plugResolver(r)
    
    def dispatch(self, module, function, arguments):
        try:
            # @todo: Catch wrong arguments errors?
            handler = self.modules[module].getFunction(function)
        except KeyError:
            raise error.ModuleNotFound(module)
        except AttributeError:
            raise error.FunctionNotFound(module, function)
        
        return defer.maybeDeferred(handler, *arguments)
    
    def resolve(self, addr):
        for r in self.resolvers:
            try:
                return r.buildProtocol(addr)
            except resolvers.ResolvingError:
                continue
        else:
            raise resolvers.ResolvingError()
    
    def plugResolver(self, resolver):
        self.resolvers.add(resolvers.IResolver(resolver))
    
    def unplugResolver(self, resolver):
        self.resolvers.discard(resolvers.IResolver(resolver))
    
    def registerModule(self, name, handler):
        self.modules[name] = module.IBERTModule(handler)
    
    def registerModules(self, **handlers):
        for k, v in handlers.iteritems():
            self.registerModule(k, v)

