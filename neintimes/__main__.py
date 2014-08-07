
#pygame imports
import pygame

#neintimes imports
from pygame.locals import *
from boid import *
from screen import *
from flock import *
from data import *
from math import *
from weaponry import *
from input import *
from statuseffects import *
import player
import camera
import random
from formationEditor import FormationEditor
import state

class MainGame(state.State):
    def __init__(self, screen):
        """ your app starts here"""
        state.State.__init__(self, screen)
        #create game objects
        self.fgroup = Flock(1.2,0.0)
        #sprite groups must be added to the screen to be drawn
        image = loadsurface("small2.png")
        pimage = loadsurface("anchor.png")
        #~ image = pygame.Surface((15, 15))
        #~ image.fill((0,255,0))
        #~ image.convert()
        self.p = player.Player(None, pimage)
        for i in range(9):
            b = Boid(Vector2D(0,0),image)
            self.fgroup.addSquad(b)
        self.fgroup.addAnchor(self.p)
        t = testEffect()
        applyEffect(b, None, t)

    def run(self):
        #deal with eventlist
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()
        (thrustDirection, boost, rotation, shooting, changeState)  = getInputActions()
        if changeState:
            state.statemanager.switch("fe", self.fgroup.formation)
        self.p.playerInput(thrustDirection, boost, rotation, shooting)

        self.fgroup.update()
        self.screen.update(self.p.position) #center camera on player
        pygame.event.pump()

    def switchin(self):
        state.State.switchin(self)
        #register sprites
        self.screen.add(self.fgroup)
        #no widgets to register
        #switch camera
        self.screen.cam = camera.roughTrack(self.p.position)

    def switchout(self):
        #unregister sprites
        self.screen.remove(self.fgroup)
        #no widgets to unregister

if __name__ == "__main__":
    random.seed()
    print "Initializing pygame..."
    pygame.init()
    print "Creating screen"
    screen = Screen(640,480,camera.roughTrack(0))
    game = MainGame(screen)
    editor = FormationEditor(screen)

    state.statemanager.addstate(game, "game")
    state.statemanager.addstate(editor, "fe")
    state.statemanager.switch("game")

    while True:
        state.statemanager.state.run()
