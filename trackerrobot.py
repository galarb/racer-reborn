motor_config = (18, 19, 5, 17, 85)

tracker = racer(motor_config, modebutton_pin=23, servo_pin=16, i2c=i2c)
'''
def robot_loop():
    while True:
        mode = tracker.get_modeflag()
        if mode == 0:  # mode0
            print('mode0')
            sleep(1)

        elif mode == 1:  # mode1
            print('mode1')
            sleep(1)

        elif mode == 2:  # mode2
            print('mode2')
            sleep(1)

_thread.start_new_thread(robot_loop, ())


'''    
