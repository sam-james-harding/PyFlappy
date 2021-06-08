# imports
import pygame; pygame.init()
import pygame.mixer as pm; pm.init()
import pygame.font as pf; pf.init()
import os; work_dir = os.path.dirname(__file__) + '/'
import random
import time
import json

import pygamekeyboard as pk

#setup variables/objects
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("PyFlappy 2")
clock = pygame.time.Clock()
newHighScore = 0

#save file functions
def saveFileGet(n):
    with open(work_dir+'resources/highScores.json') as f:
        saveFile = json.load(f)
    return saveFile[str(n)]

def saveFileSet(n, val):
    with open(work_dir+'resources/highScores.json') as f:
        saveFile = json.load(f)
    saveFile[str(n)] =  val
    with open(work_dir+'resources/highScores.json', 'w') as f:
        json.dump(saveFile,f)

def insertScore(name, score):
    highscores = []
    for i in range(1,6):
        try: highscores.append(saveFileGet(i))
        except: break

    if len(highscores) == 0: highscores = [(name,score)]
    else:
        for i in range(len(highscores)):
            if score > highscores[i][1]:
                highscores.insert(i, (name, score))
                break
        if score <= highscores[len(highscores)-1][1]:
            highscores.append((name,score))
    
    for i in range(5):
        try:
            saveFileSet(i+1, highscores[i])
        except: break

def getLowestScore():
    highscores = []
    for i in range(1,6):
        try: highscores.append(saveFileGet(i))
        except: break
    if highscores == []: return 0
    else: return highscores[-1][1]

def lessThanFiveScores():
    highscores = []
    for i in range(1,6):
        try: highscores.append(saveFileGet(i))
        except: break

    if len(highscores) < 5:
        return True
    return False

def getScoresList():
    highscores = []
    for i in range(1,6):
        try: highscores.append(saveFileGet(i))
        except: break
    return highscores

def saveFileClear():
    with open(work_dir+'resources/highScores.json', 'w') as f:
        json.dump(dict(),f)

#loading save file

'''Sprites and Images'''

