# Copyright (c) 2010 <jonathan.stoppani@gmail.com>
# See LICENSE for details.

"""
Base classes, interfaces and common implementation for resolvers for callback
service addresses.

@author: Jonathan Stoppani <jonathan.stoppani@edu.hefr.ch>
"""


from zope.interface import Interface


__all__ = ('IResolver', 'ResolvingError',)


class IResolver(Interface):
    def buildProtocol(self, addr):
        """Builds and returns a BERT protocol instance for the given address
        or raises a ResolvingError."""


class ResolvingError(Exception):
    pass

