

### input calibration result ###
image_to_arm = []
###############################

thread1 = ra.cameraDetection(1, "rsArucoDetection")

# start to find aruco code
if thread1.isAlive()==False:
    print("camera starts!")
    thread1.start()

bot = Dobot('/dev/dobot')
bot.set_homing_parameters(217,0,154,0)
bot.home()

pt = ra.center

target_point = np.dot(image_to_arm,pt)

bot.move_to( 217, 0, 154, 0 )
