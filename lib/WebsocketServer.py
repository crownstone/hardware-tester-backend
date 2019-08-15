from lib.Topics import Topics
from lib.WebsocketServerCore import WebSocketServerCore


class WebSocketServer(WebSocketServerCore):

    def __init__(self,eventBus, port=9000):
        super().__init__(eventBus, port)
        self.parserSubscription = None
        self.eventBus = eventBus

    def loadParser(self, receiverFunction):
        self.eventBus.unsubscribe(self.parserSubscription)
        self.parserSubscription = self.eventBus.subscribe(Topics.wsReceivedMessage, receiverFunction)

