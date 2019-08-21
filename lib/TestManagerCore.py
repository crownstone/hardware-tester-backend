import asyncio
import sys
import time

from BluenetLib import Bluenet, Util
from BluenetLib.BLE import BluenetBle

from lib.api import TestErrors, Connector
from tests.__util.util import findUartAddress, findUsbBleDongleHciIndex
from bluepy.btle import BTLEException

def gt():
    return "{:.3f}".format(time.time())

class TestManagerCore:

    def __init__(self, eventBus):
        self.bluenet = None
        self.bluenetBLE = None

        self.testRunning = False

        self.loop = asyncio.new_event_loop()

        self.step = 0
        self.api = Connector(eventBus, self.abortTest, self.nextStep, self.powerMeasurementReceived)

        self.macAddress1 = None
        self.macAddress2 = None


    def powerMeasurementReceived(self):
        pass

    def abortTest(self):
        """
        This method will be invoked by the connector when this test has to be aborted.
        Clean up your test and call api.testAborted() to tell the system that the test is ready.
        After this, this test should end.
        """
        self.endInError({"title":"Test Aborted"})

    def nextStep(self):
        self.step += 1
        self.run()






    async def wait(self, seconds):
        while seconds > 0 and self.testRunning:
            await asyncio.sleep(0.1)
            seconds -= 0.1
        if self.testRunning is False:
            raise TestErrors.testAborted

    async def initLibs(self):
        """
        This will start Bluenet and any other libs that we require for the tests.
        :return:
        """
        self.bluenet = Bluenet()
        try:
            address = findUartAddress()
            if not address:
                self.endInError({"title":"E_TESTER_NOT_WORKING"})
                return False
            else:
                self.bluenet.initializeUSB(address)
        except:
            print(gt(), "----- ----- Error in setting UART Address", sys.exc_info()[0])
            self.endInError({"title":"E_TESTER_NOT_WORKING"})
            return False

        print(gt(), "----- Initializing Bluenet Libraries")
        self.bluenetBLE = BluenetBle(hciIndex=findUsbBleDongleHciIndex())
        self.bluenetBLE.setSettings(
            adminKey=           "adminKeyForCrown",
            memberKey=          "memberKeyForHome",
            basicKey=           "guestKeyForOther",
            serviceDataKey=     "guestKeyForOther",
            localizationKey=    "localizationKeyX",
            meshApplicationKey= "meshKeyForStones",
            meshNetworkKey=     "meshAppForStones",
        )


    def run(self):
        raise NotImplementedError()


    def endInError(self, header, description="", data=""):
        self.cleanup()
        self.api.errorOverview(
            header,
            description,
            data,
        )
        raise TestErrors.testFailed


    def endInSuccess(self):
        self.cleanup()
        self.api.showSuccess("SUCCESS!")

        raise TestErrors.testSuccess

    def cleanup(self):
        self.testRunning = False
        self.api.turnAllDevicesOff()
        self.api.turnAllCrownstonesOff()
        if self.bluenet is not None:
            self.bluenet.stop()
            self.bluenet = None

        if self.bluenetBLE is not None:
            self.bluenetBLE.shutDown()
            self.bluenetBLE = None


# BLUETOOTH METHODS

    async def setupCrownstone(self, crownstoneIndex):
        self.api.turnAllCrownstonesOff()
        await self.wait(0.1)
        self.api.turnCrownstoneOn(crownstoneIndex)
        await self.wait(0.1)

        macAddress = await self.getMacAddress(-40)
        if crownstoneIndex == 1:
            self.macAddress1 = macAddress
        else:
            self.macAddress2 = macAddress

        await self.setupCrownstone(crownstoneIndex)
        await self.checkForNormalMode(crownstoneIndex)

    async def recoverCrownstone(self, crownstoneIndex):
        if (crownstoneIndex == 1 and self.macAddress1 is None) or (crownstoneIndex == 2 and self.macAddress2 is None):
            self.endInError("No mac address to recover")

        self.api.turnCrownstoneOff(crownstoneIndex)
        await self.wait(0.5)
        self.api.turnCrownstoneOn(crownstoneIndex)



    async def getMacAddress(self, maxRssi: int):
        nearest = self.bluenetBLE.getNearestSetupCrownstone(maxRssi, returnFirstAcceptable=True)
        if nearest is not None:
            return nearest["address"]
        else:
            self.endInError("Could not find Crownstone in setup mode.", data=f"Max Rssi = {maxRssi}")

    async def performSetup(self, crownstoneIndex):
        print(gt(), "----- Setting up Crownstone...")
        try:
            address = self.macAddress1
            if crownstoneIndex == 2:
                address = self.macAddress2
            # BLE --> BLE fast setup --> THIS TURNS THE RELAY ON AUTOMATICALLY
            self.bluenetBLE.setupCrownstone(
                address,
                sphereId=1,
                crownstoneId=crownstoneIndex,
                meshAccessAddress=Util.generateMeshAccessAddress(),
                meshDeviceKey="itsMyDeviceKeyyy",
                ibeaconUUID="1843423e-e175-4af0-a2e4-31e32f729a8a",
                ibeaconMajor=123,
                ibeaconMinor=456
            )
        except:
            err = sys.exc_info()[0]
            if type(sys.exc_info()[0]) is BTLEException:
                print(gt(), "----- Crownstone might have failed to setup... BTLE", err.message, err.__str__())
            else:
                print(gt(), "----- Crownstone might have failed to setup... checking...", err)


    async def checkForNormalMode(self, crownstoneIndex):
        address = self.macAddress1
        if crownstoneIndex == 2:
            address = self.macAddress2

        print(gt(), "----- Checking if Crownstone is in normal mode...")
        # BLE--> Check for advertisements in normal mode
        isInNormalMode = self.bluenetBLE.isCrownstoneInNormalMode(address, scanDuration=5, waitUntilInRequiredMode=True)
        if isInNormalMode is None:
            self.endInError("No Crownstone found in normal mode.")
        elif not isInNormalMode:
            self.endInError("Could not setup Crownstone.")

        print(gt(), "----- Setup was successful. Crownstone is in normal mode")