# Copyright (c) 2010 <jonathan.stoppani@gmail.com>
# See LICENSE for details.

"""
Twisted based BERT-RPC client and server implementations.

@author: Jonathan Stoppani <jonathan.stoppani@edu.hefr.ch>
"""


from txbert.module import ImplicitModuleMixin as Module
from txbert.shortcuts import serve, service


__all__ = ('serve', 'service', 'Module')


__version__ = "0.0.1"

