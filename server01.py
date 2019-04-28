#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
@version: Python3.6.4
@author:  Justinli

"""

import sys
import io

from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Echo(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionLost(self, reason):
        print(self.transport.client[0], "leave now!")
        self.factory.numProtocols = self.factory.numProtocols - 1
        pass

    def connectionMade(self):
        print("welcome ", self.transport.client[0], "connect!")
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.transport.write(("welcome to my server01, you is the %s user come here" % self.factory.numProtocols).encode())

    def dataReceived(self, data):
        self.transport.write(data)
        if data.decode() == "close\r\n":
            self.transport.write("baibai".encode())
            self.transport.loseConnection()
        else:
            print(data.decode())
            self.transport.write("have msg".encode())
    # def lineReceived(self, line):
    #     print(line.decode())
    #     self.sendLine(line)


class EchoFactory(Factory):
    def __init__(self):
        self.numProtocols = 0

    def buildProtocol(self, addr):
        return Echo(self)


endpoint = TCP4ServerEndpoint(reactor, 8001)
endpoint.listen(EchoFactory())
reactor.run()