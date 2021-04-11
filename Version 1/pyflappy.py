# basic setup
import pygame, random, sys, time
import os; work_dir = os.path.dirname(__file__) + '/'
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# variable, boolean and tuple values
shade = (255, 255, 255)
done = False
jump = False
started = False
modeno = 2
# screen setup
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption('PyFlappy')
# image setup
birdsurf = pygame.transform.scale(pygame.image.load(work_dir+'resources/bird.png').convert_alpha(), (54, 41))
background_image = pygame.image.load(work_dir+'resources/background.png').convert_alpha()
title_image = pygame.image.load(work_dir+'resources/title.png').convert_alpha()
uparrow = pygame.image.load(work_dir+'resources/arrowup.png').convert_alpha()
downarrow = pygame.image.load(work_dir+'resources/arrowdown.png').convert_alpha()
# text setup
myfont = pygame.font.SysFont('Ayuthaya', 30)
start_text = myfont.render('START', False, (255,255,255))
quit_text = myfont.render('QUIT', False, (255,255,255))
# sound setup
ding = pygame.mixer.Sound(work_dir+'resources/ding.wav')
splat = pygame.mixer.Sound(work_dir+'resources/splat.wav')
# rects
startbutton = pygame.Rect(160, 130, 180, 60)
quitbutton = pygame.Rect(160, 210, 180, 60)
mode_rect = pygame.Rect(20, 170, 120, 60)
birdrect = birdsurf.get_rect()

