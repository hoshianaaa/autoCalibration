import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from lib.dobot import Dobot

bot = Dobot('/dev/dobot')
#bot.home()
pose = bot.get_pose()
print('pose:',pose)
bot.move_to(250,0,40,0)
pose = bot.get_pose()
print('pose:',pose)
bot.set_end_effector_params(66.0,0.0,0.0)
print(bot.get_end_effector_params())
