import sys, os, time, asyncio
# this has to be on top of the run_test.py file in order for path resolving to work properly.
from BluenetLib import Bluenet
from BluenetLib.BLE import BluenetBle

from lib.TestManagerCore import TestManagerCore
from tests.__util.util import findUsbBleDongleHciIndex, findUartAddress

sys.path.append(os.path.abspath(os.path.join(os.path.join(os.path.dirname( __file__ ), '..'), '..')))

from lib.api import Connector, TestErrors
from lib.EventBus import EventBus

eventBus = EventBus()

"""
The process of a test is as follows:
    - introduction
            - here we explain the test and list any required preparation work.
            - we outline the steps and give a general ETA
    - setTestTemplate
            - Determine the best test template for your test
    - run the test
            - Use the API to enable/disable devices
            - At any time call the setProgress method on the API to indicate progress. You can add a label to explain the currently active step.
            - If there is a user action required, you can add the showNextStepButton argument to the setProgress, which will trigger your "nextStep" callback.
            - On failure of the test, cleanup and you call API.errorOverview
            - On success of the test, cleanup and you call API.showSuccess
"""
class TestManager (TestManagerCore):

    def __init__(self):
        super().__init__(eventBus)

    def run(self):
        if self.step == 0:
            self.api.showIntroduction(
                "This is the test.",
                "We will turn on the light, and the Crownstone will see it!",
                "20 seconds",
                ["Turn on light", "Measure the power"]
            )
        elif self.step == 1:
            self.testRunning = True
            self.loop.run_until_complete(self.startTest())


    async def startTest(self):
        progress = 0
        totalProgress = 20

        try:
            self.api.turnAllDevicesOff()
            self.api.turnAllCrownstonesOff()
            await self.wait(0.3)

            progress = self.api.setProgress(progress, totalProgress, "Initializing Libs...")
            await self.initLibs()

            progress = self.api.setProgress(progress, totalProgress, "Setting up Crownstone 1...")
            await self.setupCrownstone(1)
            progress = self.api.setProgress(progress, totalProgress, "Setting up Crownstone 2...")
            await self.setupCrownstone(2)

            progress = self.api.setProgress(progress, totalProgress, "Recovering Crownstone 1...")
            self.api.turnCrownstoneOff(1)
            await self.wait(0.5)
            self.api.turnCrownstoneOn(1)
            await self.recoverCrownstone(1)

            progress = self.api.setProgress(progress, totalProgress, "Setting up Crownstone 1 after recovery...")
            await self.setupCrownstone(1)


        except TestErrors:
            """
            We expect something else has already called self.endInError
            """
            return
        except:
            self.endInError({
                "title":"Unexpected Error!",
                "description":"fatal fatal",
                "data":sys.exc_info()[0]
            })


    def cleanup(self):
        super().cleanup()