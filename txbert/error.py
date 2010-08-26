# Copyright (c) 2010 <jonathan.stoppani@gmail.com>
# See LICENSE for details.

"""
Protocol and Server esception classes and error handling code used throughout
the library.

@author: Jonathan Stoppani <jonathan.stoppani@edu.hefr.ch>
"""


class BERTError(Exception):
    pass


class ServerError(BERTError):
    def __init__(self, code=0, msg='Undesignated'):
        self.code = code
        self.message = msg


class ModuleNotFound(ServerError):
    def __init__(self, mod_name):
        super(ModuleNotFound, self).__init__(1, "No such module '{0}'".format(mod_name))


class FunctionNotFound(ServerError):
    def __init__(self, mod_name, func_name):
        super(FunctionNotFound, self).__init__(2, "Function '{0}' not found on '{1}'".format(func_name, mod_name))

