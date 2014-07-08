import random
import pygame
from vector import *

blocksize = 300

class Starlayers:
    def __init__(self, (width, height), depths = None, colors = None, density = (5,10), seed = None):
        if depths is None:
            depths = [1]
        if colors is None:
            colors = []
            for d in depths:
                colors.append(pygame.Color("#FFFFFF"))
        if seed is None:
            seed = 0
        self.starfields = []
        for (d, c) in zip(depths, colors):
            s = Starfield((width, height), d, c, density, seed)
            self.starfields.append(s)
            random.seed(seed)
            seed = random.randint(0,100000)

    def draw(self, surface, offset):
        for s in self.starfields:
            s.draw(surface, offset)

    def undraw(self, surface, color = None):
        for s in self.starfields:
            s.undraw(surface, color)

    def update(self, (screenx, screeny)):
        for s in self.starfields:
            s.update((screenx, screeny))

class Starfield:
    def __init__(self, (width, height), depth = 1, color = None, density = (5,10),  seed = 0):
        if color is None:
            self.color = pygame.Color("#FFFFFF")
        else:
            self.color = color
        self.density = density
        self.size = (width, height)
        self.depth = depth
        self.seed = seed
        self.xnumblocks = width / blocksize + 2
        self.ynumblocks = height / blocksize + 2
        self.lastoffset = (0,0)
        self.refreshcount = 0
        self.position = (0,0)
        self.refresh()
        
    def draw(self, surface, offset, color = None):
#        radius = 1
        if color is None:
            color = self.color
        (screenx,screeny) = offset
        self.lastoffset = (screenx,screeny)
        screenx = screenx / self.depth
        screeny = screeny / self.depth
        for row in self.blocks:
            for block in row:
                for (xpos, ypos) in block:
                    position = (int(xpos - screenx), int(ypos - screeny))#offset the drawing based on screen position
#                    pygame.draw.circle(surface, color, position, radius)
                    surface.set_at(position, color)

    def undraw(self, surface, color = None):
        if color is None:
            color = pygame.Color("#000000")
        self.draw(surface, self.lastoffset, color)

    def refresh(self, (screenx, screeny) = (0,0)):
#        print("ARRGG depth ", self.depth, "update ", self.refreshcount)
        self.refreshcount += 1
        self.blocks = []
        x = screenx - (screenx % blocksize)
        y = screeny - (screeny % blocksize)
        self.position = (x,y)
        for blocky in range(self.ynumblocks):
            blockrow = []
            for blockx in range(self.xnumblocks):
                pos = (blocksize * blockx + x, blocksize * blocky + y)
                b = self.makeblock(pos)
                blockrow.append(b)
            self.blocks.append(blockrow)

    def update(self, (screenx, screeny)):
        screenx /= self.depth
        screeny /= self.depth
        (x,y) = self.position
        (w,h) = self.size
        x2 = x + blocksize * self.xnumblocks
        y2 = y + blocksize * self.ynumblocks
        screenx2 = screenx + w
        screeny2 = screeny + h
        if screenx < x or screenx2 > x2 or screeny < y or screeny2 > y2:
            self.refresh((screenx,screeny))

    def makeblock(self, (x, y)):
        (a,b) = self.density
        seed = self.seed
        random.seed(x)
        seed += random.randint(0,10000)
        random.seed(y)
        seed += random.randint(0,10000)
        random.seed(seed)
        numstars = random.randint(a,b)
        white = pygame.Color(0xffffff)
        radius = 1
        stars = []
        for i in range(numstars):
            xpos = random.randint(0, blocksize) + int(x)
            ypos = random.randint(0, blocksize) + int(y)
            pos = (xpos, ypos)
            stars.append(pos)
        return stars
