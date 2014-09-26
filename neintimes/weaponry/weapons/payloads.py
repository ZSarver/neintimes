#payloads.py

from weaponry.statuseffects import applyEffect
from vector import vectorfromangle

def noPayload():
    def p(self,target=None):
        assert(target is not None)
        pass
    return p

def effectPayload(effecttemplate):
    def p(self,target=None):
        assert(target is not None)
        applyEffect(target, source, effecttemplate)
    return p
    
def knockbackPayload(source,knockstrength=0,knockrotation=0):
    def p(self,target=None):
        assert(target is not None)
        knockdir = self.heading.direction + knockrotation
        knockvector = vectorfromangle(knockdir, r=knockstrength)
        e = knockbackEffect(knockvector)
        applyEffect(target, source, e)
    return p

def killPayload(self, target=None):
    assert(target is not None)
    target.killshot()
