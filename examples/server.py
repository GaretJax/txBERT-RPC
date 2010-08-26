

from twisted.internet import reactor
#from twisted.application import internet, service

#from txbert.shortcuts import serve
#from txbert import module#, server
#from txbert.resolvers.tcp import TCPResolver


import txbert


class Calculator(txbert.Module):
    def add(self, a, b):
        return a + b
 
    def sub(self, a, b):
        return a - b

txbert.serve(9999, Calculator())
reactor.run()

#factory = server.BERTFactory()
#factory.plugResolver(TCPResolver(reactor))
#factory.registerModule('ext', Calculator())
#reactor.listenTCP(9999, factory)


#application = service.Application("BERT Application")
#bertService = internet.TCPServer(9999, factory)
#bertService.setServiceParent(application)