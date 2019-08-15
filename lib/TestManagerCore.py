import asyncio

class TestManagerCore:

    def __init__(self):
        self.__waiting = False
        self.__loop = asyncio.get_event_loop()

    def nextStep(self):
        self.__waiting


    def waitForEvent(self):
        self.__waiting = True
        self.__loop.run_until_complete(self.asyncWaitForEvents())

    async def asyncWaitForEvents(self):
        while self.__waiting:
            await asyncio.sleep(0.05)



