import os, time

from lib.EventBus import EventBus
from lib.TestRunner import TestRunner
from lib.WebsocketServer import WebSocketServer

baseDir = './tests/'


def getTests():
    testToRun = None

    for filename in os.listdir(baseDir):
        if filename != "__util":
            subPath = os.path.join(baseDir, filename)
            if os.path.isdir(subPath):
                runPath = os.path.join(subPath, 'run_test.py')
                if os.path.exists(runPath):
                    testToRun = runPath
                    print("Test called", filename, "found!")
                else:
                    print("ERR: Test called", filename, "found without run_test.py!")

    return testToRun


if __name__ == "__main__":
    test = getTests()
    eventBus = EventBus()
    myRunner = TestRunner(eventBus)
    server = WebSocketServer(eventBus, 9000)
    myRunner.startTest(test)
    server.start() # <-- this is blocking
