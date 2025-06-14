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
    global missileList, shotTimer
    draw.rect(screen, BLUE, (0, 0, width, height))
    #create turret
    draw.rect(screen, GREEN, (450, 650, 100, 50))
    draw.rect(screen, BLACK, (498, 600, 5, 50))
    
    for i in range (len(missileList)-1, -1, -1): # get each missile
        missiley = missileList[i]    
        draw.circle(screen, RED, (500, missiley), 3)  #draw the missile
        missileList[i] -= 5 # move missile down 5
        
        if missileList[i] < 0: # if off screen
            del missileList[i] # delete current missile
        
    if time.get_ticks() - shotTimer >= 100: # 1 second difference
        missileList.append(600) # add new missile
        shotTimer = time.get_ticks() # reset timer
   
    display.flip()

running = True
myClock = time.Clock()
shotTimer = time.get_ticks() # time of last shot
missileList = [600] # a list for missiles currently on the screen (y - values)
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
    print(missileList)
quit()
