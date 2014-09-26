#python imports
import random

#pygame imports
import pygame
import pygame.locals as pl

#neintimes imports
from state import State, statemanager
from screen import Screen
from camera import roughTrack
from flock import Flock
from data import loadsurface
from player import Player
from boid import Boid
from vector import Vector2D
from statuseffects import testEffect, applyEffect
from formationEditor import FormationEditor
from input import getInputActions
from formation import Formation

class MainGame(State):
    def __init__(self, screen):
        """ your app starts here"""
        State.__init__(self, screen)
        #create game objects
        self.fgroup = Flock(1.2,0.0)
        #sprite groups must be added to the screen to be drawn
        image = loadsurface("small2.png")
        pimage = loadsurface("anchor.png")
        #~ image = pygame.Surface((15, 15))
        #~ image.fill((0,255,0))
        #~ image.convert()
        self.p = Player(None, pimage)
        for i in range(9):
            b = Boid(Vector2D(0,0),image)
            self.fgroup.addSquad(b)
        self.fgroup.addAnchor(self.p)
        t = testEffect()
        applyEffect(b, None, t)

    def run(self):
        #deal with eventlist
        for i in pygame.event.get():
            if i.type == pl.QUIT:
                exit()
        (thrustDirection, boost, rotation, shooting, changeState)  = getInputActions()
        if changeState:
            statemanager.switch("fe", self.fgroup.formation)
        self.p.playerInput(thrustDirection, boost, rotation, shooting)

        self.fgroup.update()
        self.screen.update(self.p.position) #center camera on player
        pygame.event.pump()

    def switchin(self, *args):
	"""args should be a tuple of exactly 1 element, a Formation object"""
        State.switchin(self)
        if len(args) > 1:
	    raise ValueError("MainGame.switchin() should take 1 or fewer arguments!")
	if len(args) == 1:
		if not isinstance(args[0],Formation):
		    raise ValueError("MainGame.switchin() needs a Formation object!")
	if len(args) == 1:
	    self.fgroup.changeFormation(args[0])
        #register sprites
        self.screen.add(self.fgroup)
        #no widgets to register
        #switch camera
        self.screen.cam = roughTrack(self.p.position)

    def switchout(self):
        #unregister sprites
        self.screen.remove(self.fgroup)
        #no widgets to unregister

if __name__ == "__main__":
    random.seed()
    print "Initializing pygame..."
    pygame.init()
    print "Creating screen"
    screen = Screen(640,480,roughTrack(0))
    game = MainGame(screen)
    editor = FormationEditor(screen)

    statemanager.addstate(game, "game")
    statemanager.addstate(editor, "fe")
    statemanager.switch("game")

    while True:
        statemanager.state.run()
