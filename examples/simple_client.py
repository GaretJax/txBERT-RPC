
#from twisted.internet import defer, reactor, task

#import txbert

#def doTest(client, num):
#    for x in xrange(num):
#        d = client.Calculator.add(1, 2)
#        d.addCallback(pp)
#        yield d
#
#@defer.inlineCallbacks
#def test():
#    s = BERTClientCreator(reactor)
#    c = yield s.connectTCP('localhost', 9999)
#    
#    work = doTest(c, 100)
#    c = task.Cooperator()
#    l = []
#    for x in xrange(700):
#        l.append(c.coiterate(work))
#    yield defer.DeferredList(l)
#    #reactor.stop()
#
#count = 0
#def pp(res):
#    global count
#    count += 1
#    print count
#
#reactor.callWhenRunning(test)
#reactor.run()


from twisted.internet import defer, reactor
import txbert

@defer.inlineCallbacks
def test():
    service = yield txbert.service('localhost', 9999)
    result = yield service.calculator.add(1, 2)
    print result

reactor.callWhenRunning(test)
reactor.run()