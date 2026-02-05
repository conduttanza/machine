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
        if self.run == True:
            GPIO.output(MOTOR_1,GPIO.HIGH)
            time.sleep(self.delay)
            self.run = False
        else:
            GPIO.cleanup()