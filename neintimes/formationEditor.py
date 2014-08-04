#python imports
import cPickle as pickle

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
from state import *

#convenient constants
MOUSE_LB = 1
MOUSE_RB = 3
PICKLE_JAR = "formations.pi"
PICKLE_PROTOCOL = 2

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
        self.image = pygame.transform.rotate(self.originalimage,degrees(float(self.aim)))
        self.rect = self.image.get_rect()
        
class FormationEditor(State):
    def __init__(self, screen):
        State.__init__(self, screen)
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
        #still need to set up cursor stuff maybe?
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        pygame.mouse.set_visible(True)
        #when left-clicked, the user is making a move action
        self.moveAction = False
        #when right-clicked, the user is making a rotate action
        self.rotateAction = False
        
    def run(self):
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()
            if i.type == MOUSEBUTTONUP:
                self.handlemouseup(i)
            if i.type == MOUSEBUTTONDOWN:
                self.handlemousedown(i)
            if i.type == MOUSEMOTION:
                self.handlemousemotion(i)
            if i.type == KEYDOWN:
                self.handlekeyboard(i)
        self.screen.update(Vector2D(0,0))
        pygame.event.pump()

    def switchin(self):
        State.switchin(self)
        #register sprites
        self.screen.add(self.drawgroup)
        #no widgets
        #camera
        self.screen.cam = camera.constant(Vector2D(0,0))

    def switchout(self):
        #unregister sprites
        self.screen.remove(self.drawgroup)
        #no widgets

    def handlekeyboard(self,event):
        if event.key == K_s:
            print "Enter filename to save. Enter nothing to cancel."
            filename = raw_input("Filename?")
            if filename != "":
                self.save(filename)
        if event.key == K_l:
            print "Enter filename to load. Enter nothing to cancel."
            filename = raw_input("Filename?")
            if filename != "":
                self.load(filename)
        if event.key == K_TAB:
            statemanager.switch("game")

    def handlemousedown(self,event):
        if event.button == MOUSE_LB and not self.rotateAction:
            #prevent moving and rotating at the same time
            self.moveAction = True
            #select a ship
            for i in self.slotSprites:
                if i[1].rect.collidepoint(event.pos):
                    self.selected = i
        if event.button == MOUSE_RB and not self.moveAction:
            #prevent moving and rotating at the same time
            self.rotateAction = True
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
            self.selected[0].spatialOffset = self.selected[0].spatialOffset + Vector2D(*event.rel)
            self.selected[1].position = self.selected[1].position + Vector2D(*event.rel)
        if self.rotateAction and (self.selected is not None):
            self.selected[1].update(0.01 * Vector2D(*event.rel).magnitude)
            self.selected[0].angularOffset = self.selected[1].aim

    def save(self,filename=None):
        fleet = Formation([])
        for i in self.slotSprites:
            fleet.addSlot(i[0])
        if filename is None:
            f = open(PICKLE_JAR, "wb")
        else:
            f = open(filename, "wb")
        pickle.dump(fleet,f,PICKLE_PROTOCOL)
        f.close()

    def load(self,filename=None):
        if filename is None:
            f = open(PICKLE_JAR, "rb")
        else:
            f = open(filename, "rb")
        fleet = None
        fleet = pickle.load(f)
        f.close()
        #now reconstruct the slotSprites list
        for i in range(fleet.numSlots()):
            self.slotSprites[i][0] = fleet.getSlot(i)
            self.slotSprites[i][1].position = fleet.getSlot(i).spatialOffset
            self.slotSprites[i][1].update(fleet.getSlot(i).angularOffset)
            
if __name__ == "__main__":
    pygame.init()
    screen = Screen(640,480)
    fe = FormationEditor(screen)
    fe.run()
