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

def drawScene(screen, button, manX, manY, scale):
    screen.blit(backgroundPic, Rect(0,0,width,height))    #draw the picture
    
    #scaling the picture
    scaleWidth = int(charPic.get_width()*scale)
    scaleHeight = int(charPic.get_height()*scale)
    #transform from the original
    newCharPic = transform.scale(charPic, (scaleWidth, scaleHeight))
    #blit the scaled picture
    screen.blit(newCharPic, (manX, manY))
    #generates a hit box for later use
    charBox = Rect(manX, manY, newCharPic.get_width(), newCharPic.get_height())
    draw.rect(screen, RED, charBox, 1) #draws hit box around the rectangle
    display.flip()

running = True
myClock = time.Clock()
manX = 0
manY = 300
scale = 1
# Game Loop
while running:
    for e in event.get():             # checks all events that happen
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            mx, my = e.pos          
            button = e.button
                    
    drawScene(screen, button, manX, manY, scale)
    myClock.tick(60)                     # waits long enough to have 60 fps
    #position of Michellin Man
    manX += 1 
    manY -= 1
    scale += .01
    if manX > width:
        running = False
quit()
