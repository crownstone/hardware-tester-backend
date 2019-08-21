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

    crownstone_slot_1 = 'crownstone_slot_1'
    crownstone_slot_2 = 'crownstone_slot_2'




class TestTemplates(Enum):
    ProgressIndicator = "ProgressIndicator"
    # ProgressAndGraph  = "ProgressAndGraph"

class TestErrors(Enum):
    testAborted = "testAborted"
    testFailed  = "testFailed"
    testSuccess = "testSuccess"

class Connector:

    def __init__(self, eventBus, abortTest, nextStep, powerMeasurementReceived):
        self.eventBus = eventBus
        self.abortCommand = abortTest
        self.powerMeasurementReceived = powerMeasurementReceived
        self.nextStep = nextStep
        self.clientName = "ACTIVE_TEST"

        client = WSClient(self.eventBus)

        self.eventBus.on(Topics.wsReceivedMessageJSON, self.handleMessage)

        client.start()

    def handleMessage(self, jsonData):
        messageType = jsonData["type"]
        messageData = jsonData["data"]
        if messageType == "next":
            self.nextStep()
        elif messageType == "abort":
            self.abortCommand()
        elif messageType == "powerMeasurement":
            self.powerMeasurementReceived(messageData)


    def showIntroduction(self, title, description, expectedDuration, steps):
        pass

    def setTestTemplate(self, template):
        pass

    def setProgress(self, progress: int, totalProgress : int, label=None, showNextStepButton=False):
        return progress + 1

    def errorOverview(self, errorHeader, errorDescription, errorData):
        pass

    def showSuccess(self, description):
        pass

    def testAborted(self):
        pass

    def turnAllDevicesOff(self):
        listOfDevices = [
            Devices.lamp_5W_1,
            Devices.lamp_5W_2,
            Devices.lamp_20W,
            Devices.lamp_40W,
            Devices.lamp_100W_1,
            Devices.lamp_100W_2,
            Devices.lamp_100W_3,
            Devices.lamp_100W_4,
            Devices.blower_1,
            Devices.blower_2,
            Devices.exotic_load_1,
            Devices.exotic_load_2,
            Devices.exotic_load_3,
            Devices.crownstone_heater,
        ]
        self.turnDevicesOff(listOfDevices)

    def turnAllCrownstonesOff(self):
        listOfDevices = [
            Devices.crownstone_slot_1,
            Devices.crownstone_slot_2,
        ]
        self.turnDevicesOff(listOfDevices)

    def turnDevicesOn(self, deviceList):
        pass

    def turnDevicesOff(self, deviceList):
        pass

    def turnDeviceOn(self, device):
        self.turnDevicesOn([device])

    def turnCrownstoneOn(self, crownstoneIndex):
        if crownstoneIndex == 1:
            self.turnDevicesOn([Devices.crownstone_slot_1])
        elif crownstoneIndex == 2:
            self.turnDevicesOn([Devices.crownstone_slot_2])

    def turnDeviceOff(self, device):
        self.turnDevicesOff([device])

    def turnCrownstoneOff(self, crownstoneIndex):
        if crownstoneIndex == 1:
            self.turnDevicesOff([Devices.crownstone_slot_1])
        elif crownstoneIndex == 2:
            self.turnDevicesOff([Devices.crownstone_slot_2])


