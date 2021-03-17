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
z_min = -60
z_max = 100

def valid_pt(pt):
  if pt[0] >= x_min and pt[0] <= x_max:
    if pt[1] >= y_min and pt[1] <= y_max:
      if pt[2] >= z_min and pt[2] <= z_max:
        return True

  return False

def pick_up(pos):
    bot.move_to( pos[0], pos[1], pos[2] + 30, 0 )
    bot.move_to( pos[0], pos[1], pos[2] - 2, 0 )
    bot.suc_on()
    time.sleep(1)
    bot.move_to( pos[0], pos[1], pos[2] + 30, 0 )

def place(pos):
    bot.move_to( pos[0], pos[1], pos[2] + 30, 0 )
    bot.move_to( pos[0], pos[1], pos[2], 0 )
    bot.suc_off()
    time.sleep(1)
    bot.move_to( pos[0], pos[1], pos[2] + 30, 0 )

### input calibration result ###
image_to_arm =   [[-26.239127019560645, 933.407153515323, -340.52739510876444, 380.05895055467505], [976.7883127139744, 13.032098127671276, -25.712268548712153, 2.5027129395039545], [-30.53449372506436, -338.27275577186344, -927.8996419314769, 389.1539650837111], [-2.220446049250313e-16, 0.0, 0.0, 1.0000000000000004]]
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

time.sleep(2)
counter = 0

g_pos = [40,261,-45,0]

while True:

  #print("wait")
  #time.sleep(2)

  print("scan")

  pt = ra.center
  pt = np.append(pt,1)
#print(pt)
#print(image_to_arm)

  t_pos = np.dot(image_to_arm,pt.T)
  t_pos[0] = t_pos[0] + 40
  print(t_pos)

  if(valid_pt(t_pos)):
    print("valid coordinate")
    time.sleep(1)

    pick_up(t_pos)
    
    if (counter == 0):
      place(g_pos)

    elif (counter == 1):
      g_pos[1] = g_pos[1] - 30
      place(g_pos)

    elif (counter <= 2):
      g_pos[2] = g_pos[2] + 20
      place(g_pos)

    elif (counter == 3):
      g_pos[1] = g_pos[1] - 30

    elif (counter <= 5):
      g_pos[2] = g_pos[2] + 20
      place(g_pos)

    counter = counter + 1

    if (counter > 6):
      bot.move_to( 217, 0, 154, 0 )
      while True:
        print("finish")
        time.sleep(1)

  else:
    print("invaid coordinate")