while True:
        # menu loop
        pygame.mixer.music.load(work_dir+'resources/menutrack.mp3')
        pygame.mixer.music.play(-1)
        while not started:
                #event queue
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                # close button setup
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                # button click (a for x, b for y)
                                a, b = event.pos
                                if startbutton.collidepoint(a, b):
                                        started = True
                                        pygame.mixer.music.stop()
                                        pygame.mixer.music.load(work_dir+'resources/theme.mp3')
                                        pygame.mixer.music.play(-1)
                                # starts music, plays infinitely
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                # button click (c for x, d for y)
                                c, d = event.pos
                                if quitbutton.collidepoint(c, d):
                                        pygame.quit()
                                        sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                                modeno += 1
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                                modeno -= 1
                        
                # blitting images
                screen.blit(background_image, (0,0))
                screen.blit(title_image, (75,20))
                # drawing rectangles
                pygame.draw.rect(screen, (0,100,0), startbutton)
                pygame.draw.rect(screen, (150,0,0), quitbutton)
                # blitting text
                screen.blit(start_text, (200,140))
                screen.blit(quit_text, (210,220))
                # highscore data retrieval
                if modeno == 1:
                        highscore_file = open(work_dir+'data/slowscore.txt', 'r')
                        scored = highscore_file.read()
                        highscore_file.close()
                if modeno == 2:
                        highscore_file = open(work_dir+'data/normscore.txt', 'r')
                        scored = highscore_file.read()
                        highscore_file.close()
                if modeno == 3:
                        highscore_file = open(work_dir+'data/fastscore.txt', 'r')
                        scored = highscore_file.read()
                        highscore_file.close()
                highscore = 'Highscore: ' + str(scored)
                # setting up and blitting highscore text
                highscore_text = myfont.render(highscore, False, (0,0,0))
                screen.blit(highscore_text, (10,350))
                # difficulty setting
                pygame.draw.rect(screen, (0,0,100), mode_rect)
                if modeno == 1:
                        mode = 'Slow'
                if modeno == 2:
                        mode = 'Normal'
                if modeno == 3:
                        mode= 'Fast'
                if modeno == 4:
                        modeno = 3
                if modeno == 0:
                        modeno = 1

                mode_text = myfont.render(mode, False, (255,255,255))
                screen.blit(mode_text, (30, 180))
                if modeno == 1 or modeno == 2:
                        screen.blit(uparrow, (70,95))
                if modeno == 2 or modeno == 3:
                        screen.blit(downarrow, (70,235))
                # standard loop ending (clear screen, framerate)
                pygame.display.update()
                clock.tick(60)
        # setting up booleans and variables needed to be reset each restart
        started = False
        # how far pipes have gone
        pipefw = 0
        # base pip height (randomized later)
        bht = 150
        # score value (of game)
        score = 0
        # variable to set when if statement should finish jump time
        jumpcount = 0
        # base flappy coords (centre coords adjusted from these as base)
        x = 100
        y = 100
        # modified coords for pipes and flappy height
        x_pipe = 440
        y_mod = y+30
        y_pipe1 = 0
        y_pipe2 = 0
        
        while not done:
                # game loop
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                # close button setup
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                # jump key control
                                jump = True
                
                if jump:
                        # increasing jump timer and increasing y value for flappy
                        jumpcount += 1
                        y_mod -= 6
                        # stopping if statement if jump timer is at limit, and resetting it
                        if jumpcount == 15:
                                jumpcount = 0
                                jump = False
                else:
                        y_mod += 5 # if not jumping, standard fall rate

                # setting background
                screen.blit(background_image, (0,0))
                
                #setting bird rectangle position, and aligning image to this
                birdrect.center = ((x+27),y_mod)
                screen.blit(birdsurf, birdrect)
                #setting y or x positions or heights according to random base height value
                y_pipe1 = 400-bht
                y_pipe2 = 250-bht
                filter_rect_x = (x_pipe-pipefw+60)
                # creating and drawing rectangles
                basepipe = pygame.Rect((x_pipe-pipefw), (y_pipe1), 60, bht)
                base_surf = pygame.Surface((70, (bht+2)))
                base_surf.fill((0,100,0))
                screen.blit(base_surf, ((x_pipe-pipefw-5),(y_pipe1-2)))
                toppipe = pygame.Rect((x_pipe-pipefw), 0, 60, y_pipe2)
                top_surf = pygame.Surface((70,(y_pipe2+3)))
                top_surf.fill((0,100,0))
                screen.blit(top_surf, ((x_pipe-pipefw-5), 0))
                # filter rectangles detects when flappy goes past, for later use in loop
                filter_rect = pygame.Rect(filter_rect_x, (y_pipe1-150), 0, 150)

                pipefw += (modeno*2)+2 # rate at which pipes go forward based on difficulty mode

                if pipefw > 499:
                        # resets pipe position to 0 once it hits max, and randomises base pipe height to be used in next loop runthrough
                        pipefw = 0
                        bht = random.randint(50,201)

                if birdrect.colliderect(basepipe) or birdrect.colliderect(toppipe) or y_mod > 379 or y_mod < 20:
                        # stops loop if flappy rectangle hits either pipe
                        done = True
                        # stops music and plays splat
                        pygame.mixer.music.stop()
                        splat.play()
                        # opens highscore file, and adds high score as variable top_score
                        highscore_file = open(work_dir+'data/'+['slow', 'norm', 'fast'][modeno-1]+'score.txt', 'r')
                        top_score = highscore_file.read()
                        highscore_file.close()
                        if int(top_score) < int(score):
                                # top_score is checked against current finished score to see if high score should be changed, and doing so if necessary
                                highscore_edit_file = open(work_dir+'data/'+['slow', 'norm', 'fast'][modeno-1]+'score.txt', 'w')
                                highscore_edit_file.write(str(score))
                                highscore_edit_file.close()

                        time.sleep(0.5)

                if modeno == 3: adjustment=5
                else: adjustment = 0
                
                if birdrect.colliderect(filter_rect) and filter_rect_x < (105+adjustment):
                        # adding score point if flappy is hitting filter rectangle, but only when it is touching the last point of the flappy, so score is only recorded once
                        score += 1
                        # play ding sound
                        ding.play()

                # creates and blits text each frame according to what the current score is
                textsurface = myfont.render(str(score), False, (0,0,0))
                screen.blit(textsurface, (10,10))

                # standard loop ending (clear screen, framerate)
                pygame.display.update()
                clock.tick(60)
        # setup for repeating the loop for restart
        done = False
