#Add Phidgets Library | You used Python's package manager to install the Phidget libraries on your computer. The import statements below give your program access to that code.
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *
#Required for sleep statement 
import time 
 
#Create | Create objects for your buttons and LEDs.
redButton = DigitalInput()
redLED =  DigitalOutput()
greenButton = DigitalInput()
greenLED = DigitalOutput()
 
#Address | Address your four objects which lets your program know where to find them.
redButton.setHubPort(0)
redButton.setIsHubPortDevice(True)
redLED.setHubPort(1)
redLED.setIsHubPortDevice(True)
greenButton.setHubPort(5)
greenButton.setIsHubPortDevice(True)
greenLED.setHubPort(4)
greenLED.setIsHubPortDevice(True)

#Open | Connect your program to your physical devices.
redButton.openWaitForAttachment(1000)
redLED.openWaitForAttachment(1000)
greenButton.openWaitForAttachment(1000)
greenLED.openWaitForAttachment(1000)

green_pressed = 0
red_pressed = 0
        
#Use your Phidgets | This code will turn on the LED when the matching button is pressed and turns off the LED when the matching button is released. The sleep function slows down the loop so the button state is only checked every 150ms.
while(1):
    if(redButton.getState()):
         red_pressed+=1
         redLED.setState(True)
         print("red is pressed")
    else:
        redLED.setState(False)
    if(greenButton.getState()):
        green_pressed+=1
        greenLED.setState(True)
        print("green is pressed")
    else:
        greenLED.setState(False)
    if(green_pressed == 10 or red_pressed == 10):
         break
    time.sleep(0.15)

if(red_pressed==10):
    for i in range(0,11):
        redLED.setState(True)
        time.sleep(1)
        redLED.setState(False)
        time.sleep(1)
        