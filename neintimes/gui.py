#python imports

#pygame imports
import pygame
from pygame import Rect
from pygame.locals import *
import pygame.font as ft

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

class TextBox(Widget):
    def __init__(self, position, font, text="", textcolor=(0,0,255), bgcolor=None):
        """A non-user-editable text box for displaying things on screen.
        
        font - a pygame.freetype.Font object. Size, style, text color,
        and rotation may be changed by editing the appropriate member
        variables of the font object

        position - an (x,y) coordinate pair to renter to on screen

        textcolor - the color of the rendered font. An (r,g,b) triple.

        bgcolor - the background color of the rendered font. An
        (r,g,b) triple. The background will be transparent if bgcolor
        is None

        """
        Widget.__init__(self,position)
        ft.init() #initialize the freetype module only if we need to
        self.font = font
        self.text = text
        self.textcolor = textcolor
        self.bgcolor = bgcolor
    def draw(self, deltaT):
        return self.font.render(self.text, True, self.textcolor, self.bgcolor)
        


pygame.init()
screen = Screen(640,480)
rsurface = loadsurface("rbutton.png")
dsurface = loadsurface("dbutton.png")
def callback():
    print "Hello buttons!"
position = Rect(100,100,150,50)

btn = Button(position, rsurface, dsurface, callback)
screen.addWidget(btn)

font = ft.SysFont("Courier New",30)
tb = TextBox((200,200), font, "Hello, TextBox!", (0,0,255),(0,0,0))
screen.addWidget(tb)

while True:
    for i in pygame.event.get():
        if i.type == QUIT:
            exit()
        screen.handleWidgetInput(i)
    screen.update(Vector2D(0,0))
    pygame.event.pump()
