 #boid.py - implements the individual agents of a flock

import pygame
from vector import *
from pygame.sprite import *
from localsprite import *
from math import *
from weaponry import *
from weaponry.weapons import *
import pprint
import random

FORMATION_LOCK_DISTANCE = 10

class Boid(LocalSprite):
    def __init__(self, position, image, aim=0, weight=1, thrust=3, maxSpeed=6, rotationspeed=0.02, weap=None):
        """Creates a new Boid

        aim - a Vector2D of the boid's initial aim in radians
        weight - the boid's weight
        image - a Surface representing the Boid
        rect - the rect representing the hitbox and position of the boid"""
        Sprite.__init__(self)
        self.image = image
        self.originalimage = image
        self.radius = max(image.get_width()/3, image.get_height()/3)
        print "Radius = " + str(self.radius)
        self.rect = image.get_rect()
        self.position = position
        self.aim = aim
        self.momentum = Vector2D(0,0)
        self.weight = weight
        self.thrust = thrust
        self.iscontrolled = False #deprecate
        self.islocked = False
        self.maxSpeed = maxSpeed
        self.rotationspeed = rotationspeed
        self.statusEffects=[]
        if weap == None:
            self.weapon = weapons.testweapon()
        else:
            self.weapon = weap
    def addEffect(self,effect):
        self.statusEffects.add(effect)
    def removeEffect(self, index):
        self.statusEffects.pop(index)
    def update(self, targetLocation, targetAim, targetMomentum, shooting):
        for index, effect in enumerate(self.statusEffects):
            effect.update(self, 
                          targetLocation, 
                          targetAim, 
                          targetMomentum, 
                          shooting,
                          effectIndex=index)
        self.weapon.cool()
        d = distance(targetLocation, self.position)
        if d  < FORMATION_LOCK_DISTANCE:
            self.lock()
        else:
            self.unlock()
        def easeMomentum(targetMomentum, c):
            goalmomentum = self.momentum.mult(1-c) + targetMomentum.mult(c)
            diff = goalmomentum - self.momentum
            diff.crop_ip(self.thrust)
            self.propel(diff)
        def easePosition(target, c):
            newpos = self.position.mult(1-c) + target.mult(c)
            self.position = newpos
        if not self.islocked:
            #when not already locked into formation, move toward the assigned position
            goal = targetLocation - self.position 
            timeestimate = sqrt(d/max(self.momentum.magnitude,self.maxSpeed/2))
            goal += (targetMomentum - self.momentum).mult(timeestimate)
            easeMomentum(goal, 0.2)
            if d > (4 * FORMATION_LOCK_DISTANCE):
                #when close to locking into formation, aim in the assigned direction
                goalaimvector = goal.unit
                self.aim = goalaimvector.direction
            else:
                #otherwise aim toward destination
                self.aim = targetAim
        if self.islocked:
            self.momentum = targetMomentum
            self.aim = targetAim
            easePosition(targetLocation,0.5)
            if shooting:
                self.shoot()
        #update image based on new aim
        self.image = pygame.transform.flip(pygame.transform.rotate(self.originalimage,degrees(float(self.aim))),False,True)
        self.rect = self.image.get_rect()
        self.position += self.momentum
    def lock(self):
        self.islocked = True
    def unlock(self):
        self.islocked = False
    def propel(self, vector):
        self.momentum = (self.momentum + vector).crop_ip(self.maxSpeed)

    def shoot(self):
        g = self.groups()[0].shotgroup
        self.weapon.fire(self.position, self.aim, self.momentum, g)
        
    def killshot(self):
        self.kill()

    def __getattr__(self, name):
        """Returns a Vector2D of the ship's position."""
        raise AttributeError("Boid has no attribute " + name)
