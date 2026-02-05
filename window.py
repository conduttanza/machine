import pygame
from threading import Thread
from config import Config
config = Config()

class Window():
    def __init__(self):
        self.running = True
        self.move = False
        pygame.init()
        pygame.display.set_caption('motor movement')
        self.screen = pygame.display.set_mode((600,600))
        self.clock = pygame.time.Clock()
        self.windowUpdate()
    
    def windowUpdate(self):
        if config.App == True:
            Thread(target=self.main, daemon=True).start()
    
    def main(self):
        try:
            button = pygame.Rect(150,100,100,150)
            
            while self.running: 
                self.screen.fill((255,255,255))
                pygame.draw.rect(self.screen, (0,255,0), button)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if button.collidepoint(event.pos):
                            self.move = True
                pygame.display.flip()
                self.clock.tick(60)
        except KeyboardInterrupt:
            self.running = False
            pygame.quit()
