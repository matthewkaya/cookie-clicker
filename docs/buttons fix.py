import sys,os
from pygame import * 
import pygame
import math
pygame.init()
#loads font from a file
font = pygame.font.SysFont('', 40)
#variables for colours and screens
gamerun=True
StartMenuScreen=True
myClock = time.Clock()
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BGGREY=(150,150,150)
LIGHTGREY=(220,220,220)
SIZE = (800, 600)
click=LIGHTGREY
screen = pygame.display.set_mode(SIZE)
#function to find disance between two points
def dist(x1,y1,x2,y2):
    return(math.sqrt((x1-x2)**2+(y1-y2)**2))

#displays the start menu
def startMenu():
    pygame.draw.rect(screen,RED,(0,0,800,600))
    pygame.draw.rect(screen,BLACK,(290,190,220,70))
    pygame.draw.rect(screen,GREEN,(300,200,200,50))
    text_surface = font.render('START!', True, BLACK)# font.render(text,anti aliasing,colour)
    screen.blit(text_surface, dest=(330,200))#draws the rendered text at a location
    pygame.draw.rect(screen,BLACK,(290,290,220,70))
    pygame.draw.rect(screen,GREEN,(300,300,200,50))
    text_surface = font.render('QUIT', True, BLACK)
    screen.blit(text_surface, dest=(330,300))    
    pygame.display.update()
#displays the game screen  
def game():
    pygame.draw.rect(screen,BGGREY,(0,0,800,600))
    pygame.draw.rect(screen,LIGHTGREY,(100,100,600,400))
    pygame.draw.circle(screen,GREEN,(220,400),50)
    pygame.draw.circle(screen,RED,(330,400),50)
    pygame.draw.circle(screen,BLUE,(440,400),50)
    pygame.draw.circle(screen,YELLOW,(550,400),50)
    pygame.draw.circle(screen,BLACK,(385,200),60,10)
    pygame.draw.circle(screen,click,(385,200),50) 
    pygame.display.update()
    
#the game loop    
while gamerun==True:
    if StartMenuScreen==True:
        startMenu()#runs our start menu function
        #print(pygame.event.get())
        for event in pygame.event.get():#finds events
            if event.type==MOUSEBUTTONDOWN:#checks if the event was a mouse press
                mx, my = event.pos#grabs the position of the mouse when pressed
                print(mx,my)
                if mx>=290 and mx<=510 and my>=190 and my<=260:#checks if the position is on our start button
                    gameScreen=True#starts the game screen
                    StartMenuScreen=False#ends the menu screen
                if mx>=290 and mx<=510 and my>=290 and my<=360:#checks if the position of the mouse is on our quit button
                    pygame.quit()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    elif gameScreen==True:
        game()#runs our game function
        for event in pygame.event.get():#finds events
            if event.type==MOUSEBUTTONDOWN:#checks if the event was a mouse press
                mx, my = event.pos
                if (dist(mx,my,220,400)<50):#uses the distance function to test if the mouse was pressed over the circle
                    click=GREEN#changes the circle to the correct colour
                elif (dist(mx,my,330,400)<50):
                    click=RED
                elif (dist(mx,my,440,400)<50):
                    click=BLUE
                elif (dist(mx,my,550,400)<50):
                    click=YELLOW
            if event.type == QUIT:
                pygame.quit()
                sys.exit()            
    myClock.tick(60)

pygame.quit()
