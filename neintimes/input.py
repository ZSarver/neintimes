import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_x, K_TAB
from vector import Vector2D


[playerThrust, playerReverse, playerStrafe, playerLeft, playerRight, 
playerBoost, playerShoot, changeState] = range(8)

keyBinding = {}
keyBinding[playerThrust] = K_UP
keyBinding[playerReverse] = K_DOWN
keyBinding[playerStrafe] = K_z
keyBinding[playerLeft] = K_LEFT
keyBinding[playerRight] = K_RIGHT
keyBinding[playerBoost] = K_x
keyBinding[playerShoot] = K_z
keyBinding[changeState] = K_TAB

def getInputActions():
    keylist = pygame.key.get_pressed()
    actions = []
    up = 1
    down = -1
    right = 1
    left = -1
    rotation = 0
    vthrust = 0
    hthrust = 0

    if keylist[keyBinding[playerReverse]]:
        vthrust += down
    if keylist[keyBinding[playerThrust]]:
        vthrust += up
    if keylist[keyBinding[playerLeft]]:
        rotation += left
    if keylist[keyBinding[playerRight]]:
        rotation += right
    if keylist[keyBinding[playerStrafe]]:
        hthrust = rotation
        rotation = 0
    if keylist[keyBinding[changeState]]:
        cs = True
    else:
        cs = False
    if vthrust is 0 and hthrust is 0:
        thrust = False
        thrustDirection = Vector2D(0,0)
    else:
        thrust = True
        thrustDirection = Vector2D(vthrust, hthrust).unit
    if keylist[keyBinding[playerBoost]]:
        boost = True
    else:
        boost = False
    if keylist[keyBinding[playerShoot]]:
        shooting = True
    else:
        shooting = False

    return (thrustDirection, boost, rotation, shooting, cs)
