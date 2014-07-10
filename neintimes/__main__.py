
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
    pgroup = player.PlayerGroup()
    #sprite groups must be added to the screen to be drawn
    screen.add(pgroup)
    print "Creating clock..."
    clock = pygame.time.Clock()
    clock.tick()
    image = loadsurface("small2.png")
    playerboid = player.Player(None, image)
    boid1 = Boid(Vector2D(0,0), image)
    boid2 = Boid(Vector2D(0,0), image)
    pgroup.add(playerboid)
    pgroup.add(boid1)
    pgroup.add(boid2)
    print "Entering main loop..."
    while True:
        #deal with eventlist
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()
        (thrustDirection, boost, rotation, shooting)  = getInputActions()
        playerboid.update(thrustDirection, boost, rotation, shooting)

        time = clock.tick(60) #tick! limit to 60 fps

        pgroup.update()
        screen.update(playerboid.position)
        pygame.event.pump()

main()
