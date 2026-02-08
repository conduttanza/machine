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
            self.angle_1 = getattr(self.window, 'servo_1_angle', 0)*(4000/(config.slider_len))+1500
            self.angle_2 = getattr(self.window, 'servo_2_angle', 0)*(4000/(config.slider_len))+1500
            print(f'angle 1: {round(self.angle_1)}',f'angle 2: {round(self.angle_2)}')
            time.sleep(config.delay)
    
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
            if getattr(self.window, 'motor_move', False):
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
            if getattr(self.window, 'motor_move') == False:
                actSpeed = getattr(self,'speed')
                if actSpeed < 0:
                    #print('backwards')
                    self.moveBack()
                    self.speed +=8
                else:
                    self.moveFwd()
                    self.speed -= 8
                if -12 < actSpeed < 12:
                    self.stop()
                    self.speed = 0
            time.sleep(config.delay)
    
    def moveFwd(self):
        #print('moving fwd')
        if getattr(self, 'speed') != 0:
            print(f'speed: {self.speed}')
    
    def moveBack(self):
        #print('moving bwd')
        if getattr(self, 'speed') != 0:
            print(f'speed: {self.speed}')

    def stop(self):
        pass#print('idle')

