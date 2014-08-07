#python imports
import math

#pygame imports
import pygame
import pygame.cursors
import pygame.mouse
from pygame.locals import *
import pygame.font as ft

#neintimes imports
from screen import *
from formation import *
from vector import Vector2D
from localsprite import *
from data import loadsurface
from state import *
from gui import *

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

    def updatepos(self, spacialoffset):
        self.position = spacialoffset

    def updateaim(self, aimoffset):
        self.aim = self.aim + aimoffset
        self.image = pygame.transform.flip(pygame.transform.rotate(self.originalimage,degrees(float(self.aim))),False,True)
        self.rect = self.image.get_rect()

    def setpos(self, spacialoffset, screen):
        self.position = spacialoffset + Vector2D(screen.x/2,screen.y/2)

    def setaim(self, aimoffset):
        self.aim = aimoffset
        self.image = pygame.transform.flip(pygame.transform.rotate(self.originalimage,degrees(float(self.aim))),False,True)
        self.rect = self.image.get_rect()
        
class FormationEditor(State):
    def __init__(self, screen):
        State.__init__(self, screen)
        #set up a list of [FormationSlot,SimpleEditorSprite] pairs
        self.slotSprites = []
        for i in range(9):
            fs = FormationSlot(Vector2D(i*40,50),0,None,0, str(i))
            ses = SimpleEditorSprite(Vector2D(i*40,50),loadsurface("small2.png"))
            self.slotSprites.append([fs,ses])
        self.clicked = None #clicked for dragging/rotating
        self.selected = None #selected for sidebar
        #set up a drawing group
        self.drawgroup = LocalGroup()
	#set up widgets
	self.widgets = {}
	self.sidebarActive = False
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
            self.screen.handleWidgetInput(i)
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

    def switchin(self, *args):
        """args should be a single-element tuple consisting of a
        formation"""
        if len(args) != 1:
            raise ValueError("formationEditor.switchin() should have exactly 1 element!")
        State.switchin(self)
        #register sprites
        for i in range(len(self.slotSprites)):
            a = args[0].getSlot(i)
            self.slotSprites[i][0] = a
            self.slotSprites[i][1].setpos(a.spatialOffset, self.screen)
            self.slotSprites[i][1].setaim(a.angularOffset)
        self.screen.add(self.drawgroup)
        #no widgets
        #camera
        self.screen.cam = camera.constant(Vector2D(0,0))
    
    def switchout(self):
        self.screen.remove(self.drawgroup) #unregister sprites
        #unregister widgets
        if self.sidebarActive:
	    self.cleanSidebar(self.selected)
	    self.sidebarActive = False

    def handlekeyboard(self,event):
        if event.key == K_TAB:
	    fleet = Formation([])
	    for i in self.slotSprites:
		fleet.addSlot(i[0])
	    statemanager.switch("game", fleet)

    def handlemousedown(self,event):
        if event.button == MOUSE_LB and not self.rotateAction:
            #prevent moving and rotating at the same time
            self.moveAction = True
            #select a ship
            for i in self.slotSprites:
                if i[1].rect.collidepoint(event.pos):
		    old = self.selected
                    self.clicked = i
                    self.selected = i
                    #bring up sidebar
		    if self.sidebarActive: 
			#if the sidebar is already active, clean up the old widgets
			self.cleanSidebar(old)
                    self.createSidebar()
        if event.button == MOUSE_RB and not self.moveAction:
            #prevent moving and rotating at the same time
            self.rotateAction = True
            #select a ship
            for i in self.slotSprites:
                if i[1].rect.collidepoint(event.pos):
		    old = self.selected
                    self.clicked = i
                    self.selected = i
                    #bring up sidebar
		    if self.sidebarActive: 
			#if the sidebar is already active, clean up the old widgets
			self.cleanSidebar(old)
                    self.createSidebar()

    def handlemouseup(self,event):
        if event.button == MOUSE_LB and self.moveAction:
            self.moveAction = False
            self.clicked = None
        if event.button == MOUSE_RB and self.rotateAction:
            self.rotateAction = False
            self.clicked = None

    def handlemousemotion(self,event):
        if self.moveAction and (self.clicked is not None):
            self.clicked[0].spatialOffset = self.clicked[0].spatialOffset + Vector2D(*event.rel)
            self.clicked[1].position = self.clicked[1].position + Vector2D(*event.rel)
        if self.rotateAction and (self.clicked is not None):
            self.clicked[1].setaim((Vector2D(*event.pos) - self.clicked[1].position).direction)
            self.clicked[0].angularOffset = self.clicked[1].aim

    def createSidebar(self):
	self.sidebarActive = True
        startx = (self.screen.x * 2)/3 #use the right 1/3 of the screen
        #ship name
        font = ft.SysFont("Courier New", 20)
        name = "Ship " + self.selected[0].name
        self.widgets["sidebarShipName"] = TextBox((startx,10), font, name, (255,255,255),(0,0,0))
        #spatial offset
        def soCallback():
            return "Spatial Offset " + str(self.selected[0].spatialOffset)
        self.widgets["sidebarShipSOffset"] = UpdatingTextBox((startx,30), font, soCallback, (255,255,255),(0,0,0))
        #angular offset
        def aoCallback():
            return "Angular Offset " + str(math.degrees(self.selected[0].angularOffset))
        self.widgets["sidebarShipAOffset"] = UpdatingTextBox((startx, 50), font, aoCallback, (255,255,255), (0,0,0))
        #time offset
        rslider = loadsurface("rslider.png")
        sslider = loadsurface("sslider.png")
        to = self.selected[0].timeOffset
        self.widgets["sidebarShipTOSlider"] = Slider((startx+15, 90), 0, 50, to, sslider, rslider)
        #time offset labels
        self.widgets["sidebarShipTOSliderMin"] = TextBox((startx, 90), font, "0", (255,0,0), (0,0,0))
        w = self.widgets["sidebarShipTOSlider"].size().width
        self.widgets["sidebarShipTOSliderMax"] = TextBox((startx+w+20,90), font, "50", (0,0,255), (0,0,0))
        def toCallback():
            return "Time Offset: " + str(self.widgets["sidebarShipTOSlider"].currentval)
        self.widgets["sidebarShipTOSliderCur"] = UpdatingTextBox((startx,70), font, toCallback, (255,255,255), (0,0,0))
        for k,w in self.widgets.iteritems():
	    self.screen.addWidget(w)
        
    def cleanSidebar(self, old):
	if old is not None:
	    #save old time offset
	    old[0].timeOffset = self.widgets["sidebarShipTOSlider"].currentval
	for k,w in self.widgets.iteritems():
	    self.screen.removeWidget(w)
	    w = None
        
if __name__ == "__main__":
    pygame.init()
    screen = Screen(640,480)
    fe = FormationEditor(screen)
    fe.run()
