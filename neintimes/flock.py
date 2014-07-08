#flock.py - implements a flock of boids

import pygame
from data import *
from vector import *
from pygame.sprite import *
from localsprite import *
import pprint

class Flock(LocalGroup):
    def __init__(self, accelConst=1.2, seperation=30.0):
        Group.__init__(self)
        self.centerOfMass = None
        self.momentum = None
        self.targetLocation = None
        self.accelConst = accelConst
        self.seperation = seperation
        self.shotgroup = LocalGroup()

    def draw(self, screen):
        self.shotgroup.draw(screen)
        Group.draw(self, screen)

    def place(self, offset=Vector2D(0,0)):
        self.shotgroup.place(offset)
        LocalGroup.place(self, offset)

    def clear(self, screen, background):
        self.shotgroup.clear(screen, background)
        Group.clear(self, screen, background)

    def update(self):
        """Updates, calculating everything each individual boid needs
        to know to flock effectively."""
        self.shotgroup.update()
        weightlist = [ship.weight for ship in self.sprites()]
        positionlist = [ship.position for ship in self.sprites()]
        accum = Vector2D(0,0)
        for i in range(len(positionlist)):
            accum = accum + scalarmult(positionlist[i], weightlist[i])
        self.centerOfMass = scalarmult(accum, 1.0/float(sum(weightlist)))
        momentumlist = [ship.momentum for ship in self.sprites()]
        haccum = Vector2D(0,0)
        for i in momentumlist:
            haccum = haccum + i
        self.momentum = scalarmult(haccum,1.0/float(len(momentumlist)))

        self.targetLocation = self.centerOfMass + scalarmult(self.momentum,self.accelConst)
        Group.update(self, self.targetLocation, self.sprites(), self.seperation)
