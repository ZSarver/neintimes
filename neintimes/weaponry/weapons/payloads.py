from weaponry import *

def nopayload():
    def p(self,target=None):
        assert(target is not None)
        pass
    return p

def effectPayload(effecttemplate):
    def p(self,target=None):
        assert(target is not None)
        statuseffects.applyEffect(target, source, effecttemplate)
    return p
    
def knockbackPayload(source,knockstrength=0,knockrotation=0):
    def p(self,target=None):
        assert(target is not None)
        knockdir = self.heading.direction + knockrotation
        knockvector = vectorfromangle(knockdir, r=knockstrength)
        e = knockbackEffect(knockvector)
        statuseffects.applyEffect(target, source, e)
    return p
