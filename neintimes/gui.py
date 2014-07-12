#python imports

#pygame imports
import pygame
from pygame import Rect
from pygame.locals import *

#neintimes imports
from screen import Screen
from data import *
from vector import Vector2D

class Widget(object):
    def __init__(self, position):
        """A template class for GUI widget objects to inherit from.

        position - a rect representing the widgets's position on screen"""
        self.position = position
    def handleInput(self,event):
        pass
    def draw(self, deltaT):
        """Should just return a surface for the Screen class to do the blitting."""
        pass

class Button(Widget):
    def __init__(self, position, rsurface, dsurface, callback):
        """A class for clickable onscreen buttons.
        
        position - a rect representing the button's position on screen
        rsurface - raised surface, for when the button is not being clicked
        dsurface - depressed surface, for whent the button has been clicked
        callback - a callback function, called when the button is clicked"""
        Widget.__init__(self, position)
        self.rsurface = rsurface
        self.dsurface = dsurface
        self.callback = callback
        self.animationtimer = 0
    def handleInput(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if self.position.collidepoint(event.pos):
                callback()
                self.animationtimer = 500
    def draw(self, deltaT):
        if self.animationtimer > 0:
            self.animationtimer -= deltaT
            return self.dsurface
        else:
            self.animationtimer = 0
            return self.rsurface

pygame.init()
screen = Screen(640,480)
rsurface = loadsurface("rbutton.png")
dsurface = loadsurface("dbutton.png")
def callback():
    print "Hello buttons!"
position = Rect(100,100,150,50)

btn = Button(position, rsurface, dsurface, callback)
screen.addWidget(btn)

while True:
    for i in pygame.event.get():
        if i.type == QUIT:
            exit()
        screen.handleWidgetInput(i)
    screen.update(Vector2D(0,0))
    pygame.event.pump()
