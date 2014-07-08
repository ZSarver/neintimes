#screen.py implements drawing things on the screen.

import pygame
from vector import *
import camera
from stars import *

screenwidth = 640
screenheight = 480

class Screen:
    def __init__(self, x=screenwidth, y=screenheight, cam=None):
        self.x = x
        self.y = y

        self.displaysurface = pygame.display.set_mode((x,y))
        self.background = pygame.Surface(self.displaysurface.get_size()).convert()
        self.background.fill((0,0,0))
#        bgblock = makebgblock(0,0)
#        self.background.blit(bgblock,(0,0))
        self.displaysurface.blit(self.background,(0,0))
        pygame.display.flip()
        self.groups = []
        self.offset = Vector2D(0,0)
        depths = [15.0 / (15 - d) for d in range(10)]
        shades = [255 - (20 * d) for d in range(10)]
        colors = [pygame.Color(s, s, s, 0) for s in shades]
        density = (0,8)
        self.stars = Starlayers((x,y), depths, colors, density)
        if cam == None:
            self.cam = camera.constant(Vector2D(0,0))
        else:
            self.cam = cam

    def update(self, playerpos):
        self.clear() #remove sprites at old locations
        self.cam.go(self, playerpos)
        self.place() #move sprites rects to current sprite positions
        self.draw()
        pygame.display.flip()

    def clear(self):
        for g in self.groups:
            g.clear(self.displaysurface, self.background)
        self.stars.undraw(self.displaysurface)

    def place(self):
        #positions the sprite rects for group
        for g in self.groups:
            g.place(self.offset)
        self.stars.update((self.offset.x, self.offset.y))

    def draw(self):
        self.stars.draw(self.displaysurface,(self.offset.x, self.offset.y))
        for g in self.groups:
            g.draw(self.displaysurface)

    def add(self, group):
        #this group will be drawn to the screen
        self.groups.append(group)

    def remove(self, group):
        #this group will no longer be draw to the screen
        self.groups.remove(group)

    def center(self, place = Vector2D(0,0)):
        #centers the screen at this position
        self.offset = place - Vector2D(640 / 2, 480 / 2)
