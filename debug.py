#07/02/2026

from config import Config
config = Config()
from window import Window
from threading import Thread
import time

class Servo_not_pi():
    def __init__(self, window):
        self.window = window
        Thread(target=self.update, daemon=True).start()
        
    def update(self):
        while True:
            self.angle = getattr(self.window, 'servo_angle', 0)*(4000/(config.slider_len))+1500
            if getattr(self, 'angle',1500) != 1500:
                print(f'angle: {self.angle}')
    
    def stop(self):
        print('stop')

class Motor_not_pi():
    def __init__(self, window):
        print('not pi')
        self.window = window
        self.delay =  config.delay
        Thread(target=self.update, daemon=True).start()
        
    def update(self):
        self.speed = 0
        while True:
            if getattr(self.window, 'move', False):
                self.targetSpeed = getattr(self.window, 'speed', 0)
                #print(f'self.speed = {self.targetSpeed}')
                if self.targetSpeed >= 0:
                    if self.speed > self.targetSpeed + 7:
                        self.speed -= 8
                    elif self.speed < self.targetSpeed - 7:
                        self.speed += 8
                    self.moveFwd()
                elif self.targetSpeed < 0:
                    if self.speed > self.targetSpeed + 7:
                        self.speed -= 8
                    elif self.speed < self.targetSpeed - 7:
                        self.speed += 8
                    self.moveBack()
            if getattr(self.window, 'move') == False:
                actSpeed = getattr(self,'speed')
                if actSpeed < 0:
                    #print('backwards')
                    #self.moveBack()
                    self.speed +=8
                else:
                    #self.moveFwd()
                    self.speed -= 8
                if -12 < actSpeed < 12:
                    self.stop()
                    self.speed = 0
            time.sleep(config.delay)
    
    def moveFwd(self):
        #print('moving fwd')
        print(f'speed: {self.speed}')
    
    def moveBack(self):
        #print('moving bwd')
        print(f'speed: {self.speed}')

    def stop(self):
        pass#print('idle')

