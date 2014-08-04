import pygame

class StateManager(object):
    def __init__(self):
        """Game state manager. Switches smoothly between various screens."""
        self.state = None
        self.states = {}
    def switch(self, name):
        """name should be an object registered to states with the addstate() 
        method"""
        if self.state is not None:
            self.state.switchout()
        self.state = self.states[name]
        self.state.switchin()
    def addstate(self, state, name):
        """State should be a State object, and name should be a string."""
        self.states[name] = (state)
    def retrievestate(self, name):
        return self.states[name]

class State(object):
    def __init__(self, screen):
        """Represents a game state.

        screen - a neintimes Screen object"""
        self.screen = screen
    def run(self):
        """A method that is called every frame while in this state."""
        pass
    def switchin(self):
        """A method that is called when this state becomes the current state. 
        Should do three things:
        1. Register this state's sprites with screen
        2. Register this state's widgets with screen
        3. Change the camera"""
        pygame.time.delay(100) #need a 10th of a second
        #to ensure keyboard repeat isn't fucking with
        #state switching
    def switchout(self):
        """A method that is called to cleanup when this state is no longer the
        current state. Should do two things:
        1. Unregister this state's sprites with screen
        2. Unregister this state's widgets with screen"""
        pass

statemanager = StateManager()
#yeah it's a global variable, sorry
