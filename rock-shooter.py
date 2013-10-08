import time
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((400, 300))

counter = 1
secondsPerFrame = 1.0 / 30
done = False
x = 0
y = 0
vx = 0
vy = 0
g = 1
onGround = False

while not done:
    delayTime = time.clock()
    
    #handle input
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_SPACE and onGround:
            vy = -10
            onGround = False
    
    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[K_UP]:
        y -= 1
    if pressedKeys[K_DOWN]:
        y += 1
    if pressedKeys[K_LEFT]:
        x -= 1
    if pressedKeys[K_RIGHT]:
        x += 1
    if pressedKeys[K_ESCAPE]:
        done = True
    
    #compute physics
    vy += g
    
    y += vy
    x += vx
    
    if y > 250:
        y = 250
        vy = 0
        onGround = True
    
    #draw things
    screen.fill((0,0,0))

    pygame.draw.circle(screen, (255, 0, 0), (x , y), 10)
    
    pygame.display.flip()
    
    counter += 1
    time.sleep(secondsPerFrame - (time.clock() - delayTime))