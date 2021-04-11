import pygame
pygame.init()

class PGKey():
    def __init__(self, char, shiftchar, coords, font, keyColour, textColour, keySize):
        self.keyColour = keyColour
        self.textColour =textColour
        self.keySize = keySize
        self.char = char
        self.shiftchar = shiftchar

        self.shiftOn = False

        self.surface = pygame.Surface((self.keySize, self.keySize))
        self.surface.fill(self.keyColour)

        self.rect = pygame.Rect(coords, (self.keySize, self.keySize))

        self.textSurf = font.render(self.char, True, self.textColour)
        self.shiftTextSurf = font.render(self.shiftchar, True, self.textColour)

    def shift(self):
        self.shiftOn = not self.shiftOn

    def render(self, screen):
        if self.shiftOn: textToBlit = self.shiftTextSurf
        else: textToBlit = self.textSurf

        screen.blit(self.surface, self.rect)

        letterXPos = self.rect.x - textToBlit.get_width()//2 + self.keySize//2
        letterYPos = self.rect.y

        screen.blit(textToBlit, (letterXPos, letterYPos))

    def clicked(self, coords):
        if self.rect.collidepoint(coords): return True
        return False

    def get(self):
        if self.shiftOn: return self.shiftchar
        else: return self.char

class PGkeyboard():
    def __init__(self, keyColour=(200,200,200), textColour=(0,0,0), keySize = 30, keySpacing = 4, coords=(0,0), backgroundColour = (150,150,150)):
        self.keyColour = keyColour
        self.textColour = textColour
        self.keySize = keySize
        self.keySpacing = keySpacing
        self.coords = coords

        self.chars = ['1','2','3','4','5','6','7','8','9','0',
                    'a','b','c','d','e','f','g','h','i','j',
                    'k','l','m','n','o','p','q','r','s','t',
                    'u','v','w','x','y','z',' ','<','/\\', 'Cl']

        self.shiftChars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                        'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '<', '\\/', 'Cl']

        self.font = pygame.font.SysFont("Helvetica", keySize)

        #creating background
        backgroundWidth = 10*keySize + 11*keySpacing
        backgroundHeight = 4*keySize + 5*keySpacing
        self.backgroundSurf = pygame.Surface((backgroundWidth, backgroundHeight))
        self.backgroundSurf.fill(backgroundColour)

        #creating all keys
        self.keys = []
        currentX = coords[0] + keySpacing
        currentY = coords[1] + keySpacing
        currentCharIndex = 0

        for i in range(4):
            for j in range(10):
                self.keys.append(
                PGKey(self.chars[currentCharIndex],
                self.shiftChars[currentCharIndex],
                (currentX, currentY),
                self.font,
                self.keyColour,
                self.textColour,
                self.keySize))

                currentX += self.keySize + self.keySpacing
                currentCharIndex += 1
            
            currentY += self.keySize + self.keySpacing
            currentX = coords[0] + self.keySpacing

    def render(self, screen):
        screen.blit(self.backgroundSurf, self.coords)
        for key in self.keys:
            key.render(screen)

    def getClickedKey(self, coords):
        for key in self.keys:
            if key.clicked(coords):
                if key.get() in ('/\\', '\\/'):
                    for key in self.keys: key.shift()
                    return ''
                return key.get()

        return ''

class EditablePGText():
    def __init__(self, font, maxWidth, defaultText='', colour=(0,0,0), backSpaceChar='<', clearChar='Cl'):
        self.font = font
        self.colour = colour
        self.maxWidth = maxWidth

        self.backSpaceChar = backSpaceChar
        self.clearChar = clearChar

        self.text = list(defaultText)
        self.textSurf = self.font.render(defaultText, True, self.colour)

    def render(self, screen, coords):
        screen.blit(self.textSurf, coords)

    def passChar(self, char):
        if char == self.backSpaceChar:
            if self.text != []: self.text.pop()
        elif char == self.clearChar:
            self.text = []
        elif char == '': return
        else: self.text.append(char)

        self.textSurf = self.font.render(''.join(self.text), True, self.colour)

        if self.textSurf.get_width() > self.maxWidth:
            self.text.pop()
            self.textSurf = self.font.render(''.join(self.text), True, self.colour)

    def get(self):
        return ''.join(self.text)

if __name__ == '__main__':
    screen = pygame.display.set_mode((600,500))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Helvetica", 50)
    done = False

    keyboard = PGkeyboard()
    textDisplay = EditablePGText(font, 300)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                textDisplay.passChar(keyboard.getClickedKey(event.pos))

        screen.fill((255,255,255))

        keyboard.render(screen)
        textDisplay.render(screen, (0,200))

        pygame.display.flip()
        clock.tick(60)

                