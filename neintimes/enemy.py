from boid import Boid
from anchor import Anchor
from flock import Flock
               
def spawnEnemy(position, angle, behavior, formation, image, aimage, target):
    enemygroup = Flock(1.2, formation)
    anchor = Anchor(position, aimage, behavior, target)
    for slot in formation:
        p = position + slot.spatialOffset.rotate(angle) 
        a = angle + slot.angularOffset
        w = slot.weapon
        b = Boid(position=p, aim=a, image=image, weap=w)
        enemygroup.addSquad(b)
    enemygroup.addAnchor(anchor)
    return enemygroup


def defaultBehavior(myanchor):
	goalvector = myanchor.target.position - myanchor.position
	myanchor.aim = goalvector.direction
	myanchor.propel(goalvector, 4)
	myanchor.shoot()
