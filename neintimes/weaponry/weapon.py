#weapon.py

#python imports
import random

#neintimes imports
from shot import *
from route import *
from vector import *
from statuseffects import *

def nopayload():
    def p(self,target=None):
        assert(target is not None)
        pass
    return p

def effectPayload(effecttemplate):
    def p(self,target=None):
        assert(target is not None)
        applyEffect(target)
    return p
            
class Weapon:
    def __init__(self, f = None, cooldown = None):
        assert(f is not None)
        assert(cooldown is not None)
        # f is called when the weapon fires to spawn projectiles
        # f( V2D:position, float:direction, V2D:momentum, shotgroup )
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
    return claw(2,pi/3,ctime=100,cooldown=40,payload=nopayload())
    
def enemyweapon():
    return flap(cooldown=200,payload=nopayload())
    
def machinegun(payload=nopayload()):
    return jitter(speed=10.0, spread=0.1, cooldown=5, payload=payload,
               lifetime=50)

def flap(width = 60, numshots = 6, period = 700, speed = 0.4,
         cooldown = 30, image = None, payload=None):
    assert(payload is not None)
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
            s = Shot(position=p, 
                     heading=sheading,
                     image=image,
                     size=size,
                     route=route,
                     payload=payload)
            shotgroup.add(s)
    return Weapon(f, cooldown)

def arc(speed, numshots, spread, cooldown = 30, image = None,
        payload = nopayload(),lifetime=300):
    def f(position, direction, momentum, shotgroup):
        for i in floatrange(direction - spread, direction + spread, numshots):
            sheading = vectorfromangle(i, speed) + momentum
            s = Shot(position=position, heading=sheading, image=image,
                     route=advance(), payload=payload, lifetime=lifetime)
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
    
def jitter(speed, spread, cooldown = 30, image = None, payload = None, lifetime = 0):
    assert(payload is not None)
    random.seed()
    def f(position, direction, momentum, shotgroup):
        d = direction - random.uniform(-1 * spread,spread)
        sheading = vectorfromangle(d, speed) + momentum
        s = Shot(position=position, heading=sheading, image=image,
                 route=advance(), payload=payload, lifetime=lifetime)
        shotgroup.add(s)
    return Weapon(f, cooldown)

def claw(numshots, spread, dist = 300.0, ctime = 1000,
         cooldown = 30.0, image = None, payload=None):
    assert(payload is not None)
    def f(position, direction, momentum, shotgroup):
        for i in floatrange(spread, -1 * spread, numshots):
            if abs(i) > 0.0001:
                theta = abs(abs(i) - pi / 2)
                d = direction + i
                radius = dist / (2 * cos(theta))
                period = ctime * (2 * pi) / (pi - 2 * theta)
                if abs(i) > pi / 2:
                    period = ctime * (2 * pi) / (pi + 2 * theta)
                cc = counterclockwise
                if i < 0:
                    cc = clockwise
                sheading = momentum
                route = loop(radius, period, d, cc) + advance()
            else:
                route = advance()
                sheading = momentum + vectorfromangle(direction).mult(300.0/ctime)
            size = 1
            lifetime = ctime * 2
            s = Shot(position=position,
                     heading=sheading,
                     image=image,
                     size=size,
                     route=route,
                     lifetime=lifetime,
                     payload=payload)
            shotgroup.add(s)
    return Weapon(f, cooldown)



