import asyncio, threading, sys, time, json

from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory

from lib.EventBus import EventBus
from lib.Topics import Topics


class MyClientProtocol(WebSocketClientProtocol):

    def __init__(self, retryCallback, eventBus):
        super().__init__()

        self.eventBus = eventBus
        self.retryCallback = retryCallback
        self.expectingPong = False
        self.terminated = False
        self.eventBus.on(Topics.wsReceivedMessageJSON, self._sendMessage)

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onConnecting(self, transport_details):
        print("Connecting; transport details: {}".format(transport_details))
        return None  # ask for defaults


    def _sendMessage(self, jsonData):
        self.sendMessage(json.dumps(jsonData))


    def onOpen(self):
        print("WebSocket connection open.")

        def pingPong():
            if self.expectingPong:
                if not self.terminated:
                    self.retryCallback()
                    return
            self.sendMessage(u"ping".encode('utf8'))
            self.expectingPong = True
            self.factory.loop.call_later(1, pingPong)

        # start sending messages every second ..
        pingPong()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            textMessage = payload.decode('utf8')
            if textMessage == 'pong':
                self.expectingPong = False
            else:
                data = json.load(textMessage)
                self.eventBus.emit(Topics.wsReceivedMessageJSON, data)



    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.terminated = True
        self.retryCallback()



class WSClient(threading.Thread):

    def __init__(self, eventBus):
        self.clientActive = False
        self.socketActive = False

        self.factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
        self.factory.protocol = lambda: MyClientProtocol(self.retry, eventBus)
        self.loop = asyncio.get_event_loop()
        self.closingLoop = asyncio.new_event_loop()

        threading.Thread.__init__(self)

    def __del__(self):
        print("cleaning up")
        self.cleanup()

    def run(self):
        self.startWebsocket()

    def cleanup(self):
        self.clientActive = False
        self.socketActive = False

    def retry(self):
        self.socketActive = False

    def startWebsocket(self):
        self.clientActive = True
        try:
            self.loop.run_until_complete(self.attempt())
        except KeyboardInterrupt as e:
            self.cleanup()

    async def attempt(self):
        while self.clientActive:
            self.socketActive = True
            await self.tryToConnect()
            await asyncio.sleep(0.5)

    async def tryToConnect(self):
        try:
            await self.loop.create_connection(self.factory, '127.0.0.1', 9000)
            await self.waitToFinish()
        except ConnectionRefusedError as err:
            pass

    async def waitToFinish(self):
        while self.socketActive:
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    eventBus = EventBus()
    client = WSClient(eventBus)
    client.start()