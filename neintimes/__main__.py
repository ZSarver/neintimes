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
from boid import Boid
from vector import Vector2D
from statuseffects import testEffect, applyEffect
from formationEditor import FormationEditor
from input import getInputActions
from formation import Formation, enemyformation
from anchor import Anchor
from weaponry.weapons.weapons import machinegun
from enemy import spawnEnemy, defaultBehavior

class MainGame(State):
    def __init__(self, screen):
        """ your app starts here"""
        State.__init__(self, screen)
        #create game objects
        self.playerFlock = Flock(1.2)
        #sprite groups must be added to the screen to be drawn
        image = loadsurface("small2.png")
        pimage = loadsurface("anchor.png")
        #game object list creation and registration
        self.allyList = []
        self.enemyList = []
        self.screen.add(self.allyList)
        self.screen.add(self.enemyList)
        #player stuff
        self.register(self.allyList, self.playerFlock)
        p = Anchor(Vector2D(0,0),pimage)
        for i in range(9):
            b = Boid(Vector2D(0,0),image, weap=machinegun())
            self.playerFlock.addSquad(b)
        self.playerFlock.addAnchor(p)
        #create an enemy
        enemy = spawnEnemy(Vector2D(100,100), 0, defaultBehavior, enemyformation(), image, pimage, p)
        self.register(self.enemyList, enemy)


    def register(self,list,entity):
        list.append(entity)
        def f():
            list.remove(entity)
        entity.unregister = f

    def run(self):
        #deal with eventlist
        for i in pygame.event.get():
            if i.type == pl.QUIT:
                exit()
        self.checkCollisions()
        (thrustDirection, boost, rotation, shooting, changeState)  = getInputActions()
        if changeState:
            statemanager.switch("fe", self.playerFlock.formation)
        self.playerFlock.anchor.playerInput(thrustDirection, boost, rotation, shooting)
        for ally in self.allyList:
            ally.update()
        for enemy in self.enemyList:
            enemy.update()
        self.screen.update(self.playerFlock.anchor.position) #center camera on player
        pygame.event.pump()
        
    def checkCollisions(self):
        #player/enemy bullet collisions
        playerShipsHit = {}
        for ally in self.allyList:
            for enemy in self.enemyList:
                playerShipsHit = pygame.sprite.groupcollide(ally, enemy.shotgroup,
                                      False, False, pygame.sprite.collide_circle)
                enemyShipsHit = pygame.sprite.groupcollide(enemy, ally.shotgroup,
                                     False, False, pygame.sprite.collide_circle)
                for ship in playerShipsHit.iterkeys():
                    for shot in playerShipsHit[ship]:
                        shot.impact(ship)
                for ship in enemyShipsHit.iterkeys():
                    for shot in enemyShipsHit[ship]:
                        shot.impact(ship)
            
    def switchin(self, *args):
        """args should be a tuple of exactly 1 element, a Formation object"""
        State.switchin(self)
        if len(args) > 1:
            raise ValueError("MainGame.switchin() should take 1 or fewer arguments!")
        if len(args) == 1:
            if not isinstance(args[0],Formation):
                raise ValueError("MainGame.switchin() needs a Formation object!")
        if len(args) == 1:
            self.playerFlock.changeFormation(args[0])
            #register sprites
            self.screen.add(self.playerFlock)
            #no widgets to register
            #switch camera
            self.screen.cam = roughTrack(self.playerFlock.anchor.position)

    def switchout(self):
        #unregister sprites
        self.screen.remove(self.playerFlock)
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
