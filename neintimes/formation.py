#formation.py - definition of formation structure and helpers

from vector import *
from copy import deepcopy
from math import pi
from weaponry import *

class FormationSlot:
    def __init__(self, spatialOffset=None, angularOffset=0, weapon=None, timeOffset=0, name = "" ):
        zero = Vector2D(0,0)
        if spatialOffset == None:
            spatialOffset = zero
        self.spatialOffset = spatialOffset
        self.timeOffset = timeOffset
        self.angularOffset = angularOffset
        self.weapon = weapon
        self.name = name

class Formation:
    def __init__(self, slotList):
        self.slotList = []
        for s in slotList:
            self.slotList.append(s)
    def __iter__(self):
        return self.slotList.__iter__()
    def numSlots(self):
        return len(self.slotList)
    def addSlot(self, s):
        self.slotList.append(s)
    def deleteSlot(self, index=-1):
        del self.slotList[index]
    def getSlot(self, index):
        s = self.slotList[index]
        return deepcopy(s)
        


def testFormation():
    #~ v1 = Vector2D(-30,0)
    #~ v2 = Vector2D(-50,-50)
    #~ v3 = Vector2D(-50,50)
    #~ s1 = FormationSlot(v1,0)
    #~ s2 = FormationSlot(v2,-pi/6)
    #~ s3 = FormationSlot(v3,pi/6)
    #~ f = Formation([s1,s2,s3])
    l = []
    for i in range(9):
        a = (i-4) * pi / 4.5
        d = 60 
        v = vectorfromangle(a).mult(d)
        t = abs(i - 4) * 5
        s = FormationSlot(v, a, None, t, str(i))
        l.append(s)
    f = Formation(l)
    return f

def enemyformation():
	v1 = Vector2D(-30,0)
	v2 = Vector2D(-50,-50)
	v3 = Vector2D(-50,50)
	w = weapon.enemyweapon()
	s1 = FormationSlot(v1,0, weapon=w)
	s2 = FormationSlot(v2,-pi/6, weapon=w)
	s3 = FormationSlot(v3,pi/6, weapon=w)
	f = Formation([s1,s2,s3])
	return f