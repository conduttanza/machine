#import os
#os.environ['SDL_VIDEODRIVER'] = 'x11'       # ensure X11 driver
#os.environ['SDL_OPENGL'] = 'software'       # use software OpenGL
import pygame
from config import Config
config = Config()

class Window():
    def __init__(self):
        self.running = True
        self.move = False
        self.move_slider = False
        pygame.init()
        pygame.display.set_caption('motor movement')
        self.screen = pygame.display.set_mode((600,600))
        self.clock = pygame.time.Clock()
        self.windowUpdate()
    
    def windowUpdate(self):
        if config.App == True:
            self.main()
    
    def main(self):
        try:
            button = pygame.Rect(10,10,75,75)
            slider = pygame.Rect(config.slider_x,config.slider_y,config.slider_len,config.slider_height)
            stopButton = pygame.Rect(515,10,75,75)
            
            while self.running: 
                
                self.screen.fill((255,255,255))
                
                pygame.draw.rect(self.screen, (0,255,0), button)
                pygame.draw.rect(self.screen, (0,0,255), slider)
                pygame.draw.rect(self.screen, (255,0,0), stopButton)
                
                self.mouse_pos = pygame.mouse.get_pos()
                move_slider = getattr(self, 'move_slider', False)
                
                if move_slider and config.slider_x <= self.mouse_pos[0] <= config.slider_x+config.slider_len:
                    pygame.draw.circle(self.screen,(0,0,0),(self.mouse_pos[0],config.slider_y+config.slider_height/2),10)
                    self.speed = (self.mouse_pos[0] - (config.slider_x+config.slider_len/2))/2
                    self.lastMousePos = self.mouse_pos
                else:
                    if getattr(self, 'lastMousePos', None) != None:
                        pygame.draw.circle(self.screen,(0,0,0),(self.lastMousePos[0],config.slider_y+config.slider_height/2),10)
                    else:
                        pygame.draw.circle(self.screen,(0,0,0),(300,config.slider_y+config.slider_height/2),10)
                    self.move_slider = False
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        #print('MOUSE CLICK')
                        if button.collidepoint(event.pos):
                            self.move = True
                            self.speed = 32
                            self.lastMousePos = (config.slider_x+config.slider_len/2+self.speed*2,self.mouse_pos[1])
                        if slider.collidepoint(event.pos):
                            self.move = True
                            self.move_slider = True
                        if stopButton.collidepoint(event.pos):
                            self.move = False
                            self.lastMousePos = None
                    elif event.type == pygame.MOUSEBUTTONUP:
                        #print('MOUSE UP')
                        self.move_slider = False
                        if button.collidepoint(event.pos):
                            self.move = False
                            self.lastMousePos = None

                        
                pygame.display.flip()
                self.clock.tick(127)
        except KeyboardInterrupt:
            self.running = False
            pygame.quit()
