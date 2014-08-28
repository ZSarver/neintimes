from boid import *
from formation import *
from anchor import Anchor
from flock import Flock
from weaponry import *

#~ class enemy():
    #~ def __init__(self, position, behavior=None):
        #~ self.position = Vector2D(0,0)
        #~ self.momentum = Vector2D(0,0)
        #~ self.squad = None
        #~ if behavior is None:
            #~ self.behavior = defaultBehavior
               
def spawnEnemy(position, angle, behavior, formation, image, aimage, target):
    enemygroup = Flock(1.2, formation)
    anchor = Anchor(position, aimage, behavior, target)
    for slot in formation:
        p = position + slot.spatialOffset.rotate(angle) 
        a = angle + slot.angularOffset
        w = slot.weapon
        b = Boid(position=p, aim=a, image=image)
        enemygroup.addSquad(b)
    enemygroup.addAnchor(anchor)
    return enemygroup


def defaultBehavior(myanchor):
	goalvector = myanchor.target.position - myanchor.position
	myanchor.aim = goalvector.direction
	myanchor.propel(goalvector, 4)
	myanchor.shoot()
