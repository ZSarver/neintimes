#flock.py - implements a flock of boids

import pygame
from data import *
from vector import *
from pygame.sprite import *
from localsprite import *
from formation import *
from copy import deepcopy
import pprint

MAX_HISTORY_FRAMES = 300

class Flock(LocalGroup):
    def __init__(self, accelConst=1.2, formation=None):
        Group.__init__(self)
        self.centerOfMass = None
        self.momentum = None
        self.targetLocation = None
        self.accelConst = accelConst
        self.shotgroup = LocalGroup()
        self.anchorgroup = LocalGroup()
        self.squad = []
        self.anchor = None
        if formation == None:
            formation = testFormation()
        self.formation = formation

    def addSquad(self, boid):
        self.add(boid)
        l = len(self.squad)
        #crash if trying to overfill a flock
        assert(l < self.formation.numSlots())
        boid.formationSlot = self.formation.getSlot(l)
        self.squad.append(boid)
    def addAnchor(self, anchor):
        self.anchor = anchor
        self.anchorgroup.add(self.anchor)
        self.anchor.setSquad(self.squad)
        self.anchor.history = []
    def draw(self, screen):
        self.anchorgroup.draw(screen)
        self.shotgroup.draw(screen)
        LocalGroup.draw(self, screen)

    def place(self, offset=Vector2D(0,0)):
        self.shotgroup.place(offset)
        self.anchorgroup.place(offset)
        LocalGroup.place(self, offset)

    def clear(self, screen, background):
        self.shotgroup.clear(screen, background)
        Group.clear(self, screen, background)

    def update(self):
        """Updates, calculating everything each individual boid needs
        to know to flock effectively."""
        self.shotgroup.update()
        p = self.anchor.position
        m = self.anchor.momentum
        a = self.anchor.aim
        f = self.anchor.shooting
        h = self.anchor.history
        h.append((p,m,a,f))
        l = len(h)
        if l > MAX_HISTORY_FRAMES*2:
            h = h[l-MAX_HISTORY_FRAMES:l]
        for ship in self.squad:
            formationSlot = ship.formationSlot
            t = formationSlot.timeOffset
            if t < len(h) and t > 0:
                (p,m,a,f) = h[-t]
            else:
                p = self.anchor.position
                m = self.anchor.momentum
                a = self.anchor.aim
                f = self.anchor.shooting
            targetLocation = p + formationSlot.spatialOffset.rotate(a)
            targetAim = a + formationSlot.angularOffset
            ship.update(targetLocation, targetAim, m,f)
        self.anchor.update()

    def changeFormation(self, formation):
        self.formation = formation
        for i in range(len(self.squad)):
            self.squad[i].formationSlot = self.formation.getSlot(i)
