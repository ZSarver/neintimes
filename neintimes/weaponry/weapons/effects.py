from weaponry import *

    
def testEffect():
    def f(e, *args):
        e.target.shoot()
        return args
    def end(e):
        print "ended!"
    def start(e):
        print "started!"
    onApply = start
    onEnd = end
    onUpdate = f
    lifetime = 1000
    t = StatusEffectTemplate(lifetime, onApply, onUpdate, onEnd)
    return t
