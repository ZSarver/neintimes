#camera.py
import pygame
from vector import *

class Camera:
    """A wrapper for manipulating and composing camera related
    functions. Composition is given by addition.

    A camera function must accept at least two argument: the player's
    position as a Vector2D and the camera's position as a Vector2D. It
    should act on the camera position based on that player position
    (with possibly some extra parameters.)"""
    def __init__(self, func):
        self.go = func

    def __add__(self, unself):
        def f(screen, playerpos):
            self.go(screen, playerpos)
            unself.go(screen, playerpos)
        return Camera(f)

def constant(n):
    def f(screen, playerpos):
        screen.offset = n
    return Camera(f)

def roughTrack(maxDistance):
    def f(screen, playerpos):
        center = playerpos - Vector2D(screen.x/2, screen.y/2)
        if (screen.offset - center).magnitude > maxDistance:
            screen.offset = center
    return Camera(f)
