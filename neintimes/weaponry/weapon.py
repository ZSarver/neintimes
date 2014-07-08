#weapon.py

from shot import *
from route import *
from vector import *

class Weapon:
    def __init__(self, f, cooldown = 0):
        self.func = f
        self.delay = 0
        self.cooldown = cooldown

    def cool(self):
        self.delay -= 1
        if self.delay <= 0:
            self.delay = 0

    def canfire(self):
        if self.delay == 0:
            return True
        else:
            return False

    def fire(self, position, direction, momentum, shotgroup):
        if self.canfire():
            self.func(position, direction, momentum, shotgroup)
            self.delay += self.cooldown
            return True
        else:
            return False

def testweapon():
    return arc(7, 8, pi / 6)

def flap(width = 60, numshots = 6, period = 700, speed = 0.4, cooldown = 30, image = None):
    def f(position, direction, momentum, shotgroup):
        for i in floatrange(width, width * -1, numshots):
            z = vectorfromangle(direction + pi /2, i)
            p = position + z
            sheading = vectorfromangle(direction, speed) + momentum
            size = 1
            if i > 0:
                c = counterclockwise
            else:
                c = clockwise
            route = loop(abs(i), period, direction, c) + advance()
            s = Shot(p, sheading, image, size, route)
            shotgroup.add(s)
    return Weapon(f, cooldown)

def arc(speed, numshots, spread, cooldown = 30, image = None):
    def f(position, direction, momentum, shotgroup):
        for i in floatrange(direction - spread, direction + spread, numshots):
            sheading = vectorfromangle(i, speed) + momentum
            s = Shot(position, sheading, image)
            shotgroup.add(s)
    return Weapon(f, cooldown)

def arc2(speed, numshots, spread, cooldown = 30, image = None):
    def f(position, direction, momentum, shotgroup):
        for i in floatrange(direction - spread, direction + spread, numshots):
            sheading = vectorfromangle(i, speed * -1)
            route = torpedo(i, 0.001) + limit() + advance()
            size = 1
            s = Shot(position, sheading, image, size, route)
            s.kick(momentum)
            shotgroup.add(s)
    return Weapon(f, cooldown)

def arc3(speed, numshots, spread, cooldown = 30, image = None):
    def f(position, direction, momentum, shotgroup):
        for i in floatrange(direction - spread, direction + spread, numshots):
            sheading = vectorfromangle(i, speed * -1)
            route = torpedo(direction, 0.1) + limit() + advance()
            size = 1
            s = Shot(position, sheading, image, size, route)
            s.kick(momentum)
            shotgroup.add(s)
    return Weapon(f, cooldown)

def claw(numshots, spread, dist = 300.0, ctime = 1000, cooldown = 30.0, image = None):
    def f(position, direction, momentum, shotgroup):
        for i in floatrange(spread, -1 * spread, numshots):
            theta = abs(abs(i) - pi / 2)
            d = direction + i
            sheading = momentum
            size = 1
            radius = dist / (2 * cos(theta))
            period = ctime * (2 * pi) / (pi - 2 * theta)
            if abs(i) > pi / 2:
                period = ctime * (2 * pi) / (pi + 2 * theta)
            cc = counterclockwise
            if i < 0:
                cc = clockwise
            route = loop(radius, period, d, cc) + advance()
            lifetime = ctime * 2
            s = Shot(position, sheading, image, size, route, lifetime)
            shotgroup.add(s)
    return Weapon(f, cooldown)



