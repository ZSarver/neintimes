#vector.py - implements vectors

from math import *

class Vector2D:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __getattr__(self, name):
        if name == 'magnitude':
            d = sqrt(self.x ** 2 + self.y ** 2)
        elif name == 'unit':
            if abs(self.magnitude) < 0.000001:
                d = Vector2D(0,0)
            else:
                d = self.mult(1.0 / self.magnitude)
        elif name == 'direction':
            d = atan2(self.y,self.x)
        else:
            raise AttributeError("Vector2D attribute not found:" + name)
        return d

#    def __setattr__(self, name, value):
#        if name == "direction":
#            self.x = self.magnitude * cos(value)
#            self.y = self.magnitude * sin(value)
#        elif name == "magnitude":
#            self.x = value * cos(self.direction)
#            self.y = value * sin(self.direction)
#        elif name == "x" or name == "y":
#            self.__dict__[name] = float(value)
#        else:
#            raise AttributeError(name + " is not a settable Vector2D attribute")

    def setdirection(self, value):
        self.x = self.magnitude * cos(float(value))
        self.y = self.magnitude * sin(float(value))
        return self

    def rotate_ip(self, value):
        c = cos(float(value))
        s = sin(float(value))
        x = self.x * c - self.y * s
        y = self.x * s + self.y * c
        self.x = x
        self.y = y
        return self

    def rotate(self, value):
        c = cos(float(value))
        s = sin(float(value))
        x = self.x * c - self.y * s
        y = self.x * s + self.y * c
        return Vector2D(x,y)

    def setmagnitude(self, value):
        self.x = float(value) * cos(self.direction)
        self.y = float(value) * sin(self.direction)
        return self

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2D(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2D(x, y)

    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y

    def crop_ip(self, m):
        if self.magnitude <= m:
            return self
        else:
            v = self.scale(m)
            self.x = v.x
            self.y = v.y
            return self

    def scale(self, m):
        return self.unit.mult(m)

    def mult(self, scalar):
        x = self.x * float(scalar)
        y = self.y * float(scalar)
        return Vector2D(x,y)
        
    def positive(self):
        return Vector2D(abs(self.x),abs(self.y))

def vectorfromangle(a,r=1):
    return Vector2D(r * cos(a),r * sin(a))

def distance(vector1, vector2):
    return sqrt((vector1.x - vector2.x)**2 + (vector1.y - vector2.y)**2)

def up():
    return vectorfromangle(3 * pi / 2)

def right():
    return vectorfromangle(0)

def left():
    return vectorfromangle(pi)

def down():
    return vectorfromangle(pi / 2)

