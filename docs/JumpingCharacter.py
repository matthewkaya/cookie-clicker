# the following code will always put the screen in the top corner
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)
from pygame import * 
init()
size = width, height = 1000, 700
screen = display.set_mode(size)
button = 0
BLACK = (0, 0, 0)
RED = (255, 0, 0)
myFont = font.SysFont("Times New Roman",30)
# loading images
backgroundPic = image.load("gamebackground2.jpg")
charPic = image.load("Michellin Man.png")
# scale the image
backgroundPic = transform.scale(backgroundPic, (width, height))
charPic = transform.scale(charPic, (charPic.get_width()//9, charPic.get_height()//9))

def drawScene(screen, button, manX, manY):
    screen.blit(backgroundPic, Rect(0,0,width,height))    #draw the picture
    
    #blit the scaled picture
    screen.blit(charPic, (manX, manY))
    #generates a hit box for later use
    charBox = Rect(manX, manY, charPic.get_width(), charPic.get_height())
    draw.rect(screen, RED, charBox, 1) #draws hit box around the rectangle
    display.flip()

running = True
myClock = time.Clock()
GROUND = 525 #constant for where the ground is
manX = 0
manY = GROUND
# more constants
PRESS_LEFT = False
PRESS_RIGHT = False
JUMPING = False
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
            if e.key == K_UP and JUMPING == False:
                JUMPING = True
                acceleration = 30 # higher this number is, higher the jump
        elif e.type == KEYUP:
            if e.key == K_RIGHT:
                PRESS_RIGHT = False
            if e.key == K_LEFT:
                PRESS_LEFT = False         
                    
    drawScene(screen, button, manX, manY)
    
    if PRESS_RIGHT == True:
        manX += moveRate
    if PRESS_LEFT == True:
        manX -= moveRate  
    if JUMPING == True:
        manY -= acceleration
        acceleration -= 1
        if manY >= GROUND:
            manY = GROUND
            JUMPING = False
        
    myClock.tick(60)                     # waits long enough to have 60 fps

quit()
