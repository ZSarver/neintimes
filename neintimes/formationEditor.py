#python imports
from copy import deepcopy

#pygame imports
import pygame
import pygame.cursors
import pygame.mouse
from pygame.locals import *

#neintimes imports
from screen import *
from formation import *
from vector import Vector2D
from localsprite import *
from data import loadsurface

#convenient constants
MOUSE_LB = 1
MOUSE_RB = 3

class SimpleEditorSprite(LocalSprite):
    def __init__(self, position=Vector2D(0,0), image=None):
        LocalSprite.__init__(self, position)
        self.image = image
        self.originalimage = image
        self.rect = image.get_rect()
        self.aim = 0.0

    def update(self, aimoffset):
        #update aim
        self.aim = self.aim + aimoffset
        print "New aim = " + str(self.aim)
        self.image = pygame.transform.rotate(self.originalimage,degrees(float(self.aim)))
        
class FormationEditor(object):
    def __init__(self, screen):
        self.screen = screen
        #set up a list of [FormationSlot,SimpleEditorSprite] pairs
        self.slotSprites = []
        for i in range(9):
            self.slotSprites.append([FormationSlot(Vector2D(i*40,50),0,None,0),SimpleEditorSprite(Vector2D(i*40,50),loadsurface("small2.png"))])
        self.selected = None
        #set up a drawing group
        self.drawgroup = LocalGroup()
        #set up sprites for all the ships in the formation
        for i in self.slotSprites:
            self.drawgroup.add(i[1])
        #register this drawing group with screen
        self.screen.add(self.drawgroup)
        #still need to set up cursor stuff maybe?
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        pygame.mouse.set_visible(True)
        #when left-clicked, the user is making a move action
        self.moveAction = False
        #when right-clicked, the user is making a rotate action
        self.rotateAction = False
        
    def run(self):
        while True:
            for i in pygame.event.get():
                if i.type == QUIT:
                    exit()
                if i.type == MOUSEBUTTONUP:
                    self.handlemouseup(i)
                if i.type == MOUSEBUTTONDOWN:
                    self.handlemousedown(i)
                if i.type == MOUSEMOTION:
                    self.handlemousemotion(i)
            self.screen.update(None)
            pygame.event.pump()

    def handlemousedown(self,event):
        if event.button == MOUSE_LB and not self.rotateAction:
            #prevent moving and rotating at the same time
            self.moveAction = True
            #select a ship
            for i in self.slotSprites:
                if i[1].rect.collidepoint(event.pos):
                    self.selected = i
            print "Move Action. Selected = " + str(self.selected)
        if event.button == MOUSE_RB and not self.moveAction:
            #prevent moving and rotating at the same time
            self.rotateAction = True
            print "Rotate Action"
            #select a ship
            for i in self.slotSprites:
                if i[1].rect.collidepoint(event.pos):
                    self.selected = i

    def handlemouseup(self,event):
        if event.button == MOUSE_LB and self.moveAction:
            self.moveAction = False
            self.selected = None
        if event.button == MOUSE_RB and self.rotateAction:
            self.rotateAction = False
            self.selected = None

    def handlemousemotion(self,event):
        if self.moveAction and (self.selected is not None):
            self.selected[0].spacialOffset = self.selected[0].spatialOffset + Vector2D(*event.rel)
            self.selected[1].position = self.selected[1].position + Vector2D(*event.rel)
        if self.rotateAction and (self.selected is not None):
            self.selected[1].update(0.01 * Vector2D(*event.rel).magnitude)
            
pygame.init()
screen = Screen(640,480)
fe = FormationEditor(screen)
fe.run()
