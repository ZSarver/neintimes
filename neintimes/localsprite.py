#localsprite.py implementation of sprites and groups with
#relative placement of drawing rects

import pygame
from pygame.sprite import Sprite, Group
from vector import Vector2D

class LocalSprite(Sprite):
    def __init__(self, position=Vector2D(0,0)):
        self.position = position
        Sprite.__init__(self)

    def place(self, offset=Vector2D(0,0)):
        #Places the sprite's rect relative to the given offset
        #This should be the only thing that alters the rect after init
        self.rect.centerx = self.position.x - offset.x
        self.rect.centery = self.position.y - offset.y

#Group of localsprites
#Expects each sprite to implement place(self, offset)
class LocalGroup(Group):
    def __init__(self):
        Group.__init__(self)

    def place(self, offset=Vector2D(0,0)):
        #Places the rects for every sprite in the group
        for s in self.sprites():
            s.place(offset)
