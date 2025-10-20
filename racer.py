from machine import Pin, PWM, I2C
from time import sleep
from simplemotordriver import simplemotordriver
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

class racer:
    def __init__(self, motor_config, modebutton_pin, servo_pin, i2c):
        enc1, enc2, in1, in2, wheel_size = motor_config

        # Initialize motor driver
        self.motor = simplemotordriver(enc1, enc2, in1, in2, wheel_size)

        # I2C LCD setup
        self.i2c = i2c
        lcd_addr = self.i2c.scan()[0]  # find LCD automatically
        self.lcd = I2cLcd(self.i2c, lcd_addr, 4, 20)
        self.lcd.hal_backlight_on()
        self.lcd.clear()
        self.lcd.putstr("Ready...")

        # Button setup
        self.modeflag = 0
        self.modebutton = Pin(modebutton_pin, Pin.IN, Pin.PULL_UP)
        self.modebutton.irq(trigger=Pin.IRQ_FALLING, handler=lambda p: self.changemode())

        # Servo setup (cleanup + new PWM)
        try:
            PWM(Pin(servo_pin)).deinit()
        except:
            pass
        self.servo_pin = Pin(servo_pin, Pin.OUT)
        self.servo = PWM(self.servo_pin)
        self.servo.freq(50)  # typical for hobby servo

    def get_modeflag(self):
        return self.modeflag

    def changemode(self):
        self.modeflag = (self.modeflag + 1) % 3  # cycles 0–2
        mode_text = ["IDLE MODE", "HUNT MODE", "MANUAL MODE"][self.modeflag]

        print(f"Mode changed to: {mode_text}")

        # LCD feedback
        self.lcd.clear()
        self.lcd.putstr("Mode:\n" + mode_text)
        if self.modeflag==1:
            self.lcd.hal_backlight_off()

    
