
def findUartAddress():
    import subprocess
    from subprocess import Popen, PIPE

    session = subprocess.Popen(['ls', "/dev"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    session.terminate()

    devList = stdout.decode("utf-8").split("\n")

    usbIndex = 0

    for device in devList:
        if "ACM" in device:
            return "/dev/" + device

    return False


def findUsbBleDongleHciIndex():
    import subprocess
    from subprocess import Popen, PIPE

    session = subprocess.Popen(['hciconfig'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    session.terminate()

    hciInfoArray = str(stdout).split("hci")
    hciInfoArray.pop(0)

    usbIndex = 0

    for device in hciInfoArray:
        if "USB" in device:
            break
        usbIndex += 1

    return usbIndex
