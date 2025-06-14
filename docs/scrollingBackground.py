# the following code will always put the screen in the top corner
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)
from pygame import * 
init()
size = width, height = 1000, 700
screen = display.set_mode(size)
button = 0
BLACK = (0, 0, 0)
RED = (255, 255, 255)
myFont = font.SysFont("Times New Roman",30)
# loading images
backgroundPic = image.load("gamebackground2.jpg")
# scale the image
backgroundPic = transform.scale(backgroundPic, (width, height))

def drawScene(screen, button, backx):
    # left side
    screen.blit(backgroundPic, Rect(backx,0,width,height))    #draw the picture
    # right side
    screen.blit(backgroundPic, Rect(backx + width, 0, width, height))
    display.flip()

running = True
myClock = time.Clock()
backgroundX = 0
# Game Loop
while running:
    for e in event.get():             # checks all events that happen
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            mx, my = e.pos          
            button = e.button
                    
    drawScene(screen, button, backgroundX)
    myClock.tick(60)                     # waits long enough to have 60 fps
    backgroundX -= 1
    if backgroundX < -1*width:
        backgroundX = 0
quit()
