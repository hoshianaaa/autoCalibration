
# coding: utf-8
# Author: Francis (Github @heretic1993)
# License: MIT

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


thread1 = ra.cameraDetection(1, "rsArucoDetection")

def showImg():
    while True:
#         display.clear_output(wait=True)
        cv2.imwrite('./color.jpg', ra.color_image)
#         img=Image.open(r'./color.jpg')
#         plt.imshow(img)
    
thread2 = threading.Thread(target=showImg)

# start to find aruco code
if thread1.isAlive()==False:
    print("camera starts!")
    thread1.start()
    
time.sleep(2)
if thread2.isAlive()==False:
    print("showImg starts!")
    thread2.start()



#dobot init


bot = Dobot('/dev/dobot')
bot.set_homing_parameters(217,0,100,0)
bot.home()
#bot.gripper_open()
#time.sleep(5)
#bot.gripper_close()
bot.suc_on()
time.sleep(5)

# Calibration points
default_cali_points = [[180,-100,30,0],[260,-100,30,0],
                       [180,100,30,0],[260,100,30,0],
                       [260,120,-30,0],[180,120,-30,0],
                       [180,-120,-30,0],[260,-120,-30,0]]

np_cali_points = np.array(default_cali_points)
arm_cord = np.column_stack((np_cali_points[:,0:3], np.ones(np_cali_points.shape[0]).T)).T


# clear queue
#dType.SetQueuedCmdClear(api)
#dType.SetQueuedCmdStartExec(api)

centers=np.ones(arm_cord.shape)

for ind,pt in enumerate(default_cali_points):
    print("Current points:", pt)
#     dType.SetQueuedCmdStopExec(api)
#     dType.SetQueuedCmdClear(api)
    #queuedCmdIndex = dType.SetPTPCmd(api, 1, pt[0], pt[1], pt[2], pt[3], isQueued=0);
    #while dType.GetQueuedCmdCurrentIndex(api) != queuedCmdIndex:
    #    time.sleep(1)

    bot.move_to( pt[0], pt[1], pt[2], pt[3] )

    time.sleep(2)
    centers[0:3,ind]=ra.center
    time.sleep(1)
    print(ra.center)
    

image_to_arm = np.dot(arm_cord, np.linalg.pinv(centers))
arm_to_image = np.linalg.pinv(image_to_arm)
#dType.SetPTPCmd(api, 1, 217,0,154,0, isQueued=0);
#dType.SetQueuedCmdStopExec(api);
bot.move_to( 217, 0, 125, 0 )

print("Finished")
print("Image to arm transform:\n", image_to_arm)
print("Image to arm transform list :\n", image_to_arm.tolist())

print("-------------------")
print("Image_to_Arm")
print("-------------------")
d_list = []
for ind, pt in enumerate(centers.T):
    x = default_cali_points[ind][0:3]
    y = np.dot(image_to_arm, np.array(pt))[0:3]
    print("Expected:", x)
    print("Result:", y)
    d = distance.euclidean(x, y)
    print(d)
    d_list.append(d)

print("error_mean:",sum(d_list)/len(d_list))

#bot.gripper_off()
bot.suc_off()
    
    
"""
print("-------------------")
print("Arm_to_Image")
print("-------------------")
#d_list = []
for ind, pt in enumerate(default_cali_points):
    x = centers.T[ind][0:3]
    y = np.dot(arm_to_image, np.array(pt))[0:3]
    print("Expected:", x)
    pt[3]=1
    print("Result:", y)
#    d = distance.euclidean(x, y)
#    print(d)
#    d_list.append(d)
 
#print("error_mean:",sum(d_list)/len(d_list))

"""
