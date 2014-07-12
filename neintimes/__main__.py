
import pygame
from pygame.locals import *
from boid import *
from screen import *
from flock import *
from data import *
from math import *
from weaponry import *
from input import *
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
    p = player.Player(None, image)
    for i in range(3):
        b = Boid(Vector2D(0,0),image)
        fgroup.addSquad(b)
    fgroup.addAnchor(p)

    print "Entering main loop..."
    while True:
        #deal with eventlist
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()
        (thrustDirection, boost, rotation, shooting)  = getInputActions()
        p.playerInput(thrustDirection, boost, rotation, shooting)

        time = clock.tick(60) #tick! limit to 60 fps

        fgroup.update()
        screen.update(p.position) #center camera on player
        pygame.event.pump()

main()
