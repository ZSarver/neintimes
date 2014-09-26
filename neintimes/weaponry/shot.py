#shot.py - implements shots

import pygame
import pprint
from vector import Vector2D
from weapons.routes import advance
from localsprite import LocalSprite

class Shot(LocalSprite):
    def __init__(self, position=None, heading=None, image=None, size=1, 
                 route=None, lifetime=300, payload=None):
        """Creates a new shot.

        position - a Vector2D of the shot's position
        heading - a Vector2D of the boid's initial heading
        size - the size of the shot 
        route - a route object representing the shot's behavior
        lifetime - how long it takes the shot to expire
        payload - a function that takes a shot and a target"""
        assert(position is not None)
        assert(heading is not None)
        assert(payload is not None)
        assert(route is not None)
        LocalSprite.__init__(self, position)
        self.heading = heading # V2D
        self.position = position # V2D
        self.size = size
        self.age = 0.0
        self.lifetime=lifetime
        self.payload=payload

        if image == None: #TODO: crash here
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

    def impact(self, target):
        self.payload(self,target)

def floatrange(x1, x2, num):
    a = []
    n = num - 1
    for i in range(num):
        z = x1 + i * (x2 - x1) / n
        a.append(z)
    return a
