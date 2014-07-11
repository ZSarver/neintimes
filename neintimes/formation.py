#formation.py - definition of formation structure and helpers

from vector import *
from copy import deepcopy

class FormationSlot:
    def __init__(self, spatialOffset=None, angularOffset=0, weapon=None, timeOffset=0 ):
        zero = Vector2D(0,0)
        if spatialOffset == None:
            spatialOffset = zero
        self.spatialOffset = spatialOffset
        self.timeOffset = timeOffset
        self.angularOffset = angularOffset
        self.weapon = weapon

class Formation:
    def __init__(self, slotList):
        self.slotList = []
        for s in slotList:
            self.slotList.append(s)
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
    v1 = Vector2D(-30,0)
    v2 = Vector2D(-50,-50)
    v3 = Vector2D(-50,50)
    s1 = FormationSlot(v1,0)
    s2 = FormationSlot(v2,-pi/6)
    s3 = FormationSlot(v3,pi/6)
    f = Formation([s1,s2,s3])
    return f
