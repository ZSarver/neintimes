from vector import pi, Vector2D
from weaponry.route import Route
from math import cos, sin

def advance():
    def f(shot):
        shot.position += shot.heading
    return Route(f)

def torpedo(angle, magnitude = .1):
    def f(shot):
        shot.heading += vectorfromangle(angle, magnitude)
    return Route(f)

def accelerate(amount = .1):
    def f(shot):
        shot.kick(shot.heading.unit.mult(amount))
    return Route(f)

CLOCKWISE = 1
COUNTERCLOCKWISE = -1
def loop(radius = 30, period = 100, angle=0, direction=CLOCKWISE):
    if direction == CLOCKWISE:
        start = angle - pi / 2
    else:
        start = angle + pi / 2
    def f(shot):
        a = 2 * pi / period * direction
        t0 = shot.age * a
        t1 = t0 + a
        dx = cos(t1 + start) - cos(t0 + start)
        dy = sin(t1 + start) - sin(t0 + start)
        shot.position += Vector2D(dx, dy).mult(radius)
    return Route(f)

def seek(sprite, acceleration = .1):
    def f(shot):
        v = sprite.position - shot.position
        magnitude = acceleration
        v = v.unit.mult(magnitude)
        shot.kick(v)
    return Route(f)

def limit(maxspeed = 20):
    def f(shot):
        shot.heading = shot.heading.crop(maxspeed)
    return Route(f)

def randroute():
    r = random.Random()
    r.seed()
    def f(shot):
        shot.kick(Vector2D(r.uniform(-1,1),r.uniform(-1,1)))
    return Route(f)
