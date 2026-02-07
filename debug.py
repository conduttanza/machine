#07/02/2026

from config import Config
config = Config()
from window import Window
from threading import Thread
import time
    
class Move_not_pi():
    def __init__(self, window):
        print('not pi')
        self.window = window
        self.delay =  config.delay
        Thread(target=self.update, daemon=True).start()
        
    def update(self):
        self.speed = 0
        while True:
            if getattr(self.window, 'move', False):
                self.targetSpeed = getattr(self.window, 'speed', 8)
                #print(f'self.speed = {self.speed}')
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
        print(f'speed: {self.speed}')
    
    def moveBack(self):
        #print('moving bwd')
        print(f'speed: {self.speed}')

    def stop(self):
        pass#print('idle')
        

window = Window.__new__(Window)
window.running = True
window.move = False
import pygame
pygame.init()
pygame.display.set_caption('motor movement')
window.screen = pygame.display.set_mode((600,600))
window.clock = pygame.time.Clock()
move = Move_not_pi(window)

window.main()

