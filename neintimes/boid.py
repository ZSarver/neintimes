 #boid.py - implements the individual agents of a flock

import pygame
from vector import *
from pygame.sprite import *
from localsprite import *
from math import *
from weaponry import *
import pprint
import random


class Boid(LocalSprite):
    def __init__(self, position, image, aim=0, weight=1, thrust=3, maxSpeed=6, rotationspeed=0.02, weap=None):
        """Creates a new Boid

        aim - a Vector2D of the boid's initial aim
        weight - the boid's weight
        image - a Surface representing the Boid
        rect - the rect representing the hitbox and position of the boid"""
        Sprite.__init__(self)
        self.image = image
        self.originalimage = image
        self.rect = image.get_rect()
        self.position = position
        self.aim = aim
        self.momentum = Vector2D(0,0)
        self.weight = weight
        self.thrust = thrust
        self.iscontrolled = False
        self.maxSpeed = maxSpeed
        self.rotationspeed = rotationspeed
        if weap == None:
            self.weapon = weapon.testweapon()
        else:
            self.weapon = weap
    def update(self, targetLocation, targetAim, targetMomentum):
        self.weapon.cool
        #~ if not self.iscontrolled:
            #~ #deal with seperation
            #~ acc = Vector2D(0,0)
            #~ for i in list(flockmates):
                #~ d = distance(self.position, i.position)
                #~ if d > 0.0001:
                    #~ c = (seperation * i.weight) / d
                    #~ acc += scalarmult(self.position - i.position, c)
        #head toward target location
        d = distance(targetLocation, self.position)
        t = 30
        goal = targetLocation - self.position 
        timeestimate = sqrt(d/max(self.momentum.magnitude,self.maxSpeed/2))
        goal += (targetMomentum - self.momentum).mult(timeestimate)
        def easeMomentum(targetMomentum, c):
            goalmomentum = self.momentum.mult(1-c) + targetMomentum.mult(c)
            diff = goalmomentum - self.momentum
            diff.crop(self.thrust)
            self.propel(diff)
        easeMomentum(goal, 0.2)
        if d > t:
            goalaimvector = goal.unit
            self.aim = goalaimvector.direction
        else:
            self.aim = targetAim
        #update image based on new aim
        self.image = pygame.transform.flip(pygame.transform.rotate(self.originalimage,degrees(float(self.aim))),False,True)
        self.position += self.momentum

    def propel(self, vector):
        self.momentum = (self.momentum + vector).crop(self.maxSpeed)

    def shoot(self):
        g = self.groups()[0].shotgroup
        self.weapon.fire(self.position, self.aim, self.momentum, g)

    def __getattr__(self, name):
        """Returns a Vector2D of the ship's position."""
        raise AttributeError("Boid has no attribute " + name)
