from weaponry import *

def nopayload():
    def p(self,target=None):
        assert(target is not None)
        pass
    return p

def effectPayload(effecttemplate):
    def p(self,target=None):
        assert(target is not None)
        statuseffects.applyEffect(target)
    return p
