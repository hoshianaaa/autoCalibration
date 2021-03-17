import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import time

from lib.dobot import Dobot

bot = Dobot('/dev/dobot')

while True:
  pos = bot.get_pose()
  print(pos)
  time.sleep(0.3)
