#05/02/2026
import math
import pygame
from config import Config
config = Config()
from text_labels import Label

class Window():
    def __init__(self):
        self.pi = math.pi
        self.running = True
        self.move = False
        self.move_motor_slider = False
        self.move_servo_1_slider = False
        self.move_servo_2_slider = False
        self.lastMotorPos = (300,0)
        self.lastServoPos_1 = (300,0)
        self.lastServoPos_2 = (300,0)
        self.lastLineMovPos = (300,0)
        self.lastMousePos = None
        self.speed = 0
        self.servo_1_angle = 0
        self.servo_2_angle = 0
        self.line_pos = 0
        self.squareSide = config.squareSide
        self.margin = config.margin
        pygame.init()
        pygame.display.set_caption('motor movement')
        self.screen = pygame.display.set_mode((config.screenSide,config.screenSide))
        self.clock = pygame.time.Clock()
        #self.windowUpdate()
    
    def windowUpdate(self):
        if config.App == True:
            self.main()
        
    def main(self):
        try:
            #BEFORE LOOP / constants
            self.labels()
            self.shapes()
            while self.running: 
                self.screen.fill((config.WHITE))
                #DRAW COMMANDS
                self.draw()
                Label.show_labels()
                #GET THE POSITION FOR THE SLIDER MARKER
                self.mouse_pos = pygame.mouse.get_pos()
                self.move_motor_slider = getattr(self, 'move_motor_slider', False)
                self.move_servo_1_slider = getattr(self, 'move_servo_1_slider', False)
                self.move_servo_2_slider = getattr(self, 'move_servo_2_slider', False)
                self.move_line_slider = getattr(self, 'move_line_slider', False)
                
                #IF THE SLIDERMARK IS ABLE TO MOVE AND IS INSIDE ITS RECTANGLE
                self.last_motor = getattr(self,'lastMotorPos',(300, 0))
                self.last_servo_1 = getattr(self,'lastServoPos_1',(300, 0))
                self.last_servo_2 = getattr(self,'lastServoPos_2',(300, 0))
                self.last_line_movement = getattr(self,'lastLineMovPos',(300, 0))
                
                
                if self.move_motor_slider and config.slider_x <= self.mouse_pos[0] <= config.slider_x+config.slider_len:
                    #draw this slider updating
                    self.drawMotorSliderPoint()
                    #draw the last known other sliders
                    self.drawLastSliderServo1()
                    self.drawLastSliderServo2()
                    self.drawLastLineMovPos()
                    #change vars
                    self.speed = (self.mouse_pos[0] - (config.slider_x+config.slider_len/2))/2
                    self.lastMotorPos = self.mouse_pos
                    
                elif self.move_servo_1_slider and config.slider_x <= self.mouse_pos[0] <= config.slider_x+config.slider_len:
                    #draw this slider updating
                    self.drawServo1SliderPoint()
                    #draw the last known other sliders
                    self.drawLastSliderMotor()
                    self.drawLastSliderServo2()
                    self.drawLastLineMovPos()
                    #change vars
                    self.servo_1_angle = (self.mouse_pos[0] - (config.slider_x+config.slider_len/2))/2
                    self.lastServoPos_1 = self.mouse_pos
                    
                elif self.move_servo_2_slider and config.slider_x <= self.mouse_pos[0] <= config.slider_x+config.slider_len:
                    #draw this slider updating
                    self.drawServo2SliderPoint()
                    #draw the last known other sliders
                    self.drawLastSliderMotor()
                    self.drawLastSliderServo1()
                    self.drawLastLineMovPos()
                    #change vars
                    self.servo_2_angle = (self.mouse_pos[0] - (config.slider_x+config.slider_len/2))/2
                    self.lastServoPos_2 = self.mouse_pos
                
                elif self.move_line_slider and config.slider_x <= self.mouse_pos[0] <= config.slider_x+config.slider_len:
                    #draw this slider updating
                    self.drawLineMovementPoint()
                    #draw the last known other sliders
                    self.drawLastSliderMotor()
                    self.drawLastSliderServo1()
                    self.drawLastSliderServo2()
                    #change vars
                    self.findLineAngle()
                    self.line_pos = (self.mouse_pos[0] - (config.slider_x+config.slider_len/2))/2
                    self.lastLineMovPos = self.mouse_pos
                    
                #MOTOR
                else:#IF MOUSE IS NOT IN SLIDER MARK POSITION
                    if getattr(self, 'lastMotorPos', None) != None:
                        self.drawLastSliderMotor()
                        self.move_motor_slider = False
                    else:#IF SHOULDNT MOVE MOTOR SLIDER
                        pygame.draw.circle(
                            self.screen,(config.BLACK),
                            (config.screenSide/2,config.slider_y+config.slider_height/2),
                            10
                        )
                        self.speed = 0
                #SERVO 1    
                    if getattr(self, 'lastServoPos_1', None) != None:
                        self.drawLastSliderServo1()
                        self.move_servo_1_slider = False
                    else:#IF SHOULDNT MOVE SERVO 1 SLIDER
                        pygame.draw.circle(
                            self.screen,
                            (config.BLACK),
                            (config.screenSide/2,config.slider_servo_y+config.slider_height/2),
                            10
                        )
                        self.servo_1_angle = 0
                #SERVO 2
                    if getattr(self, 'lastServoPos_2', None) != None:
                        self.drawLastSliderServo2()
                        self.move_servo_2_slider = False
                    else:#IF SHOULDNT MOVE SERVO 2 SLIDER
                        pygame.draw.circle(
                                self.screen,
                                (config.BLACK),
                                (config.screenSide/2,config.slider_servo_y+config.slider_height+self.margin+config.slider_height/2),
                                10
                            )
                        self.servo_2_angle = 0
                
                #LINE MOVEMENT
                    if getattr(self, 'lastLineMovPos', None) != None:
                        self.drawLastLineMovPos()
                        self.move_line_slider = False
                    else:#IF SHOULDNT MOVE LINE SLIDER
                        pygame.draw.circle(
                                self.screen,
                                (config.BLACK),
                                (config.screenSide/2,config.slider_servo_y+2*(config.slider_height+self.margin)),
                                10
                            )
                        self.line_pos = 0
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouseDown(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouseUp(event)
                        
                pygame.display.flip()
                self.clock.tick(60)
        except KeyboardInterrupt:
            self.running = False
            pygame.quit()
    
    def labels(self):
        Label(self.screen,config.labelForStop,600-self.squareSide+0.2*self.margin,3*self.margin)
        Label(self.screen,config.labelForCruise,self.margin,3*self.margin)
    
    def shapes(self):
        # here lies the all-mighty button for 32 / 256 throttle
        self.button = pygame.Rect(self.margin,self.margin,self.squareSide,self.squareSide)
        #slider to set motor's speed
        self.slider_motor_speed = pygame.Rect(config.slider_x,config.slider_y,config.slider_len,config.slider_height)
        #slider to set servo's angle
        self.slider_servo_1 = pygame.Rect(
                config.slider_x,
                config.slider_servo_y,
                config.slider_len,
                config.slider_height)
        self.slider_servo_2 = pygame.Rect(
                config.slider_x,
                config.slider_servo_y+config.slider_height+self.margin,
                config.slider_len,
                config.slider_height
            )
            #DEFCON 1
        self.stopButton = pygame.Rect(600-self.squareSide-self.margin,self.margin,self.squareSide,self.squareSide)
        #LINE MOV
        self.line_movement = pygame.Rect(
                config.slider_x,
                config.slider_servo_y+2*(config.slider_height+self.margin), 
                config.slider_len, 
                config.slider_height
            )
    
    def draw(self):
        pygame.draw.rect(self.screen, (config.GREEN), self.button)
        pygame.draw.rect(self.screen, (config.RED), self.stopButton)
                
        pygame.draw.rect(self.screen, (config.BLUE), self.slider_motor_speed)
                
        pygame.draw.rect(self.screen, (config.BLUE), self.slider_servo_1)
        pygame.draw.rect(self.screen, (config.BLUE), self.slider_servo_2)
        
        pygame.draw.rect(self.screen, config.BLACK, self.line_movement)
    
    def drawMotorSliderPoint(self):
        pygame.draw.circle(
            self.screen,
            (config.BLACK),
            (self.mouse_pos[0],
            config.slider_y+config.slider_height/2),
            10
        )
    
    def drawServo1SliderPoint(self):
        pygame.draw.circle(
            self.screen,
            (config.BLACK),
            (self.mouse_pos[0],config.slider_servo_y+config.slider_height/2),
            10
        )
    
    def drawServo2SliderPoint(self):
        pygame.draw.circle(
            self.screen,
            (config.BLACK),
            (self.mouse_pos[0],
            config.slider_servo_y+config.slider_height+self.margin+config.slider_height/2),
            10
            )

    def drawLineMovementPoint(self):
        pygame.draw.circle(
                self.screen,
                (config.WHITE),
                (self.mouse_pos[0],
                config.slider_servo_y+2*(config.slider_height+self.margin)+config.slider_height/2),
                10
            )
        
    def drawLastSliderServo1(self):
        pygame.draw.circle(
                self.screen,
                (config.BLACK),
                (self.last_servo_1[0],config.slider_servo_y+config.slider_height/2),
                10
            )
    
    def drawLastSliderServo2(self):
        pygame.draw.circle(
                self.screen,
                (config.BLACK),
                (self.last_servo_2[0],
                config.slider_servo_y+config.slider_height+self.margin+config.slider_height/2),
                10
            )
        
    def drawLastLineMovPos(self):
        pygame.draw.circle(
                self.screen,
                (config.WHITE),
                (self.lastLineMovPos[0],
                config.slider_servo_y+2*(config.slider_height+self.margin)+config.slider_height/2),
                10
            )
        
    def drawLastSliderMotor(self):
        pygame.draw.circle(
            self.screen,
            (config.BLACK),
            (self.last_motor[0],config.slider_y+config.slider_height/2),
            10
        )
    
    def mouseDown(self, event):
        #print('MOUSE CLICK')
        if self.button.collidepoint(event.pos):#CRUISE BUTTON LOGIC
            self.motor_move = True
            self.speed = 31
            self.lastMotorPos= (config.slider_x+config.slider_len/2+self.speed*2,self.mouse_pos[1])
            self.move_motor_slider = True
        
        #MOTOR SPEED SLIDER LOGIC
        if self.slider_motor_speed.collidepoint(event.pos):
            self.move = True
            self.motor_move = True
            self.move_motor_slider = True
            
        if self.slider_servo_1.collidepoint(event.pos):
            self.move = True
            self.servo_1_move = True
            self.move_servo_1_slider = True
            
        if self.slider_servo_2.collidepoint(event.pos):
            self.move = True
            self.servo_2_move = True
            self.move_servo_2_slider = True
        
        if self.line_movement.collidepoint(event.pos):
            self.move = True
            self.last_line_move = True
            self.move_line_slider = True
            #print('line mov collide')
            
        #DEFCON 1 ACTIVATION
        if self.stopButton.collidepoint(event.pos):
            #print('stop')
            self.move_motor_slider = False
            self.move_servo_1_slider = False
            self.move_servo_2_slider = False
            self.lastMotorPos = (300,0)
            self.lastServoPos_1 = (300,0)
            self.lastServoPos_2 = (300,0)
            self.lastLineMovPos = (300,0)
            self.lastMousePos = None
            self.speed = 0
            self.servo_1_angle = 0
            self.servo_2_angle = 0
            self.line_pos = 0
            
    def mouseUp(self, event):
        #print('MOUSE UP')
        #STOP SLIDERS IF MOUSE UP
        self.move_servo_1_slider = False
        self.move_servo_2_slider = False
        self.move_motor_slider = False
        self.move_line_slider = False
        if self.button.collidepoint(event.pos):
            self.move = False

    def findLineAngle(self):
        linePos = round((self.line_pos+112.5)/(2*112.5)*100, 2)
        servo1rad = round(math.acos(linePos/200),2)
        servo2rad = round(math.pi - 2*servo1rad,2)
        servo1deg = round(servo1rad*90/math.pi,1)
        servo2deg = round(servo2rad*90/math.pi,1)
        self.servo_1_angle = round(servo1deg/90*112.5,1)
        self.servo_2_angle = round(servo2deg/90*112.5,1)
        '''
        servo1angle = self.servo_1_angle*(4000/(config.slider_len))+1500
        servo2angle = self.servo_2_angle*(4000/(config.slider_len))+1500
        servo1rad = round(servo1angle/1500*self.pi - self.pi, 3)
        servo2rad = round(servo2angle/1500*self.pi - self.pi, 3)
        '''
        #print(f'servo 1: {servo1rad} rad {servo1deg} deg servo 2: {servo2rad} rad {servo2deg} deg line pos: {linePos}%')
        #print(f'servo 1: {self.servo_1_angle} servo 2: {self.servo_2_angle}')
        
        



