#05/02/2026
import pygame
from config import Config
config = Config()
from text_labels import Label

class Window():
    def __init__(self):
        self.running = True
        self.move = False
        self.lastMotorPos = 300
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
            squareSide = 75
            margin = 10
            #stop label
            Label(self.screen,config.labelForStop,600-squareSide+0.2*margin,3*margin)
            Label(self.screen,config.labelForCruise,margin,3*margin)
            # MAKE THE COMMANDS ON PYGAME'S WINDOW
            # here lies the all-mighty button for 32 / 256 throttle
            button = pygame.Rect(margin,margin,squareSide,squareSide)
            #slider to set motor's speed
            slider_motor_speed = pygame.Rect(config.slider_x,config.slider_y,config.slider_len,config.slider_height)
            #slider to set servo's angle
            slider_servo_1 = pygame.Rect(config.slider_x,config.slider_servo_y,config.slider_len,config.slider_height)
            #DEFCON 1
            stopButton = pygame.Rect(600-squareSide-margin,margin,squareSide,squareSide)
            
            while self.running: 
                
                self.screen.fill((config.WHITE))
                #DRAW COMMANDS
                pygame.draw.rect(self.screen, (config.GREEN), button)
                pygame.draw.rect(self.screen, (config.BLUE), slider_motor_speed)
                pygame.draw.rect(self.screen, (config.BLUE), slider_servo_1)
                pygame.draw.rect(self.screen, (config.RED), stopButton)
                Label.show_labels()
                #GET THE POSITION FOR THE SLIDER MARKER
                self.mouse_pos = pygame.mouse.get_pos()
                move_motor_slider = getattr(self, 'move_motor_slider', False)
                move_servo_slider = getattr(self, 'move_servo_slider', False)
                
                #IF THE SLIDERMARK IS ABLE TO MOVE AND IS INSIDE ITS RECTANGLE
                if move_motor_slider and config.slider_x <= self.mouse_pos[0] <= config.slider_x+config.slider_len:
                    #draw this slider updating
                    pygame.draw.circle(self.screen,(config.BLACK),(self.mouse_pos[0],config.slider_y+config.slider_height/2),10)
                    self.speed = (self.mouse_pos[0] - (config.slider_x+config.slider_len/2))/2
                    self.lastMotorPos = self.mouse_pos
                    #draw the last known other sliders
                    last_servo = getattr(self,'lastServoPos',(300,0))
                    pygame.draw.circle(self.screen,(config.BLACK),(last_servo[0],config.slider_servo_y+config.slider_height/2),10)
                    
                elif move_servo_slider and config.slider_x <= self.mouse_pos[0] <= config.slider_x+config.slider_len:
                    #draw this slider updating
                    pygame.draw.circle(self.screen,(config.BLACK),(self.mouse_pos[0],config.slider_servo_y+config.slider_height/2),10)
                    self.servo_angle = (self.mouse_pos[0] - (config.slider_x+config.slider_len/2))/2
                    self.lastServoPos = self.mouse_pos
                    #draw the last known other sliders
                    last_motor = getattr(self,'lastMotorPos',(300,0))
                    pygame.draw.circle(self.screen,(config.BLACK),(last_motor[0],config.slider_y+config.slider_height/2),10)
                    
                else:#IF MOUSE IS NOT IN SLIDER MARK POSITION
                    if getattr(self, 'lastMotorPos', None) != None:
                        pygame.draw.circle(self.screen,(config.BLACK),(self.lastMotorPos[0],config.slider_y+config.slider_height/2),10)
                        self.move_motor_slider = False
                    else:#IF SHOULDNT MOVE MOTOR SLIDER
                        pygame.draw.circle(self.screen,(config.BLACK),(300,config.slider_y+config.slider_height/2),10)
                        self.speed = 0
                        
                    if getattr(self, 'lastServoPos', None) != None:
                        pygame.draw.circle(self.screen,(config.BLACK),(self.lastServoPos[0],config.slider_servo_y+config.slider_height/2),10)
                        self.move_servo_slider = False
                    else:#IF SHOULDNT MOVE SERVO SLIDER
                        pygame.draw.circle(self.screen,(config.BLACK),(300,config.slider_servo_y+config.slider_height/2),10)
                        self.servo_angle = 0
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        #print('MOUSE CLICK')
                        if button.collidepoint(event.pos):#FIRST BUTTON LOGIC
                            self.move = True
                            self.speed = 31
                            self.lastMousePos = (config.slider_x+config.slider_len/2+self.speed*2,self.mouse_pos[1])
                        if slider_motor_speed.collidepoint(event.pos):#MOTOR SPEED SLIDER LOGIC
                            self.move = True
                            self.motor_move = True
                            self.move_motor_slider = True
                        if slider_servo_1.collidepoint(event.pos):
                            self.move = True
                            self.servo_move = True
                            self.move_servo_slider = True
                        if stopButton.collidepoint(event.pos):#DEFCON 1 ACTIVATION
                            #print('stop')
                            self.move_motor_slider = False
                            self.move_servo_slider = False
                            self.lastMotorPos = (300,0)
                            self.lastServoPos = (300,0)
                            self.lastMousePos = None
                            self.speed = 0
                            self.servo_angle = 0
                    elif event.type == pygame.MOUSEBUTTONUP:
                        #print('MOUSE UP')
                        #STOP SLIDERS IF MOUSE UP
                        self.move_servo_slider = False
                        self.move_motor_slider = False
                        if button.collidepoint(event.pos):
                            self.move = False

                        
                pygame.display.flip()
                self.clock.tick(127)
        except KeyboardInterrupt:
            self.running = False
            pygame.quit()
