#python imports

#pygame imports
import pygame
from pygame import Rect
from pygame.locals import *
import pygame.font as ft

#neintimes imports
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
    def size(self):
        """Should return an on-screen size Rect."""
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
                self.callback()
                self.animationtimer = 500
    def draw(self, deltaT):
        if self.animationtimer > 0:
            self.animationtimer -= deltaT
            return self.dsurface
        else:
            self.animationtimer = 0
            return self.rsurface
    def size(self):
        return self.position

class TextBox(Widget):
    def __init__(self, position, font, text="", textcolor=(0,0,255), bgcolor=(0,0,0)):
        """A non-user-editable text box for displaying things on screen.
        
        font - a pygame.freetype.Font object. Size, style, text color,
        and rotation may be changed by editing the appropriate member
        variables of the font object

        position - an (x,y) coordinate pair for the top-left corner of
        the text box

        textcolor - the color of the rendered font. An (r,g,b) triple.

        bgcolor - the background color of the rendered font. An
        (r,g,b) triple. The background will be transparent if bgcolor
        is None

        """
        Widget.__init__(self,position)
        ft.init() #initialize the font module only if we need to
        #multiple initializations are safe
        self.font = font
        self._text = text
        self.textcolor = textcolor
        self.bgcolor = bgcolor
    def draw(self, deltaT):
        return self.font.render(self.text, True, self.textcolor, self.bgcolor)
    def size(self):
        return Rect(self.position, self.font.size(self.text))
    @property
    def text(self):
        return str(self._text)
    @text.setter
    def text(self, value):
        self._text = value

class UpdatingTextBox(TextBox):
    def __init__(self, position, font, callback, textcolor=(0,0,255), bgcolor=(0,0,0)):
        """A textbox that rather having a static text string, updates what it
        what it displays by calling a callback function every frame. All
        arguments as in TextBox except

        callback - A callback function that will be called every frame.
        Should return a value."""
        TextBox.__init__(self, position, font, "", textcolor, bgcolor)
        self.callback = callback
    @property
    def text(self):
        return str(self.callback())

class EditableTextBox(TextBox):
    def __init__(self, position, font, text="...", textcolor=(0,0,255), bgcolor=(0,0,0)):
        TextBox.__init__(self, position, font, text, textcolor, bgcolor)
        self.capturing = False
    def handleInput(self,event):
        if event.type == MOUSEBUTTONDOWN:
            r = Rect(self.position, self.font.size(self.text))
            if r.collidepoint(event.pos):
                self.capturing = True
            else:
                self.capturing = False
        if self.capturing:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.text = self.text[0:-1]
                if event.key <= 127 and not event.key == K_BACKSPACE:
                    if (event.mod & KMOD_SHIFT):
                        self.text = self.text + chr(event.key).upper()
                    else:
                        self.text = self.text + chr(event.key)

class Slider(Widget):
    def __init__(self, position, minval, maxval, defaultval, sSurface, rSurface):
        """A class for a click-n-dragable slider widget. Intended for integers.
 
        position - A pair (x,y) describing the upper-left corner of the slider

        minval - The minimum value the slider can set

        maxval - The maximum value the slider can set

        defaultval - The default value of the slider

        sSurface - The surface to be rendered for the click-n-drag slider
        itself

        rSurface - The surface to be rendered representing the bounds of
        slider"""
        p = Rect(position, (rSurface.get_rect().width, sSurface.get_rect().height))
        Widget.__init__(self, p)
        self.currentval = defaultval
        self.minval = minval
        self.maxval = maxval
        self.sSurface = sSurface
        sliderx = (((self.currentval - self.minval)* self.position.width) / (self.maxval - self.minval)) - self.sSurface.get_width()/2
        self.sliderpos = Rect((sliderx + self.position.x, self.position.y),(self.sSurface.get_width(), self.sSurface.get_height()))
        self.rSurface = rSurface
        self.moveAction = False
    def handleInput(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.sliderpos.collidepoint(event.pos):
                self.moveAction = True
            else:
                self.moveAction = False
        if event.type == MOUSEMOTION and self.moveAction:
            self.sliderpos.x = event.pos[0]
            self.currentval = int(((float(self.sliderpos.x) - float(self.position.x))/float(self.position.width))*float(self.maxval))
            if self.currentval > self.maxval:
                self.currentval = self.maxval
            if self.currentval < self.minval:
                self.currentval = self.minval
        if event.type == MOUSEBUTTONUP:
            self.moveAction = False
    def draw(self, deltaT):
        drawsurface = pygame.Surface((self.position.width, self.position.height))
        #draw retainer
        drawsurface.blit(self.rSurface, (0,self.position.height/2))
        #draw slider
        sliderx = (((self.currentval - self.minval)* self.position.width) / (self.maxval - self.minval)) - self.sSurface.get_width()/2
        self.sliderpos.x = sliderx + self.position.x
        drawsurface.blit(self.sSurface, (sliderx, 0))
        return drawsurface
    def size(self):
        return self.position
    def getCurrentVal(self):
        return self.currentval
        
if __name__ == "__main__":
    from screen import Screen
    pygame.init()
    screen = Screen(640,480)
    rsurface = loadsurface("rbutton.png")
    dsurface = loadsurface("dbutton.png")
    def cb():
        print "Hello buttons!"
    position = Rect(100,100,150,50)

    btn = Button(position, rsurface, dsurface, cb)
    screen.addWidget(btn)

    font = ft.SysFont("Courier New",30)
    tb = TextBox((200,200), font, "Hello, TextBox!", (0,0,255),(0,0,0))
    screen.addWidget(tb)

    etb = EditableTextBox((300,300), font, "...", (0,0,0), (255,255,255))
    screen.addWidget(etb)

    rslider = loadsurface("rslider.png")
    sslider = loadsurface("sslider.png")
    slider = Slider((200, 400), 19, 87, 33, sslider, rslider)
    screen.addWidget(slider)

    utb = UpdatingTextBox((375, 400), font, slider.getCurrentVal)
    screen.addWidget(utb)

    while True:
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()
            screen.handleWidgetInput(i)
        screen.update(Vector2D(0,0))
        pygame.event.pump()
