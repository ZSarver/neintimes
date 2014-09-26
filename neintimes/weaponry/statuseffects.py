class StatusEffectTemplate:
    def __init__(self, lifetime, onApply, onUpdate, onEnd):
        self.lifetime = lifetime # effect duration
        self.onUpdate = onUpdate # called every round
        #function(effect, [update args])
        #returns a new list of [update args] ?
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
    
    def update(self, effectIndex=None, *args):
        #this is called by the target's update() method
        assert(effectIndex is not None)
        self.age += 1
        if self.age > self.lifetime:
            self.removeEffect(effectIndex)
        newargs = self.onUpdate(self, *args)
        return newargs

    def removeEffect(self,index):
        self.target.removeEffect(index)
        self.onEnd()
    
def applyEffect(target, source, effectTemplate):
    s = StatusEffect(target, source, effectTemplate)
    target.addEffect(s)
    effectTemplate.onApply(s)
