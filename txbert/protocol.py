# Copyright (c) 2010 <jonathan.stoppani@gmail.com>
# See LICENSE for details.

"""
Transport agnostic BERT Protocol classes to facilitate the exchange of
BERT-encoded data.

@author: Jonathan Stoppani <jonathan.stoppani@edu.hefr.ch>
"""


import struct
import bert

from twisted.internet import defer
from twisted.protocols import basic
from twisted.python import log


class BERTError(Exception):
    def __init__(self, type, code, klass, detail, backtrace):
        self.type = type
        self.code = code
        self.klass = klass
        self.detail = detail
        self.backtrace = backtrace
    
    def __repr__(self):
        return '<BERT %s error: %d - %s>' % (self.type, self.code, self.klass)
    
    def __str__(self):
        return '%s: %s' % (self.klass, self.detail)


class BERTProtocol(basic.IntNStringReceiver, object):
    """
    Base BERT protocol.
    """
    
    structFormat = "!L"
    prefixLength = struct.calcsize(structFormat)
    
    methods = set(('call', 'reply', 'error', 'cast', 'info', 'noreply'))
    
    def __init__(self):
        self.result = None
        """This property will be set to a deferred when waiting for a result."""
        
        self.request_lock = defer.DeferredLock()
        """Lock to be used by the functions to wait for a response before
        sending out the next request."""
    
    def stringReceived(self, data):
        """
        Handles incoming BERT requests by dispatching them to the right
        method. Allowed methods are, as defined in the BERT-RPC specification,
        C{call}, C{reply}, C{error}, C{cast} and C{info}.
        
        @todo: Add a C{setRawMode} or C{setStreamMode} to handle streamed
               requests.
        """
        decoded = bert.decode(data)
        method = decoded[0]
        
        print self.transport
        
        try:
            assert isinstance(method, bert.Atom)
            assert method in self.methods
            handler = getattr(self, '%sReceived' % method)
        except (AttributeError, AssertionError):
            log.err("No such method '%s'." % method)
        else:
            if method == bert.Atom('error'):
                handler(*decoded[1])
            else:
                handler(*decoded[1:])
    
    def callReceived(self, module, function, arguments):
        raise NotImplementedError
    
    def errorReceived(self, type, code, klass, detail, backtrace):
        if self.result:
            self.result.errback(BERTError(type, code, klass, detail, backtrace))
    
    def castReceived(self, module, function, arguments):
        raise NotImplementedError
    
    def infoReceived(self, command, options):
        raise NotImplementedError
    
    def replyReceived(self, result):
        if self.result:
            self.result.callback(result)
        else:
            log.err('Reply received but no requests where listening.')
    
    def noreplyReceived(self):
        if self.result:
            self.result.callback(None)
        else:
            log.err('Noreply received but no requests where listening.')
    
    def sendPacket(self, method, *options):
        """
        Encodes the given C{term} using the Binary ERlang Term format and
        sends it over the transport using a Binary ERlang Packet.
        """
        term = bert.encode((bert.Atom(method),) + options)
        self.transport.write(struct.pack(self.structFormat, len(term)))
        self.transport.write(term)
    
    def sendReply(self, result):
        self.sendPacket('reply', result)
    
    def sendNoreply(self):
        self.sendPacket('noreply')
    
    @defer.inlineCallbacks
    def sendRequest(self, method, module, function, arguments):
        yield self.request_lock.acquire()
        
        try:
            self.result = defer.Deferred()
            self.sendPacket(method, bert.Atom(module), bert.Atom(function), list(arguments))
            try:
                result, self.result = (yield self.result), None
            except BERTError as e:
                self.result = None
                print e
                result = e
            defer.returnValue(result)
        finally:
            self.request_lock.release()
    
    def sendCall(self, module, function, arguments):
        return self.sendRequest('call', module, function, arguments)
    
    def sendCast(self, module, function, arguments):
        return self.sendRequest('cast', module, function, arguments)
    
    def sendInfo(self, command, options):
        self.sendPacket('info', bert.Atom(command), options)

