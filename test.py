import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import time

from lib.dobot import Dobot

bot = Dobot('/dev/dobot')
bot.set_homing_parameters(217,0,134,0)
bot.home()
bot.move_to(217,0,154,0)
print(bot.get_end_effector_params())

default_cali_points = [[180,-120,135,0],[260,-120,135,0],
                       [180,120,135,0],[260,120,135,0],
                       [260,120,-5,0],[180,120,-5,0],
                       [180,-120,-5,0],[260,-120,-5,0]]

for ind,pt in enumerate(default_cali_points):

    bot.move_to( pt[0], pt[1], pt[2], pt[3] )

    time.sleep(2)
 
