#05/02/2026

from config import Config
config = Config()
from window import Window
import pigpio
from threading import Thread
import time

class Servo():
    def __init__(self, window):
        self.window = window
        self.pi = pigpio.pi()
        if not self.pi.connected:
            exit()
        self.servo_1_pin = config.servo_1
        self.servo_2_pin = config.servo_2
        self.pi.set_servo_pulsewidth(self.servo_1_pin,1500)
        self.pi.set_servo_pulsewidth(self.servo_2_pin,1500)
        Thread(target=self.update, daemon=True).start()
        
    def update(self):
        while True:
            self.angle_1 = getattr(self.window, 'servo_1_angle', 0)*(4000/(config.slider_len))+1500
            self.angle_2 = getattr(self.window, 'servo_2_angle', 0)*(4000/(config.slider_len))+1500
            self.pi.set_servo_pulsewidth(self.servo_1_pin,self.angle_1)
            self.pi.set_servo_pulsewidth(self.servo_2_pin,self.angle_2)
    
    def stop(self):
        self.pi.set_servo_pulsewidth(self.servo_1_pin, 0)
        self.pi.set_servo_pulsewidth(self.servo_2_pin, 0)

class Motor():
    def __init__(self, window):
        self.window = window
        self.pi = pigpio.pi()
        if not self.pi.connected:
            exit()
        self.PWM = 16
        self.AIN1 = 20
        self.AIN2 = 21
        for pin in (self.AIN1, self.AIN2):
            self.pi.set_mode(pin, pigpio.OUTPUT)
        self.delay =  config.delay
        self.pi.set_PWM_frequency(self.PWM,1000)
        Thread(target=self.update, daemon=True).start()
        
    def update(self):
        self.speed = 0
        while True:
            if getattr(self.window, 'motor_move', False):
                self.targetSpeed = getattr(self.window, 'speed', 8)
                #print(f'self.speed = {self.speed}')
                if self.targetSpeed >= 0:
                    if self.speed > self.targetSpeed + 7:
                        self.speed -= 8
                    elif self.speed < self.targetSpeed - 7:
                        self.speed += 8
                    if self.speed > 255:
                        self.speed = 255
                    elif self.speed < 0:
                        self.speed = 0
                    self.moveFwd()
                elif self.targetSpeed < 0:
                    if self.speed > self.targetSpeed + 7:
                        self.speed -= 8
                    elif self.speed < self.targetSpeed - 7:
                        self.speed += 8
                    if self.speed < -255:
                        self.speed = -255
                    elif self.speed > 0:
                        self.speed = 0
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
        self.pi.write(self.AIN1, 1)
        self.pi.write(self.AIN2, 0)
        self.pi.set_PWM_dutycycle(self.PWM,self.speed)
    
    def moveBack(self):
        self.pi.write(self.AIN1,0)
        self.pi.write(self.AIN2,1)
        self.pi.set_PWM_dutycycle(self.PWM,-self.speed)

    def stop(self):
        self.pi.set_PWM_dutycycle(self.PWM,0)
        self.pi.write(self.AIN1, 0)
        self.pi.write(self.AIN2, 0)
    
    def cleanUp(self):
        self.pi.stop()


