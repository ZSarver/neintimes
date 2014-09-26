#screen.py implements drawing things on the screen.

#pygame imports
import pygame
import pygame.font as ft

#neintimes imports
from vector import Vector2D
from camera import constant
from stars import Starlayers
from gui import UpdatingTextBox

screenwidth = 640
screenheight = 480
_debug = True

class Screen:
    def __init__(self, x=screenwidth, y=screenheight, cam=None):
        self.x = x
        self.y = y

        self.displaysurface = pygame.display.set_mode((x,y))
        self.background = pygame.Surface(self.displaysurface.get_size()).convert()
        self.background.fill((0,0,0))
#        bgblock = makebgblock(0,0)
#        self.background.blit(bgblock,(0,0))
        self.displaysurface.blit(self.background,(0,0))
        pygame.display.flip()
        self.referenceLists = []
        self.offset = Vector2D(0,0)
        depths = [15.0 / (15 - d) for d in range(10)]
        shades = [255 - (20 * d) for d in range(10)]
        colors = [pygame.Color(s, s, s, 0) for s in shades]
        density = (0,8)
        self.stars = Starlayers((x,y), depths, colors, density)
        if cam == None:
            self.cam = constant(Vector2D(0,0))
        else:
            self.cam = cam
        self.widgets = []
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.deltaT = 0

        if _debug:
            font = ft.SysFont("Courier New", 30)
            self.framerate = UpdatingTextBox((10,10), font, self.clock.get_fps, (255,255,255), (0,0,0))
            self.addWidget(self.framerate)
            print "Debug!"

    def update(self, playerpos):
        self.deltaT = self.clock.tick(60) #tick! limit to 60fps
        self.clear() #remove sprites at old locations
        self.cam.go(self, playerpos)
        self.place() #move sprites rects to current sprite positions
        self.draw()
        pygame.display.flip()

    def clear(self):
        for rl in self.referenceLists:
            for ref in rl:
                ref.clear(self.displaysurface, self.background)
        self.stars.undraw(self.displaysurface)
        for w in self.widgets:
            self.displaysurface.blit(self.background, w.size())

    def place(self):
        #positions the sprite rects for group
        for rl in self.referenceLists:
            for ref in rl:
                ref.place(self.offset)
        self.stars.update((self.offset.x, self.offset.y))

    def draw(self):
        self.stars.draw(self.displaysurface,(self.offset.x, self.offset.y))
        for rl in self.referenceLists:
            for ref in rl:
                ref.draw(self.displaysurface)
        for w in self.widgets:
            self.displaysurface.blit(pygame.Surface.convert(w.draw(self.deltaT)),w.position)

    def add(self, reflist):
        #this group will be drawn to the screen
        self.referenceLists.append(reflist)

    def remove(self, reflist):
        #this group will no longer be draw to the screen
        self.referenceLists.remove(reflist)

    def center(self, place = Vector2D(0,0)):
        #centers the screen at this position
        self.offset = place - Vector2D(640 / 2, 480 / 2)

    def addWidget(self, widget):
        """Adds a gui widget to be tracked by Screen."""
        self.widgets.append(widget)

    def removeWidget(self, widget):
        """Removes a gui widget from being tracked."""
        self.widgets.remove(widget)

    def handleWidgetInput(self, event):
        for w in self.widgets:
            w.handleInput(event)
