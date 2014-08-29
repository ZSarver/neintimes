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

def knockbackEffect(vector):
    def onUpdate(e, *args):
        return args
    def onEnd(e):
        pass
    def onApply(e)
        e.target.propel(vector)
    lifetime = 0
    t = StatusEffectTemplate(lifetime, onApply, onUpdate, onEnd)
    return t
