from lib.HardwareTesterProtocol import HardwareTesterProtocol

from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.internet import reactor


class WebSocketServerCore:
    port = 9000

    def __init__(self, eventBus, port = 9000):
        self.running = False
        self.eventBus = eventBus
        self.port = port

    def __del__(self):
        self.stop()

    def start(self):
        factory = WebSocketServerFactory()
        factory.protocol = lambda : HardwareTesterProtocol(self.eventBus)

        reactor.listenTCP(self.port, factory)
        self.running = True
        reactor.run()

    def stop(self):
        if self.running:
            print("\nClose Command Received: Stopping Server...")
            reactor.stop()
