class UpdateHook:
    def __init__(self, target, function, nextHook, prevHook=None):
        self.target = target
        self.function = function
        self.nextHook = nextHook
        self.prevHook = prevHook

    def removeHook(self):
        if self.prevHook is None:
            self.target.update = self.nextHook
            if isHook(self.nextHook):
                self.nextHook.prevHook = None
        else:
            self.prevHook.nextHook = self.nextHook
            if isHook(self.nextHook):
                self.nextHook.prevHook = self.prevHook

    def __call__(self, *args):
        newargs = self.function(*args)
        self.nextHook(*newargs)
        
def isHook(f):
    return hasattr(f, "function")

def addUpdateHook(target, function):
    if isHook(target.update):
        nextHook = target.update.nextHook
        prevHook = target.update
        f = UpdateHook(target, function, nextHook, prevHook)
        prevHook.nextHook = f
        if isHook(nextHook):
            nextHook.prevHook = f
    else:
        nextHook = target.update
        prevHook = None
        f = UpdateHook(target, function, nextHook, prevHook)
        target.update = f
    return f

class StatusEffectTemplate:
    def __init__(self, lifetime, onApply, onUpdate, onEnd):
        self.lifetime = lifetime # effect duration
        self.onUpdate = onUpdate # called every round
        #function(effect, [update args])
        #returns a new list of [update args]
        self.onApply = onApply # function to call when effect starts
        #onApply(effect)
        self.onEnd = onEnd # function to call when effect ends
        #onEnd(effect)

class StatusEffect:
    def __init__(self, target, source, template):
        self.age = 0
        self.target = target
        self.source = source
        self.hook = None
        self.lifetime = template.lifetime
        self.onUpdate = template.onUpdate
        self.onEnd = template.onEnd
            
    def __call__(self, *args): 
    #this is hooked into the target's update() method
        self.age += 1
        if self.age > self.lifetime:
            self.removeEffect()
        newargs = self.onUpdate(self, *args)
        return newargs

    def removeEffect(self):
        self.hook.removeHook()
        self.onEnd(self)
    
def applyEffect(target, source, effectTemplate):
    s = StatusEffect(target, source, effectTemplate)
    s.hook = addUpdateHook(target, s)
    effectTemplate.onApply(s)
    
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
