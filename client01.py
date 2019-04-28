#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
@version: Python3.6.4
@author:  Justinli
good test

"""

import sys
import io
import time
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import threading
from twisted.protocols.basic import LineReceiver
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Echo(Protocol):
    def __init__(self):
        self.connected = False

    def dataReceived(self, data):
        print(data.decode())
        # sys.stdout.write(data.decode())

    def connectionMade(self):
        self.connected = True

    def connectionLost(self, reason):
        self.connected = False


class EchoClientFactory(ClientFactory):
    def __init__(self):
        self.protocol = None

    def startedConnecting(self, connector):
        print("Started to connect...")

    def buildProtocol(self, addr):
        print("Connected.")
        self.protocol = Echo()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print('Lost connection. Reson :', reason)

    def clientConnectionFailed(self, connector, reason):
        print('failed connection. Reason: ',reason)


def sendmsg(ff):
    factory = ff
    while True:
        time.sleep(3)
        if factory.protocol and factory.protocol.connected:
            factory.protocol.transport.write("hello".encode())

            # text = input("please input your message: ")
            # factory.protocol.transport.write(text.encode("utf8"))

factorye = EchoClientFactory()
reactor.connectTCP('127.0.0.1', 8001, factorye)
bloop = True
t = threading.Thread(target=sendmsg, args=(factorye,))
t.setDaemon(True)
t.start()
reactor.run()
bloop = False






