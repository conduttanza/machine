#05/02/2026

class Config():
    screenSide = 725
    #
    servo_1 = 23
    servo_2 = 11
    #servo_3 = 9 #MAGARI NO, gnd
    servo_4 = 10
    #servo_5 = 25 #MAGARI NO, gnd
    #servo_6 = 2 #MAGARI NO, 5v
    labelForStop = 'STOP'
    labelForCruise = 'CRUISE'
    #
    motorRun = False
    servoRun = True
    servo2Run = True
    #
    run = True
    delay = 0.05
    App = True
    #
    squareSide = 75
    margin = 10
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    GREEN = (0,255,0)
    RED = (255,0,0)
    BLUE = (0,0,255)
    slider_len = round(screenSide/1.333,0)
    slider_height = round(screenSide/12,0)
    slider_x = (screenSide-slider_len)/2
    slider_y = round(screenSide/6,0)
    slider_servo_y = round(screenSide/2.4,0)
    
    
    
