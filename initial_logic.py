#05/02/2026

from config import Config
config = Config()
from window import Window
window = Window()
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
        for pin in self.AIN1, self.AIN2:
            self.pi.set_mode(pin, pigpio.OUTPUT)
        self.delay =  config.delay
        self.run = config.run
        self.pi.set_PWM_frequency(self.PWM,1000)
        Thread(target=self.update, daemon=False).start()
        
    def update(self):
        if self.run == True:
            self.moveFwd()
        #self.stop()
        self.run = window.returnTrue() or False
    
    def moveFwd(self):
        self.pi.write(self.AIN1, 1)
        self.pi.write(self.AIN2, 0)
        self.pi.set_PWM_dutycycle(self.PWM,128)
        time.sleep(config.delay)
        self.run = False

    def stop(self):
        self.pi.set_PWM_dutycycle(self.PWM,0)
        self.pi.write(self.AIN1, 0)
        self.pi.write(self.AIN2, 0)
        self.pi.stop()
