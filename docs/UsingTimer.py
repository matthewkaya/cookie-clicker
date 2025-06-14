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

myFont = font.SysFont("Times New Roman",30)

def drawScene(screen, button):
    global missiley, hasShot, shotTimer
    draw.rect(screen, BLUE, (0, 0, width, height))
    #create turret
    draw.rect(screen, GREEN, (450, 650, 100, 50))
    draw.rect(screen, BLACK, (498, 600, 5, 50))
    if hasShot == True:
        draw.circle(screen, RED, (500, missiley), 3)
        missiley -= 5
        if missiley < 0:
            missiley = 600
            hasShot = False
            shotTimer = time.get_ticks() # time of last shot
    else:
        if time.get_ticks() - shotTimer >= 1000: #how often I want to shoot
            hasShot = True
    display.flip()

running = True
myClock = time.Clock()
missiley = 600  # position of the missile
shotTimer = time.get_ticks() # time of last shot
hasShot = True  # is the missile out there
# Game Loop
while running:
    for e in event.get():             # checks all events that happen
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            mx, my = e.pos          
            button = e.button
                    
    drawScene(screen, button)
    myClock.tick(60)                     # waits long enough to have 60 fps
    
quit()
