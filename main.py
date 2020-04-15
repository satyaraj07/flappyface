import sys, pygame
import pygame.locals
import math
from random import randint
from time import sleep
pygame.init()

def setdefault() :
    player.x = 200
    player.y = 250
    player.ychange = 0
    global start
    start = False
    global runs
    runs = 0
    global pipes
    pipes = []
    global dead
    dead = False
    global score
    score = 0
    global running
    running = True
gravity = 1
#window size
size = width, height = 800, 600
#background colour rgb
white = 255, 255, 255
#background image
background = pygame.image.load('Background2.png')
#setting background
screen = pygame.display.set_mode(size)
#setting title and icon
pygame.display.set_caption("flapping face")
icon_surf = pygame.image.load('icon.png')
icon = pygame.display.set_icon(icon_surf)
#image of face
playerimg = pygame.image.load('p3-removebg-preview.png')
#image of pipe
pipe = pygame.image.load('birduppipe.png')
#ground image
groundimg = pygame.image.load('birdupground.png')
font = pygame.font.SysFont('Comic Sans MS', 30)
class player:
    x = 200
    y = 250
    ychange = 0
    def update() :
        if start :
            if player.y < 440 :
                player.y += player.ychange
                player.ychange += gravity
            else :
                player.y = 440
                die()
            if player.y < 0 :
                player.y = 0
                player.ychange = 0
        else :
            player.y = 250 + int(math.sin(runs/10)*30)
        player.getAngle()

    def jump() :
        player.ychange = -10

    def getAngle() :
        global birdup
        #image rotates after pressing space
        birdup = pygame.transform.rotate(playerimg, -3*player.ychange)
class Pipe() :
    def __init__(self, dir, x, len) :
        self.dir = dir
        self.x = x
        self.len = len

    def update(self) :
        if self.dir == "UP" :
            screen.blit(pipe, (self.x, 600-self.len))
        else :
            screen.blit(pygame.transform.rotate(pipe, 180), (self.x, self.len-431))
        if not dead :
            self.x -= 10

    def collide(self) :
        if self.dir == "DOWN" :
            if player.x + 43 > self.x and self.x + 70 > player.x :
                if player.y < self.len :
                    die()
        else :
            if player.x + 43 > self.x and self.x + 70 > player.x :
                if player.y + 40 > 600-self.len :
                    die()

def pipePair() :
    r = randint(75, 350)
    pipes.append(Pipe("DOWN", 900, r))
    pipes.append(Pipe("UP", 900, 600-(r+125)))
    global score
    score += 1

def ground():
    screen.blit(groundimg, ((runs%111)*-7, 500))
def die() :
    global dead
    dead = True
    running = False

#game loop

setdefault()
while running:
    pygame.time.delay(5)
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE :
                if not start :
                    start = True
                if not dead:
                    player.jump()

    if runs % 45 == 0 and start :
        pipePair()
    for p in pipes :
        p.update()
        p.collide()
    player.update()
    screen.blit(birdup, (player.x,player.y))
    ground()
    scoreboard = font.render(str(score-2), False, (0, 0, 0))
    if score > 2 :
        scorebase = pygame.draw.rect(screen, (255, 255, 255), (7, 5, len(str(score-2))*15+10, 35))
        screen.blit(scoreboard, (10, 0))
    pygame.display.update()
    if not dead :
        runs += 1
pygame.quit()