#bird sprite
class Bird(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.baseImage = image
        self.image = image

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(image)

        self.paused = False

        #gravity and jumping settings
        self.velocity = 0
        self.gravity = 0.7
        self.jumpVelocity = -12
        self.terminalVelocity = 30

        #rotation settings
        self.jumpRotation = 45
        self.minRotation = -90
        self.rotationRate = -2  #must be negative int
        self.rotation = 0

        #pre-loading rotations
        self.spriteAngles = dict()
        self.spriteAngleMasks = dict()

        for i in range(self.minRotation, self.jumpRotation+1):
            self.spriteAngles[i] = pygame.transform.rotate(self.baseImage, i)
            self.spriteAngleMasks[i] = pygame.mask.from_surface(self.spriteAngles[i])

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.paused: return

        if self.velocity < self.terminalVelocity:
            self.velocity += self.gravity
        self.rect.y += int(self.velocity)
        self.changeRotatation(self.rotationRate)

        self.rect.clamp_ip(screen.get_rect())

    def jump(self):
        if self.paused: return
        
        self.velocity = self.jumpVelocity
        self.setRotation(self.jumpRotation)

    def changeRotatation(self, angle):
        self.rotation += angle
        if self.rotation >= self.minRotation: 
            self.image = self.spriteAngles[self.rotation]
            self.mask = self.spriteAngleMasks[self.rotation]

    def setRotation(self, angle):
        self.rotation = angle
        self.image = self.spriteAngles[self.rotation]
        self.mask = self.spriteAngleMasks[self.rotation]

    def pause(self): self.paused = True

    def unpause(self): self.paused = False

birdImage = pygame.transform.scale(
    pygame.image.load(work_dir + 'resources/bird.png').convert_alpha(),
    (80,60))
bird = Bird(birdImage)

#pipe sprites
pipes = pygame.sprite.Group()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, image, dimensions, screenDimensions, isUpsideDown, *groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.baseImage = image
        self.image = pygame.transform.rotate (
            pygame.transform.scale(image, dimensions),
            isUpsideDown * 180)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        if isUpsideDown:
            self.rect.y = 0
        else:
            self.rect.y = screenDimensions[1] - dimensions[1]

        self.rect.x = screenDimensions[0]

    def obliterate(self):
        self.kill()
        del self

pipeImage = pygame.image.load(work_dir + 'resources/pipe.png').convert_alpha()

backgroundImage = pygame.image.load(work_dir + 'resources/background.png').convert_alpha()

titleImage = pygame.transform.scale(
    pygame.image.load(work_dir + 'resources/title.png').convert_alpha(),
    (420,96))

backSymbol = pygame.transform.scale(
    pygame.image.load(work_dir + 'resources/backSymbol.png').convert_alpha(),
    (90,90))


resetSymbol = pygame.transform.scale(
    pygame.image.load(work_dir + 'resources/resetSymbol.png').convert_alpha(),
    (90,90))

#sounds
splatSound = pygame.mixer.Sound(work_dir+"resources/splat.wav")

'''Functions'''
def collideWithFirstTwo(sprite, group):
    if pygame.sprite.collide_mask(sprite, group.sprites()[0]): return True
    if pygame.sprite.collide_mask(sprite, group.sprites()[1]): return True
    return False

'''Screens'''
#base screen class
class Screen():
    def __init__(self, screen, clock, backgroundColour):
        self.done = False
        self.screen = screen
        self.clock = clock
        self.backgroundColour = backgroundColour

    def Input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def Update(self):
        pass

    def Render(self):
        pass

    def RenderBase(self):
        if self.done: return
        self.screen.fill(self.backgroundColour)
        self.Render()
        pygame.display.flip()
        self.clock.tick(60)

    def Play(self):
        self.__init__(self.screen, self.clock, self.backgroundColour)
        while not self.done:
            self.Input()
            self.Update()
            self.RenderBase()

#screen classes
class Menu(Screen):
    def __init__(self, screen, clock, backgroundColour, startMusic = False):
        super().__init__(screen, clock, backgroundColour)

        self.ground = pygame.Surface((800, 10)); self.ground.fill((139,69,19))

        self.buttonFont = pygame.font.SysFont('Impact', 80)

        #button rects
        self.startButton = pygame.Rect((0,150),(400,100))
        self.scoreButton = pygame.Rect((0,300),(400,100))
        self.quitButton = pygame.Rect((0,450),(400,100))

        #text surfaces
        self.startText = self.buttonFont.render("Start Game", True, (255,255,255))
        self.scoreText = self.buttonFont.render("High Scores", True, (255,255,255))
        self.quitText = self.buttonFont.render("Quit Game", True, (255,255,255))

        #text coordinates
        self.startTextY = (150+(50-(self.startText.get_height()//2)))
        self.startTextX = 200-(self.startText.get_width()//2)

        self.scoreTextY = (300+(50-(self.scoreText.get_height()//2)))
        self.scoreTextX = 200-(self.scoreText.get_width()//2)

        self.quitTextY = (450+(50-(self.quitText.get_height()//2)))
        self.quitTextX = 200-(self.quitText.get_width()//2)

        #music
        if startMusic == True:
            pygame.mixer.music.load(work_dir + "resources/menutrack.mp3")
            pygame.mixer.music.play(-1)
    
    def Input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = event.pos
                if self.startButton.collidepoint(coord):
                    self.done=True
                    Game(screen, clock, (255,255,255)).Play()
                elif self.quitButton.collidepoint(coord):
                    self.done=True
                if self.scoreButton.collidepoint(coord):
                    self.done=True
                    HighScores(screen, clock, (255,255,255)).Play()


    def Update(self):
        pass

    def Render(self):
        #background
        self.screen.blit(backgroundImage, (0,0))
        self.screen.blit(self.ground, (0,590))

        #buttons
        pygame.draw.rect(self.screen, (0,200,0), self.startButton)
        pygame.draw.rect(self.screen, (200,200,0), self.scoreButton)
        pygame.draw.rect(self.screen, (200,0,0), self.quitButton)

        #title
        self.screen.blit(titleImage, (190,20))

        #render button text
        screen.blit(self.startText, (self.startTextX, self.startTextY))
        screen.blit(self.scoreText, (self.scoreTextX, self.scoreTextY))
        screen.blit(self.quitText, (self.quitTextX, self.quitTextY))

class Game(Screen):
    def __init__(self, screen, clock, backgroundColour):
        super().__init__(screen, clock, backgroundColour)
        bird.rect.x = 100
        bird.rect.y = 100

        self.pipeVerticalGap = 100
        self.pipeHorizontalGap = 400
        self.minPipeHeight = 100
        self.pipeSpeed = 9
        self.pipeWidth = 100

        self.pipePassedBird = False
        self.birdDead = False
        self.score = 0

        self.distanceSinceLastPipe = self.pipeHorizontalGap

        self.scoreFont = pygame.font.SysFont('Arial', 80, bold=True)

        #resetting previous events
        bird.unpause()
        for pipe in pipes: pipe.obliterate()
        bird.velocity = 0
        bird.rotation = 0

        #create surfaces
        self.ground = pygame.Surface((800, 10)); self.ground.fill((139,69,19))

        #music
        pygame.mixer.music.load(work_dir + "resources/theme.mp3")
        pygame.mixer.music.play(-1)
    
    def Input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.birdDead:
                bird.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.birdDead:
                bird.jump()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                self.createPipes(random.randint(self.minPipeHeight, 600-self.minPipeHeight-self.pipeVerticalGap), 
                self.pipeVerticalGap)

    def Update(self):
        bird.update()

        #updates for all pipes
        for pipe in pipes.sprites(): 
            pipe.rect.x -= self.pipeSpeed # moves pipes forward

            if pipe.rect.x < -100:
                pipe.obliterate()
                self.pipePassedBird = False

        #checking whether to add new pipes based on distance since last pipe
        self.distanceSinceLastPipe += self.pipeSpeed

        if self.distanceSinceLastPipe >= self.pipeHorizontalGap:
            self.distanceSinceLastPipe = 0
            self.createPipes(random.randint(self.minPipeHeight, 600-self.minPipeHeight-self.pipeVerticalGap), 
                self.pipeVerticalGap)

        #detect collisions
        if collideWithFirstTwo(bird, pipes) and not self.birdDead:
            self.pipeSpeed=0
            bird.velocity = 0
            self.birdDead = True
            pygame.mixer.music.stop()

        #scoring
        if pipes.sprites()[0].rect.x + self.pipeWidth < 100 and not self.pipePassedBird:
            self.pipePassedBird = True
            self.score += 1

        #detect hitting the ground
        if bird.rect.y >= 540:
            self.birdDead = True
            pygame.mixer.music.stop()
            splatSound.play()
            time.sleep(0.5)
            self.done = True
            if self.score > getLowestScore() or (lessThanFiveScores() and self.score > 0):
                #getting name for new highscore
                global newHighScore
                newHighScore = self.score
                NewHighScore(screen, clock, (255,255,255)).Play()
            else:
                Menu(screen, clock, (255,255,255), startMusic=True).Play()


    def Render(self):
        self.screen.blit(backgroundImage, (0,0))
        pipes.draw(self.screen)
        bird.draw(self.screen)
        self.screen.blit(self.ground, (0,590))

        #blit score
        textSurf = self.scoreFont.render(str(self.score), True, (200,0,0))
        self.screen.blit(textSurf, (10,0))

    def createPipes(self, topPipeHeight, pipeGap):
        Pipe(pipeImage, (self.pipeWidth, topPipeHeight), (800, 600), True, pipes)
        Pipe(pipeImage, (self.pipeWidth, 600-topPipeHeight-pipeGap), (800,600), False, pipes)

class HighScores(Screen):
    def __init__(self, screen, clock, backgroundColour):
        super().__init__(screen, clock, backgroundColour)

        self.ground = pygame.Surface((800, 10)); self.ground.fill((139,69,19))
        self.backButton = pygame.Rect((10,10), (110,110))

        self.resetButton = pygame.Rect((680,10), (110,110))

        self.textFont = pygame.font.SysFont('Arial', 60)

        self.titleFont = pygame.font.SysFont('Arial', 80, bold=True)
        self.title = self.titleFont.render("High Scores", True, (0,0,0))
        self.titleX = 400 - self.title.get_width()//2
        self.titleY = 65 -self.title.get_height()//2

        self.highscoreTextSurfs = []
        for highscore in getScoresList():
            text = highscore[0] + ' - ' + str(highscore[1])
            self.highscoreTextSurfs.append(
                self.textFont.render(text, True, (0,0,0))
            )

        if self.highscoreTextSurfs == []:
            self.highscoreTextSurfs = [self.textFont.render("No High Scores", True, (0,0,0))]


    def Input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = event.pos

                if self.backButton.collidepoint(coords):
                    self.done = True
                    Menu(screen, clock, (255,255,255)).Play()

                elif self.resetButton.collidepoint(coords):
                    saveFileClear()
                    self.highscoreTextSurfs = [self.textFont.render("No High Scores", True, (0,0,0))]


    def Update(self):
        pass

    def Render(self):
        #background
        self.screen.blit(backgroundImage, (0,0))
        self.screen.blit(self.ground, (0,590))

        pygame.draw.rect(self.screen, (255,255,255), self.backButton)
        screen.blit(backSymbol, (20,20))

        pygame.draw.rect(self.screen, (255,50,50), self.resetButton)
        screen.blit(resetSymbol, (690,20))

        self.screen.blit(self.title, (self.titleX, self.titleY))

        #rendering high scores
        currentY = 150

        for highscore in self.highscoreTextSurfs:
            textX = 400-highscore.get_width()//2
            self.screen.blit(highscore, (textX, currentY))
            currentY += 60

class NewHighScore(Screen):
    def __init__(self, screen, clock, backgroundColour):
        super().__init__(screen, clock, backgroundColour)

        self.ground = pygame.Surface((800, 10)); self.ground.fill((139,69,19))

        self.textFont = pygame.font.SysFont('Arial', 40, bold=False)
        self.titleFont = pygame.font.SysFont('Arial', 60, bold=True)

        self.title = self.titleFont.render("Enter New Highscore Name", True, (0,0,0))
        self.titleX = 400 - self.title.get_width()//2

        self.textFieldBackground = pygame.Surface((420, 46)); self.textFieldBackground.fill((255,255,255))
        self.textFieldBackgroundOutline = pygame.Surface((430, 56)); self.textFieldBackgroundOutline.fill((0,0,0))

        self.keyboard = pk.PGkeyboard(keySize=50, keySpacing=5, coords=(122,180))
        self.textField = pk.EditablePGText(self.textFont, 400)

        self.submitButton = pygame.Rect((250,450), (300, 80))
        self.submitButtonText = self.titleFont.render("Submit", True, (255,255,255))

        self.submitButtonTextX = 150 - self.submitButtonText.get_width()//2 + 250

    def Input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = event.pos
                self.textField.passChar(self.keyboard.getClickedKey(coords))

                #submitting score with name
                if self.submitButton.collidepoint(coords) and self.textField.get() != '':
                    global newHighScore
                    self.done = True
                    insertScore(self.textField.get(), newHighScore)
                    Menu(screen, clock, (255,255,255), startMusic=True).Play()
                    

    def Update(self):
        pass

    def Render(self):
        #background
        self.screen.blit(backgroundImage, (0,0))
        self.screen.blit(self.ground, (0,590))

        #title
        self.screen.blit(self.title, (self.titleX,0))

        #text field background
        self.screen.blit(self.textFieldBackgroundOutline, (185,100))
        self.screen.blit(self.textFieldBackground, (190,105))

        #text field
        self.textField.render(self.screen, (200, 103))

        #keyboard
        self.keyboard.render(self.screen)

        #submit button
        pygame.draw.rect(self.screen, (255,165,0), self.submitButton)
        self.screen.blit(self.submitButtonText, (self.submitButtonTextX,455))

Menu(screen, clock, (255,255,255), startMusic=True).Play()
pygame.quit()