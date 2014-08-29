#route.py
import pygame
from vector import *
from pygame.sprite import *
from localsprite import *
from math import *
import pprint
import random

#the route class is a wrapper for functions that describe a shot's behavior
#it's main purpose is to allow addition of such functions
class Route:
    def __init__(self, func):
        self.go = func

    def __add__(self, unself):
        def f(shot):
            self.go(shot)
            unself.go(shot)
        return Route(f)
