import pygame

class Screen():
    def Initialize(self):
        '''Inherit to add additional initialization.'''
        pass

    def Input(self):
        '''Inherit to add input management'''
        pass

    def Update(self):
        '''Inherit to add frame updates'''
        pass

    def Render(self):
        '''Inherit to add rendering.'''
        pass
    
    def __init__(self, screen, clock):
        '''
        Initialiser - do not inherit this method.
        Takes a screen object, clock object, and 
        background colour rgb tuple as arguments.
        '''
        self.screen = screen
        self.clock = clock

        self.done = False
        self.eventReactions = {pygame.QUIT: self.end}
        self.deltaTime = 0

        self.Initialize()

    def end(self, *event):
        '''Do not inherit. Use this function to stop the screen.'''
        self.done = True

    def addEventReaction(self, eventType, func):
        '''Do not inherit. Takes a pygame event type and a function
        as an argument - the function will be called if the event occurs,
        and will be passed the event as the first argument'''
        self.eventReactions[eventType] = func

    def InputBase(self):
        '''Private - do not inherit'''
        for event in pygame.event.get():
            command = self.eventReactions.get(event.type, lambda e:None)
            command(event)

        self.Input()

    def RenderBase(self):
        '''Private - do not inherit'''
        if self.done: return
        self.Render()
        pygame.display.flip()
        self.clock.tick(60)

    def Play(self):
        '''Do not inherit. Call this to play the screen.'''
        self.__init__(self.screen, self.clock)
        while not self.done:
            self.InputBase()
            self.Update()
            self.RenderBase()
            self.deltaTime = self.clock.get_time()