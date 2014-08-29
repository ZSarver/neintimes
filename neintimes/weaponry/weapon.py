#weapon.py

#python imports
import random

#neintimes imports
from shot import *
from route import *
from vector import *
from statuseffects import *

            
class Weapon:
    def __init__(self, f = None, cooldown = None):
        assert(f is not None)
        assert(cooldown is not None)
        # f is called when the weapon fires to spawn projectiles
        # f( V2D:position, float:direction, V2D:momentum, shotgroup )
        self.func = f
        self.delay = 0
        self.cooldown = cooldown

    def cool(self):
        self.delay -= 1
        if self.delay <= 0:
            self.delay = 0

    def canfire(self):
        if self.delay == 0:
            return True
        else:
            return False

    def fire(self, position, direction, momentum, shotgroup):
        if self.canfire():
            self.func(position, direction, momentum, shotgroup)
            self.delay += self.cooldown
            return True
        else:
            return False