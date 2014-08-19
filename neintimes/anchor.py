#anchor.py

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

class Anchor(LocalSprite):

    def __init__(self, image):
        Sprite.__init__(self)
        self.image = image
        self.originalimage = image
        self.aim = 0
        self.position = Vector2D(0,0)
        self.momentum = Vector2D(0,0)
        self.rect = image.get_rect()
        self.squad = None
        self.shooting = False
    def setSquad(self, squad):
        self.squad = squad
    def playerInput(self, relThrustVector, boost, rotationDir, shooting):
        self.shooting = shooting
        self.aim += rotationSpeed * rotationDir 
        self.image = pygame.transform.flip(pygame.transform.rotate(self.originalimage,degrees(float(self.aim))),False,True)
        self.rect = self.image.get_rect()
        thrustVector = relThrustVector.rotate(self.aim).mult(thrust)
        self.propel(thrustVector, baseSpeed)

    def update(self):  
        self.position += self.momentum
        
    def propel(self, vector, maxSpeed):
        self.momentum = (self.momentum + vector).crop_ip(maxSpeed)

