'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.

Note that pyglet users should probably just add the data directory to the
pyglet.resource search path.
'''

import os
import pygame
from pygame.locals import *

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

def filepath(filename):
    '''Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    '''Open a file in the data directory.

    "mode" is passed as the second arg to open().
    '''
    return open(os.path.join(data_dir, filename), mode)

def loadsurface(filename,colorkey=-1,isSource=True):
    """Loads an image, returning a pygame surface of that image.

    filename - the name of the file in the data directory

    colorkey - the colorkey of the image. If set to -1, uses the
    top-left pixel of the image. If set to None, uses no color key. If
    set to any RGB triple, uses that RGB triple. None by default.

    isSource - When true, a flag is set to make blitting this surface
    to another surface faster. When false, this flag is not set, but
    blitting to this surface is faster. tl;dr: set to false if loading
    a background. True by default. Irrelevant if the color key is none."""
    try:
        image = pygame.image.load(filepath(filename))
    except pygame.error, message:
        print "Can't load image: " + str(message)
        exit()
    #work surface magic
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        if isSource:
            image.set_colorkey(colorkey, RLEACCEL)
        else:
            image.set_colorkey(colorkey)

    return image
