import os, subprocess, sys, time, traceback

class TestRunner:
    def __init__(self, eventBus):
        self.running = False
        self.session = None
        self.eventBus = eventBus

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        # kill all processes. LED goes off. Button is ignored!
        print("TestRunner: Cleaning up")
        self.running = False
        if self.session is not None:
            print("TestRunner: Terminating Test")
            try:
                self.session.terminate()
            except:
                print("TestRunner: Error terminating Test", sys.exc_info()[0])
                traceback.print_exc()
            try:
                print("TestRunner: Waiting to terminate Test")
                self.session.wait(1)
                print("TestRunner: Test has been Terminated.")
            except:
                traceback.print_exc()
                print("TestRunner: Terminate not successful. Killing Test now.", sys.exc_info()[0])
                if self.session is not None:
                    self.session.kill()
                time.sleep(1)
            self.session = None

    def startTest(self, testToRun):
        print("Start running", testToRun)
        self.running = True
        self.session = subprocess.Popen(["sudo", "python3", testToRun], preexec_fn=os.setsid)

