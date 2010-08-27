# Copyright (c) 2010 <jonathan.stoppani@gmail.com>
# See LICENSE for details.

"""
Utilities to expose objects to be accessed remotely through a BERT request.

@author: Jonathan Stoppani <jonathan.stoppani@edu.hefr.ch>
"""


from zope.interface import Interface, implements


class IBERTModule(Interface):
    """
    Interface used to mark an object as exposable over a BERT based service.
    """
    
    def getFunction(name):
        """
        The only method needed to be implemented to correctly dispatch the
        function call requested by a BERT client.
        
        Shall return a function or instance method which will handle requests
        for C{name} function calls on the implementing module.
        """


class ExplicitModuleMixin(object):
    """
    A mixin which can be added as a superclass to existing objects to make
    them usable as modules exposed over a BERT service.
    
    @see: See the documentation for the C{getFunction} method to obtain more
          info on how this mixin resolves function names to instance methods.
    """
    
    implements(IBERTModule)
    
    def getFunction(self, name):
        """
        Returns the instance method with the given C{name} prepended by the
        C{bertrpc_} prefix.
        """
        return getattr(self, 'bertrpc_{0}'.format(name))


class ImplicitModuleMixin(object):
    """
    A mixin which can be added as a superclass to existing objects to make
    them usable as modules exposed over a BERT service.
    
    @see: See the documentation for the C{getFunction} method to obtain more
          info on how this mixin resolves function names to instance methods.
    """
    
    implements(IBERTModule)
    
    def getFunction(self, name):
        """
        Returns the instance method with the given C{name} only if the name
        does not begin with an underscore.
        """
        if name.startswith('_'):
            raise AttributeError("Underscore-prefixed methods are considered" \
                    " private and cannote be called.")
        
        return getattr(self, name)


def WhitelistModuleMixin(*methods):
    whitelist = set(methods)
    
    class WhitelistModuleMixin(object):
        implements(IBERTModule)
        
        def getFunction(self, name):
            """
            Returns the instance method with the given C{name} only if the name
            was whitelisted.
            """
            if name not in whitelist:
                raise AttributeError("Only whitelisted methods can be called" \
                        " on this module.")
            
            return getattr(self, name)
    return WhitelistModuleMixin

