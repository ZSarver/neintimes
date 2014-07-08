#shot.py - implements shots

import pygame
from vector import *
from route import *
from pygame.sprite import *
from localsprite import *
from math import *
import pprint


class Shot(LocalSprite):
    def __init__(self, position, heading, image=None, size=1, route=None, lifetime=10000):
        """Creates a new shot.

        position - a Vector2D of the shot's position
        heading - a Vector2D of the boid's initial heading
        size - the size of the shot 
        route - a route object representing the shot's behavior
        lifetime - how long it takes the shot to expire"""
        Sprite.__init__(self)
        self.heading = heading
        self.position = position
        self.size = size
        self.age = 0.0
        self.lifetime=lifetime

        if image == None:
            image = pygame.Surface((5* size, 5 * size))
            image.fill((0,255,0))
            image.convert()

        self.image = image
        self.rect = image.get_rect(center=(position.x,position.y))
        self.originalimage = image
        
        if route == None:
            self.route = advance()
        else:
            self.route = route

    def update(self):
        self.route.go(self)
        self.age += 1
        if self.age >= self.lifetime:
            self.kill()

    def __getattr__(self, name):
        """Returns a Vector2D of the shot's position."""
        if name == "position":
            return Vector2D(self.rect.centerx, self.rect.centery)
        else:
            raise AttributeError("Shot has no attribute " + name)

    def kick(self, vector):
        self.heading += vector

def floatrange(x1, x2, num):
    a = []
    n = num - 1
    for i in range(num):
        z = x1 + i * (x2 - x1) / n
        a.append(z)
    return a
