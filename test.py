import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from lib.interface import Interface

bot = Interface('/dev/dobot')

print('Bot status:', 'connected' if bot.connected() else 'not connected')

params = bot.get_homing_paramaters()
print('Params:', params)

print('Homing')
#bot.set_homing_command(0)
bot.set_homing_parameters(250, 0, 0, 0)
params = bot.get_homing_paramaters()
print(params)

params = bot.get_end_effector_params()
print(params)
