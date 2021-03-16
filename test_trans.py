import threading
import time
import rsAruco as ra
import cv2
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
from IPython import display

from lib.dobot import Dobot

from scipy.spatial import distance

x_min = 180
x_max = 260
y_min = -100
y_max = 100
z_min = -20
z_max = 100

def valid_pt(pt):
  if pt[0] >= x_min and pt[0] <= x_max:
    if pt[1] >= y_min and pt[1] <= y_max:
      if pt[2] >= z_min and pt[2] <= z_max:
        return True

  return False


### input calibration result ###
image_to_arm = [[78.74290364330686, 898.8805858748223, -395.16061310803207, 385.1951642424718], [976.8638451909984, -57.00955755166629, 47.52067042333153, -26.849053417368566], [22.958992016166274, -409.39970429420066, -913.4520402840946, 378.86352312168736], [1.3322676295501878e-15, 5.329070518200751e-15, -1.7763568394002505e-15, 1.0000000000000007]]
image_to_arm = np.array(image_to_arm)
###############################

thread1 = ra.cameraDetection(1, "rsArucoDetection")

# start to find aruco code
if thread1.isAlive()==False:
    print("camera starts!")
    thread1.start()

bot = Dobot('/dev/dobot')
bot.set_homing_parameters(217,0,154,0)
#bot.home()

while True:
  #print("wait")
  #time.sleep(3)

  #print("scan")

  pt = ra.center
  pt = np.append(pt,1)
#print(pt)
#print(image_to_arm)

  target = np.dot(image_to_arm,pt.T)
  target[0] = target[0] + 30
  print(target)

  if(valid_pt(target)):
    print("valid coordinate")
    #print("wait")
    #time.sleep(1)
    #bot.move_to( target[0], target[1], target[2] + 50, 0 )
    #bot.move_to( target[0], target[1], target[2], 0 )
    #bot.move_to( target[0], target[1], target[2] + 50, 0 )
    #bot.move_to( 217, 0, 154, 0 )
  else:
    print("invaid coordinate")
