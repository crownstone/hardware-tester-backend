import sys, os
# this has to be on top of the run_test.py file in order for path resolving to work properly.
from lib.TestManagerCore import TestManagerCore

sys.path.append(os.path.abspath(os.path.join(os.path.join(os.path.dirname( __file__ ), '..'), '..')))

from lib.Connector import Connector
from lib.EventBus import EventBus

eventBus = EventBus()



class TestManager:

    def __init__(self):
        super().__init__()

        self.step = 0
        self.api = Connector(eventBus, self.abortTest, self.nextStep)

    def abortTest(self):
        """
        This method will be invoked by the connector when this test has to be aborted.
        Clean up your test and call api.testAborted() to tell the system that the test is ready.
        After this, this test should end.
        """
        pass

    def nextStep(self):
        self.step += 1
        self.run()

    def run(self):
        if self.step == 0:
            self.api.showIntroduction(
                "This is the test.",
                "We will turn on the light, and the Crownstone will see it!",
                "20 seconds",
                ["Turn on light", "Measure the power"]
            )
        elif self.step == 1:
            pass








