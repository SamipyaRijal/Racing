#Add Phidgets Library
from Phidget22.Phidget import *
import time
from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput

# Create
slider = VoltageRatioInput()

# Address
slider.setHubPort(3)
slider.setIsHubPortDevice(True)

# Open
slider.openWaitForAttachment(5000)

def get_slider_value():
    return slider.getVoltageRatio()

if __name__ == "__main__":
    while True:
        print("Slider Value: " + str(get_slider_value()))
        time.sleep(0.1)