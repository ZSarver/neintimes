
#pygame imports
import pygame
from pygame.sprite import *

#neintimes imports
from pygame.locals import *
from boid import *
from screen import *
from flock import *
from data import *
from math import *
from weaponry import *
from weaponry.weapons import *
from input import *
from statuseffects import *
import anchor
import camera
import random
from formationEditor import FormationEditor
import state
from formation import Formation
from enemy import *

class MainGame(state.State):
    def __init__(self, screen):
        """ your app starts here"""
        state.State.__init__(self, screen)
        #create game objects
        self.fgroup = Flock(1.2)
        #sprite groups must be added to the screen to be drawn
        image = loadsurface("small2.png")
        pimage = loadsurface("anchor.png")
        #player stuff
        self.p = anchor.Anchor(Vector2D(0,0),pimage)
        for i in range(9):
            b = Boid(Vector2D(0,0),image, weap=weapons.weapons.machinegun())
            self.fgroup.addSquad(b)
        self.fgroup.addAnchor(self.p)
        self.screen.add(self.fgroup)
        #create an enemy
        self.enemy = spawnEnemy(Vector2D(100,100), 0, defaultBehavior, enemyformation(), image, pimage, self.p)
        self.screen.add(self.enemy)

    def run(self):
        #deal with eventlist
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()
        self.checkCollisions()
        (thrustDirection, boost, rotation, shooting, changeState)  = getInputActions()
        if changeState:
            state.statemanager.switch("fe", self.fgroup.formation)
        self.p.playerInput(thrustDirection, boost, rotation, shooting)

        self.fgroup.update()
        self.enemy.update()
        self.screen.update(self.p.position) #center camera on player
        pygame.event.pump()
        
    def checkCollisions(self):
        #player/enemy bullet collisions
        playerShipsHit = groupcollide(self.fgroup, self.enemy.shotgroup,
                                      False, False, collide_circle)
                                      
        enemyShipsHit = groupcollide(self.enemy, self.fgroup.shotgroup,
                                     False, False, collide_circle)
        
        for ship in playerShipsHit.iterkeys():
            for shot in playerShipsHit[ship]:
                shot.impact(ship)
        for ship in enemyShipsHit.iterkeys():
            for shot in enemyShipsHit[ship]:
                shot.impact(ship)
            
    def switchin(self, *args):
        """args should be a tuple of exactly 1 element, a Formation object"""
        state.State.switchin(self)
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
    screen = Screen(800,600,camera.roughTrack(0))
    game = MainGame(screen)
    editor = FormationEditor(screen)

    state.statemanager.addstate(game, "game")
    state.statemanager.addstate(editor, "fe")
    state.statemanager.switch("game")

    while True:
        state.statemanager.state.run()
