import time
from ev3lego_zk import ev3lego_zk
from tm1650_1 import TM1650
from ModeButton import ModeButton
from Ultrasonic import Ultrasonic
from pid import PID
from MotorController import MotorController
import neopixel
from machine import Pin, SoftI2C
from i2c_lcd import I2cLcd
from time import sleep

encoder1_pin = 36
encoder2_pin = 39
in1_pin = 26
in2_pin = 25
wheel_size = 85 # wheel size (in mm)
trig_pin = 13
echo_pin = 14
leds_pin = 23
NUM_LEDS = 2
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

# Create objects
robot = ev3lego_zk(encoder1_pin, encoder2_pin, in1_pin, in2_pin, wheel_size)
display = TM1650(18, 19)
mode_button = ModeButton(pin_num=35, modes=4)
pid = PID(54, 168, 4.3)
us = Ultrasonic(trig_pin, echo_pin)
controller = MotorController(robot, pid, us)
np = neopixel.NeoPixel(Pin(leds_pin), NUM_LEDS)
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=100000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
            
def set_color(i, r, g, b):
    np[i] = (g, r, b)  # Swap R and G
def blink_idle():
    set_color(0, 255, 0, 0)   # Red
    set_color(1, 0, 255, 0)   # Green
    np.write()
    time.sleep(0.5)

    # Swap colors
    set_color(0, 0, 255, 0)   # Green
    set_color(1, 255, 0, 0)   # Red
    np.write()
    time.sleep(0.5)
    
    
while True:
    mode_button.update()      # <---- REQUIRED
    
    mode = mode_button.get_mode()
    

    if mode == 0:
        lcd.hal_backlight_on()
        print('run distance measurement')
        lcd.move_to(8, 0)
        lcd.putstr("Mode 0")
        set_color(0, 0, 0, 255)  # real BLUE    
        #set_color(1, 0, 0, 255)  # real BLUE
        np.write()
        d = us.distance_cm()
        if d is None:
            print("Out of range")
        else:
            print("Distance: {:.1f} cm".format(d))
            display.ShowNum(int(d))
            display.displayDot(4, 1)
       
        time.sleep(1)

    elif mode == 1:
        lcd.move_to(8, 0)
        lcd.putstr("Mode 1")
        print('run motor encoder')
        set_color(0, 0, 255, 0)  # real GREEN    
        #set_color(1, 0, 255, 0)  # real GREEN
        np.write()

        controller.go_degrees(180)
        #robot.motgo(200)
        display.ShowNum(robot.degrees)
        display.displayDot(4, 0)
  
        time.sleep(1)
        robot.brake() 


    elif mode == 2:
        lcd.move_to(8, 0)
        lcd.putstr("Mode 2")
        print('go to 20 cm')
        set_color(0, 80, 0, 80)     
        #set_color(1, 80, 0, 80)
        np.write()
        #controller.go_us(20, 100)
        controller.go_degrees(0)

        display.ShowNum(int(us.distance_cm()))
        robot.brake() 

        time.sleep(1)
        
        
    elif mode == 3:
        lcd.backlight_off()
        
        print('run_idle()')
        robot.brake() 
        robot.degrees = 0
        display.ShowStr('IdLE')
        blink_idle()        



robot.brake() 
robot.stop()
