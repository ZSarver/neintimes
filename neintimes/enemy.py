from boid import *
from formation import *

#~ class enemy():
    #~ def __init__(self, position, behavior=None):
        #~ self.position = Vector2D(0,0)
        #~ self.momentum = Vector2D(0,0)
        #~ self.squad = None
        #~ if behavior is None:
            #~ self.behavior = defaultBehavior
               
def spawnEnemy(screen, position, angle, behavior, formation, image):
    enemygroup = flock (1.2, 0, formation)
    anchor = enemy(position, angle, behavior)
    for slot in formation:
        p = position + slot.spatialOffset.rotate(angle) 
        a = angle + slot.angularOffset
        w = slot.weapon
        b = Boid(position=p, angle=a, weapon=w, image=image)
        enemygroup.addSquad(b)
    enemygroup.addAnchor(anchor)
    screen.add(enemygroup)
    return enemygroup


def defaultBehavior(self, target):
    goalvector = target.anchor.position - self.position
    self.aim = goalvector.angle
    self.propel(goalvector, self.baseSpeed)

