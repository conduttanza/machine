#05/02/2026

from config import Config
config = Config()

import pigpio
from threading import Thread
import time


    
class Move():
    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            exit()
        self.PWM = 16
        self.AIN1 = 20
        self.AIN2 = 21
        self.pi.set_mode(self.MOTOR_1, pigpio.OUTPUT)
        self.delay =  config.delay
        self.run = config.run
        self.pi.set_PWM_frequency(self.AIN1,1000)
        Thread(target=self.update, daemon=False).start()
        
    def update(self):
        while self.run == True:
            self.moveFwd()
        self.stop()
    
    def moveFwd(self):
        self.pi.set_PWM_dutycycle(self.PWM,128)
        time.sleep(config.delay)
        self.run = False

    def stop(self):
        self.pi.set_PWM_dutycycle(self.AIN1,0)
        self.pi.stop()
