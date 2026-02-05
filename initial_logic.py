#05/02/2026

from run import Config
config = Config()

import RPi.GPIO as GPIO
from threading import Thread
import time

MOTOR_1 = 18
MOTOR_2 = None

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_1, GPIO.OUT)

class Move():
    def __init__(self):
        self.delay =  config.delay
        self.run = config.run
        Thread(target=self.update, daemon=False).start()
        
    def update(self):
        self.moveFwd()
    
    def moveFwd(self):
        pwm = GPIO.PWM(MOTOR_1, 500)
        if self.run == True:
            pwm.start(0)
            pwm.ChangeDutyCycle(50)
            time.sleep(self.delay)
            self.run = False
        else:
            pwm.stop()
            GPIO.cleanup()