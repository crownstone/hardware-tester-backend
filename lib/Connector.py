from enum import Enum

from lib.Topics import Topics
from tests.__util.WSClientThread import WSClient

class Devices(Enum):
    lamp_5W_1         = 'lamp_5W_1'
    lamp_5W_2         = 'lamp_5W_2'
    lamp_20W          = 'lamp_20W'
    lamp_40W          = 'lamp_40W'
    lamp_100W_1       = 'lamp_100W_1'
    lamp_100W_2       = 'lamp_100W_2'
    lamp_100W_3       = 'lamp_100W_3'
    lamp_100W_4       = 'lamp_100W_4'
    blower_1          = 'blower_1'
    blower_2          = 'blower_2'
    exotic_load_1     = 'exotic_load_1'
    exotic_load_2     = 'exotic_load_2'
    exotic_load_3     = 'exotic_load_3'
    crownstone_heater = 'crownstone_heater'


class Connector:

    def __init__(self, eventBus, abortTest, nextStep):
        self.eventBus = eventBus
        self.abortCommand = abortTest
        self.nextStep = nextStep
        self.clientName = "ACTIVE_TEST"

        client = WSClient(self.eventBus)

        self.eventBus.on(Topics.wsReceivedMessageJSON, self.handleMessage)

        client.start()

    def handleMessage(self, jsonData):
        messageType = jsonData["type"]
        if messageType == "next":
            self.nextStep()
        elif messageType == "abort":
            self.abortCommand()

    def showIntroduction(self, title, description, expectedDuration, steps):
        pass

    def initializeTestOverview(self, showGraph=False):
        pass

    def setProgress(self, progress, label=None):
        pass

    def errorOverview(self, errorHeader, errorDescription, errorData):
        pass

    def showSuccess(self, description):
        pass

    def testAborted(self):
        pass

    def turnAllDevicesOff(self):
        pass

    def enableDevices(self, deviceList):
        pass

    def enableDevice(self, device):
        self.enableDevices([device])

    def disableDevices(self, deviceList):
        pass

    def disableDevice(self, device):
        self.disableDevices([device])

