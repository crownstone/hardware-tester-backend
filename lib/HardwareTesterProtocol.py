import json
from autobahn.twisted.websocket import WebSocketServerProtocol
from lib.Topics import Topics


class HardwareTesterProtocol(WebSocketServerProtocol):

    def __init__(self, eventBus):
        super().__init__()
        self.counter = 0
        self.eventBus = eventBus
        self.writeSubscriptionId = self.eventBus.subscribe(Topics.wsWriteMessage, self.writeMessage)

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        # implementation of basic ping-pong. If this is not added, the connection will fall asleep without any notification, error or event.
        if payload.decode('utf8') == 'ping':
            self.sendMessage(b"pong", isBinary)
            return

        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            print("Text message received: {}".format(payload.decode('utf8')))
            self.eventBus.emit(Topics.wsReceivedMessage, payload.decode('utf8'))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
        self.eventBus.unsubscribe(self.writeSubscriptionId)

    def writeMessage(self, data):
        self.counter = self.counter + 1
        self.sendMessage(bytes(str(json.dumps(data)), 'utf-8'), False)

