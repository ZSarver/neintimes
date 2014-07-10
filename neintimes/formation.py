#formation.py - definition of formation structure and helpers

from vector import *

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
		for s in slotList:
			self.slotList.append(s)
	def numSlots(self):
		return len(self.slotList)
	def addSlot(self, s):
		self.slotList.append(s)
	def deleteSlot(self, index=-1):
		del self.slotList[index]
	
