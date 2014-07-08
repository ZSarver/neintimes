#Player.py - A class for the player

import pygame
from vector import *
from pygame.sprite import *
from localsprite import *
from math import *
from weaponry import *
import pprint
import random

rotationSpeed = 0.05
thrust = 0.5
baseSpeed = 6
boostThrust = 4
boostSpeed = 16

class PlayerGroup(LocalGroup):
    def __init__(self):
        Group.__init__(self)
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
        self.shotgroup.update()



class Player(LocalSprite):

    def __init__(self, weap, image):
        Sprite.__init__(self)
        self.image = image
        self.originalimage = image
        self.aim = 0
        self.position = Vector2D(0,0)
        self.momentum = Vector2D(0,0)
        self.rect = image.get_rect()
        if weap == None:
            self.weapon = weapon.testweapon()
    
    def update(self, relThrustVector, boost, rotationDir, shooting):
        self.weapon.cool()
        if shooting:
            self.shoot()
        #for rotation,
        #  right = 1
        #  left = -1
        self.aim += rotationSpeed * rotationDir
        self.image = pygame.transform.flip(pygame.transform.rotate(self.originalimage,degrees(float(self.aim))),False,True)
        if boost is True:
            t = boostThrust
            maxSpeed = boostSpeed
        else:
            t = thrust
            maxSpeed = baseSpeed
        thrustVector = relThrustVector.rotate(self.aim).mult(t)
        self.propel(thrustVector, maxSpeed)
        self.position += self.momentum

    def propel(self, vector, maxSpeed):
        self.momentum = (self.momentum + vector).crop(maxSpeed)

    def shoot(self):
        g = self.groups()[0].shotgroup
        self.weapon.fire(self.position, self.aim, self.momentum, g)
