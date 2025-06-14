# the following code will always put the screen in the top corner
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)

from pygame import * 
init()
size = width, height = 1000, 700
screen = display.set_mode(size)
button = 0
# defining colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# movement key booleans
PRESS_RIGHT = False
PRESS_LEFT = False
PRESS_UP = False
PRESS_DOWN = False

myFont = font.SysFont("Times New Roman",30)
# load image
shipPic = image.load("spaceship.gif")
shipPic = transform.scale(shipPic, (shipPic.get_width()//2, shipPic.get_height()//2))
shipPic = transform.rotate(shipPic, 180)
def drawScene(screen, button, shipx, shipy):
    global missileList, shotTimer
    draw.rect(screen, BLUE, (0, 0, width, height))
    #draw shipPic
    shipRect = Rect(shipx, shipy, shipPic.get_width(), shipPic.get_height())
    screen.blit(shipPic, shipRect)
    rect1 = Rect(shipx + 20, shipy + 80, 6, 20) 
    rect2 = Rect(shipx + 12, shipy + 60, 24, 20)
    rect3 = Rect(shipx, shipy + 40, 46, 20)
    hitList = [rect1, rect2, rect3]
    for hit in hitList:
        draw.rect(screen, RED, hit, 1)
    #create turret
    draw.rect(screen, GREEN, (450, 650, 100, 50))
    draw.rect(screen, BLACK, (498, 600, 5, 50))
    
    # loop is for drawing
    for i in range (len(missileList)-1, -1, -1): # get each missile
        missiley = missileList[i] 
        missileRect = Rect(500, missiley, 3, 5)
        draw.rect(screen, RED, missileRect)  #draw the missile
        missileList[i] -= 5 # move missile down 5
        
        if missileList[i] < 0: # if off screen
            del missileList[i] # delete current missile
    display.flip()
    
    # loop is for collision
    for i in range (len(missileList)-1, -1, -1): # get each missile
        missiley = missileList[i] 
        missileRect = Rect(500, missiley, 3, 5)  
        #print(missileRect.collidelist(hitList))
        if(missileRect.collidelist(hitList) != -1):
            return False
        
    if time.get_ticks() - shotTimer >= 1000: # 1 second difference
        missileList.append(600) # add new missile
        shotTimer = time.get_ticks() # reset timer
   
    
    return True

running = True
myClock = time.Clock()
shotTimer = time.get_ticks() # time of last shot
missileList = [600] # a list for missiles currently on the screen (y - values)
shipX = 0
shipY = 0
moveRate = 5
# Game Loop
while running:
    for e in event.get():             # checks all events that happen
        if e.type == QUIT:
            running = False
        elif e.type == MOUSEBUTTONDOWN:
            mx, my = e.pos          
            button = e.button
        elif e.type == KEYDOWN:
            if e.key == K_RIGHT:
                PRESS_RIGHT = True
            if e.key == K_LEFT:
                PRESS_LEFT = True 
            if e.key == K_UP:
                PRESS_UP = True
            if e.key == K_DOWN:
                PRESS_DOWN = True
        elif e.type == KEYUP:
            if e.key == K_RIGHT:
                PRESS_RIGHT = False
            if e.key == K_LEFT:
                PRESS_LEFT = False 
            if e.key == K_UP:
                PRESS_UP = False
            if e.key == K_DOWN:
                PRESS_DOWN = False   
    if running:
        running = drawScene(screen, button, shipX, shipY)
    myClock.tick(60)                     # waits long enough to have 60 fps
    
    # for ship movement
    if PRESS_RIGHT == True:
        shipX += moveRate
    if PRESS_LEFT == True:
        shipX -= moveRate  
    if PRESS_UP == True:
        shipY -= moveRate
    if PRESS_DOWN == True:
        shipY += moveRate    
quit()
