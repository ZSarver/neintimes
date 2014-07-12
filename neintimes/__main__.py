
import pygame
from pygame.locals import *
from boid import *
from screen import *
from flock import *
from data import *
from math import *
from weaponry import *
from input import *
from statuseffects import *
import player
import camera
import random

def main():
    """ your app starts here
    """
    random.seed()
    print "Initializing pygame..."
    pygame.init()
    print "Creating screen"

    screen = Screen(640,480,camera.roughTrack(0))    

    #create game objects
    fgroup = Flock(1.2,0.0)
    #sprite groups must be added to the screen to be drawn
    screen.add(fgroup)
    print "Creating clock..."
    clock = pygame.time.Clock()
    clock.tick()
    image = loadsurface("small2.png")
    pimage = loadsurface("anchor.png")
    #~ image = pygame.Surface((15, 15))
    #~ image.fill((0,255,0))
    #~ image.convert()
    p = player.Player(None, pimage)
    for i in range(9):
        b = Boid(Vector2D(0,0),image)
        fgroup.addSquad(b)
    fgroup.addAnchor(p)
    t = testEffect()
    applyEffect(b, None, t)

    print "Entering main loop..."
    while True:
        #deal with eventlist
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()
        (thrustDirection, boost, rotation, shooting)  = getInputActions()
        p.playerInput(thrustDirection, boost, rotation, shooting)

        fgroup.update()
        screen.update(p.position) #center camera on player
        pygame.event.pump()

main()
