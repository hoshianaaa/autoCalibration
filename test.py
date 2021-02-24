import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from lib.dobot import Dobot

bot = Dobot('/dev/dobot')
bot.home()
pose = bot.get_pose()
print('pose:',pose)
bot.move_to(250,0,40,0)
pose = bot.get_pose()
print('pose:',pose)
print(bot.get_end_effector_params())
