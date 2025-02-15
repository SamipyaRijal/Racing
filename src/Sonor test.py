  #Add Phidgets Library
from Phidget22.Phidget import *
from Phidget22.Devices.DistanceSensor import *
#Required for sleep statement
import time

#Create
distanceSensor = DistanceSensor()

#Open
distanceSensor.openWaitForAttachment(1000)

#Use your Phidgets
while (True):
  try:
    print("Distance: " + str(distanceSensor.getDistance()) + " mm")
    time.sleep(1)
  except:
    print("couldn't read the distance")
    time.sleep(1)
  
