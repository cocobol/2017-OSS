import random, time, pygame, sys, datetime
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 500
WINDOWHEIGHT = 450
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'
HIGHSCORE = []
MUTE = 0
DIFF = 0

file = open("highscore.txt", "r")
for line in file:
    HIGHSCORE += [int(line)]
file.close()

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 20

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = ( 50,  50,  50)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
ORANGE      = (255, 153,   0)
YELLOW      = (255, 255,   0)
GREEN       = ( 51, 255,  51)
BLUE        = (  0,   0, 255)
LIGHTBLUE   = ( 51, 255, 255)
PUPPLE      = (153,   0, 204)
SHADOW      = (130, 130, 130)

BORDERCOLOR = WHITE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (RED,ORANGE,YELLOW,GREEN,BLUE,LIGHTBLUE,PUPPLE,SHADOW)

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '..OO.',
                     '.OO..',
                     '.....',
                     '.....'],
                    ['.....',
                     '.O...',
                     '.OO..',
                     '..O..',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.OO..',
                     '..OO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.OOOO',
                     '.....',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.OO..',
                     '.OO..',
                     '.....',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '.O...',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OOO.',
                     '...O.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '.O...',
                     '.O...',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '.OOO.',
                     '.O...',
                     '.....',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '.O...',
                     '.OO..',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OOO.',
                     '..O..',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, MIDFONT, HIGHSCORE, MUTE, BGCOLOR, DIFF
    pygame.init()
    pygame.display.set_caption("TETRIS")
    icon = pygame.image.load('logo.png')
    pygame.display.set_icon(icon)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(BGCOLOR)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    MIDFONT = pygame.font.Font('freesansbold.ttf', 70)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    TFONT = pygame.font.Font('freesansbold.ttf', 80)
    # pygame.display.set_caption('Tetromino')
    titleSurf, titleRect = makeTextObjs('TETRIS', TFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 50)
    DISPLAYSURF.blit(titleSurf, titleRect)
    if BGCOLOR == BLACK :
        COLOR = "GRAY"
    else :
        COLOR = "BLACK"

    if MUTE == 0 :
        TEXT = "Mute"
    else :
        TEXT = "Unmute"

    choose = dumbmenu(DISPLAYSURF, [
                            'Start Game',
                            'Manual',
                            'Highscore',
                            TEXT,
                            'Theme : ' + COLOR,
                            'Quit'], 160,250,None,30,1.4)
    if choose == 0 :
        DISPLAYSURF.fill(BGCOLOR)
        choose2 = dumbmenu(DISPLAYSURF, [
                                'Easy',
                                'Normal',
                                'Hard',
                                ], 150,200,None,30,1.4)
        if choose2 == 0 :
            DIFF = 0
        elif choose2 == 1 :
            DIFF = 1
        elif choose2 == 2 :
            DIFF = 2

        if MUTE == 0 :
            if random.randint(0, 1) == 0:
                pygame.mixer.music.load('tetrisb.mid')
            else:
                pygame.mixer.music.load('tetrisc.mid')
            pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen2('Game Over')
        file = open("highscore.txt", "w")
        file.write(str(HIGHSCORE[0]) + '\n' + str(HIGHSCORE[1]) + '\n' + str(HIGHSCORE[2]) + '\n')
        file.close()
        main()

    elif choose == 1 :
        DISPLAYSURF.fill(BGCOLOR)
        uSurf, uRect = makeTextObjs("Up - Block rotate 90", BASICFONT, TEXTCOLOR)
        rSurf, rRect = makeTextObjs("Right - Block move right", BASICFONT, TEXTCOLOR)
        lSurf, lRect = makeTextObjs("Left - Block move left", BASICFONT, TEXTCOLOR)
        dSurf, dRect = makeTextObjs("Down - Block move down", BASICFONT, TEXTCOLOR)
        sSurf, sRect = makeTextObjs("Space bar - Block down", BASICFONT, TEXTCOLOR)
        fSurf, fRect = makeTextObjs("SHIFT - Block change", BASICFONT, TEXTCOLOR)
        pSurf, pRect = makeTextObjs("P - Paused", BASICFONT, TEXTCOLOR)
        vSurf, vRect = makeTextObjs("Level = (score / 5) + 1", BASICFONT, TEXTCOLOR)
        uRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 150)
        rRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 120)
        lRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 90)
        dRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 60)
        sRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 30)
        fRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 0)
        pRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - -30)
        vRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - -60)
        DISPLAYSURF.blit(uSurf, uRect)
        DISPLAYSURF.blit(rSurf, rRect)
        DISPLAYSURF.blit(lSurf, lRect)
        DISPLAYSURF.blit(dSurf, dRect)
        DISPLAYSURF.blit(sSurf, sRect)
        DISPLAYSURF.blit(fSurf, fRect)
        DISPLAYSURF.blit(pSurf, pRect)
        DISPLAYSURF.blit(vSurf, vRect)
        choose2 = dumbmenu(DISPLAYSURF, [
                                'Exit'], 160,350,None,30,1.4)
        if choose2 == 0 :
            main()

    elif choose == 2 :
        text1 = "EASY HIGHSCORE : " + str(HIGHSCORE[0])
        text2 = "NORMAL HIGHSCORE : " + str(HIGHSCORE[1])
        text3 = "HARD HIGHSCORE : " + str(HIGHSCORE[2])
        DISPLAYSURF.fill(BGCOLOR)
        eSurf, eRect = makeTextObjs(text1, BASICFONT, TEXTCOLOR)
        nSurf, nRect = makeTextObjs(text2, BASICFONT, TEXTCOLOR)
        hSurf, hRect = makeTextObjs(text3, BASICFONT, TEXTCOLOR)
        eRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 90)
        nRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 60)
        hRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 30)
        DISPLAYSURF.blit(eSurf, eRect)
        DISPLAYSURF.blit(nSurf, nRect)
        DISPLAYSURF.blit(hSurf, hRect)
        choose2 = dumbmenu(DISPLAYSURF, [
                                'Reset',
                                'Exit'], 160,350,None,30,1.4)

        if choose2 == 0 :
            HIGHSCORE[0] = 0
            HIGHSCORE[1] = 0
            HIGHSCORE[2] = 0
            file = open("highscore.txt", "w")
            file.write(str(HIGHSCORE[0]) + '\n' + str(HIGHSCORE[1]) + '\n' + str(HIGHSCORE[2]) + '\n')
            file.close()
            main()
        if choose2 == 1 :
            main()

    elif choose == 3 :
        if MUTE == 0 :
            MUTE = 1
        else :
            MUTE = 0
        main()

    elif choose == 4 :
        if BGCOLOR == BLACK :
            BGCOLOR = GRAY
        else :
            BGCOLOR = BLACK
        main()

    else :
        pygame.quit()
        sys.exit()

def runGame():
    # setup variables for the start of the game
    global HIGHSCORE
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    shadowPiece = getShadowPiece(fallingPiece)
    nextPiece = getNewPiece()
    start_ticks=pygame.time.get_ticks()

    while True: # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            shadowPiece = getShadowPiece(fallingPiece)
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime
            for i in range(1, BOARDHEIGHT):
                if not isValidPosition(board, fallingPiece, adjY=i):
                    break
                shadowPiece['y'] = fallingPiece['y'] + i
            if not isValidPosition(board, fallingPiece):
                return
            # can't fit a new piece on the board, so game over
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            for i in range(1, BOARDHEIGHT):
                if not isValidPosition(board, fallingPiece, adjY=i):
                    break
                shadowPiece['y'] = fallingPiece['y'] + i
                # drawPiece(shadowPiece)
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused') # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False


            elif event.type == KEYDOWN:
                # moving the piece sideways
                if event.key == K_LEFT and isValidPosition(board, fallingPiece, adjX=-1):
                    if MUTE == 0 :
                        pygame.mixer.Sound('move.wav').play()
                    fallingPiece['x'] -= 1
                    shadowPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif event.key == K_RIGHT and isValidPosition(board, fallingPiece, adjX=1):
                    if MUTE == 0 :
                        pygame.mixer.Sound('move.wav').play()
                    fallingPiece['x'] += 1
                    shadowPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # rotating the piece (if there is room to rotate)
                elif event.key == K_UP :
                    if MUTE == 0 :
                        pygame.mixer.Sound('move.wav').play()
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    shadowPiece['rotation'] = (shadowPiece['rotation'] + 1) % len(PIECES[shadowPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                        shadowPiece['rotation'] = (shadowPiece['rotation'] - 1) % len(PIECES[shadowPiece['shape']])
                elif (event.key == K_q): # rotate the other direction
                    if MUTE == 0 :
                        pygame.mixer.Sound('move.wav').play()
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    shadowPiece['rotation'] = (shadowPiece['rotation'] - 1) % len(PIECES[shadowPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                        shadowPiece['rotation'] = (shadowPiece['rotation'] + 1) % len(PIECES[shadowPiece['shape']])

                # making the piece fall faster with the down key
                elif event.key == K_DOWN :
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    if MUTE == 0 :
                        pygame.mixer.Sound('move.wav').play()
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

                elif event.key == K_LSHIFT:
                    fallingPiece, nextPiece = nextPiece, fallingPiece
                    fallingPiece['y'] = nextPiece['y']
                    nextPiece['y'] = -2
                    fallingPiece['x'] = nextPiece['x']
                    nextPiece['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2)
                    shadowPiece = getShadowPiece(fallingPiece)

                elif event.key == K_r:
                    runGame()

                elif event.key == K_m:
                    return

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
                shadowPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
                shadowPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                if HIGHSCORE[DIFF] < score :
                    HIGHSCORE[DIFF] = score
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(shadowPiece)
            drawPiece(fallingPiece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def showTextScreen2(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, MIDFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def showTextScreen3(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)
    pygame.display.update()
    time.sleep(1)
    FPSCLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 5) + 1
    fallFreq = 0.7 - (level * 0.02) - DIFF
    if DIFF == 0 :
        fallFreq = 0.5
    if DIFF == 1 :
        fallFreq = 0.27
    if DIFF == 2 :
        fallFreq = 0.1
    return level, fallFreq

def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    color = 0
    if shape == 'Z' :
        color = 0
    if shape == 'L' :
        color = 1
    if shape == 'O' :
        color = 2
    if shape == 'S' :
        color = 3
    if shape == 'J' :
        color = 4
    if shape == 'I' :
        color = 5
    if shape == 'T' :
        color = 6
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': color }
    return newPiece

def getShadowPiece(original):
    newPiece = {'shape': original['shape'],
                'rotation': original['rotation'],
                'x': original['x'],
                'y': original['y'], # start it above the board (i.e. less than 0)
                'color': 7}
    return newPiece

def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    if numLinesRemoved > 1 :
        showTextScreen3('X'+str(numLinesRemoved)) # pause until a key press
    if numLinesRemoved > 0 and MUTE == 0 :
        pygame.mixer.Sound('remove.wav').play()
    numLinesRemoved *= numLinesRemoved
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 2, pixely + 2, BOXSIZE - 2, BOXSIZE - 2))

def drawBoard(board):
    GRAY = (50,50,50)
    BLACK = (80,80,80)
    COLOR = GRAY
    if BGCOLOR == GRAY :
        COLOR = BLACK
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 3)
    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] != '.' :
                drawBox(x, y, board[x][y])
            else :
                if (x + y) % 2 == 0 :
                    pygame.draw.rect(DISPLAYSURF, COLOR, (152 + x * BOXSIZE, 30 + y * BOXSIZE, BOXSIZE - 1, BOXSIZE - 1))

def drawStatus(score, level):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10, 50)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (10, 20)
    DISPLAYSURF.blit(levelSurf, levelRect)

    hsSurf = BASICFONT.render('Highscore: %s' % HIGHSCORE[DIFF], True, TEXTCOLOR)
    hsRect = hsSurf.get_rect()
    hsRect.topleft = (10, 80)
    DISPLAYSURF.blit(hsSurf, hsRect)

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-110, pixely=100)
    # now = datetime.datetime.now()
    # nowTime = now.strftime('%H:%M:%S')
    # nextSurf = BASICFONT.render(nowTime, True, TEXTCOLOR)
    # nextRect.topleft = (WINDOWWIDTH - 110, )
    # DISPLAYSURF.blit(nextSurf, nextRect)


def dumbmenu(screen, menu, x_pos = 100, y_pos = 100, font = None,
            size = 70, distance = 1.4, fgcolor = (255,255,255),
            cursorcolor = (255,0,0), exitAllowed = True):
	"""Draws a Menu using pygame.

	Parameters are: screen, menu, x_pos, y_pos, font,
	                size, distance, fgcolor, cursor

	PARAMETERS
	==========
	screen (Surface): The surface created with pygame.display.set_mode()

	menu (List):      A List of every menupoint that should be visible

	x_pos (digit):   Start of x_position, in Pixels (Default: 100)

	y_pos (digit):   Start of y_position, in Pixels (Default: 100)

	size (digit):    Fontsize (Default: 70)

	distance (float):Y-Distance after every single menupoint
	                 (Default: 1.4)

	fgcolor (Tupel): Foreground-Color, means the Font-Color
	                 (Default: (255,255,255), means white)

	cursorcolor (Tupel): Cursor-Color, means that ">"-Charakter
	                     (Default: (255,0,0), means red)

	exitAllowed (Bool): If True:
	                    If User pressed the ESC-Key, the Cursor will
	                    move to the last Menupoint. If Cursorposition
	                    is already to the last Menupoint, a pressed
	                    ESC-Key will return the latest Menupoint. Very
	                    useful if the last Menupoint is something like
	                    "Quit Game"...
	                    If False:
	                    A pressed ESC-Key will takes no effect.
	                    (Default: True)

	EXAMPLE
	=======
	import pygame
	from dumbmenu import *
	pygame.init()

	# Just a few static variables
	red   = 255,  0,  0
	green =   0,255,  0

	size = width, height = 640,480
	screen = pygame.display.set_mode(size)
	screen.fill(blue)
	pygame.display.update()

	print dumbmenu(screen, [
	                        'Start Game',
	                        'Options',
	                        'Manual',
	                        'Show Highscore',
	                        'Quit Game'],
	                        320, 250, "Courier", 32, 1.4, green, red)

	HOW TO INTERACT
	===============
	After called dumbmenu(), the User MUST choose an Menupoint. The
	Script will be haltet until the User makes a decision or a event
	called pygame.QUIT() will be raised.

	The User kann pressed directly a Key from 1 to 9 to take the choice.
	Another Method is pressing the UP-/DOWN-Key and take the choice with
	RETURN. Every single Menupoint will get a Number, beginning with 1.

	The return-value ist the Number of Menupoint decreased by 1. From
	the above Example: If the User will choice "Manual", the return-
	value will be 2.

	If the number of Menupoints is greater than 9, the numeration will
	continue from A to Z... the return-value is still a number,
	continue from 9 to 34...

	If a pygame.QUIT()-Event will be raised, the return-value will be
	-1.

	ACTUAL LIMITATIONS
	==================
	It's actually not possible to change the Font itself.

	Drawing Menu will be antialiased. If you want to change that, you'll
	have to change the sourcecode directly.

	OTHERS
	======
	Yes, I know, my english isn't that good (I'm not a naturally
	speaker) and the sourcecode isn't that good too ;) . It's more or
	less a "quick'n dirty"-Solution. My first intention was to make that
	code for me, but I hope it could may useful for other people too...

	Version: 0.40
	Author: Manuel Kammermeier aka Astorek
	License: MIT

	CHANGES:
	========
	Version 0.35:
	- First Version

	Version 0.40:
	- "bgcolor" removed, now the Function saves the Background
	- added "font", which allows to choose a Systemfont
	"""


	# Draw the Menupoints
	pygame.font.init()
	if font == None:
		myfont = pygame.font.Font(None, size)
	else:
		myfont = pygame.font.SysFont(font, size)
	cursorpos = 0
	renderWithChars = False
	for i in menu:
		if renderWithChars == False:
			text =  myfont.render(str(cursorpos + 1)+".  " + i,
				True, fgcolor)
		else:
			text =  myfont.render(chr(char)+".  " + i,
				True, fgcolor)
			char += 1
		textrect = text.get_rect()
		textrect = textrect.move(x_pos,
		           (size // distance * cursorpos) + y_pos)
		screen.blit(text, textrect)
		pygame.display.update(textrect)
		cursorpos += 1
		if cursorpos == 9:
			renderWithChars = True
			char = 65

	# Draw the ">", the Cursor
	cursorpos = 0
	cursor = myfont.render(">", True, cursorcolor)
	cursorrect = cursor.get_rect()
	cursorrect = cursorrect.move(x_pos - (size // distance),
	             (size // distance * cursorpos) + y_pos)

	# The whole While-loop takes care to show the Cursor, move the
	# Cursor and getting the Keys (1-9 and A-Z) to work...
	ArrowPressed = True
	exitMenu = False
	clock = pygame.time.Clock()
	filler = pygame.Surface.copy(screen)
	fillerrect = filler.get_rect()
	while True:
		clock.tick(30)
		if ArrowPressed == True:
			screen.blit(filler, fillerrect)
			pygame.display.update(cursorrect)
			cursorrect = cursor.get_rect()
			cursorrect = cursorrect.move(x_pos - (size // distance),
			             (size // distance * cursorpos) + y_pos)
			screen.blit(cursor, cursorrect)
			pygame.display.update(cursorrect)
			ArrowPressed = False
		if exitMenu == True:
			break
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return -1
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE and exitAllowed == True:
					if cursorpos == len(menu) - 1:
						exitMenu = True
					else:
						cursorpos = len(menu) - 1; ArrowPressed = True


				# This Section is huge and ugly, I know... But I don't
				# know a better method for this^^
				if event.key == pygame.K_1:
					cursorpos = 0; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_2 and len(menu) >= 2:
					cursorpos = 1; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_3 and len(menu) >= 3:
					cursorpos = 2; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_4 and len(menu) >= 4:
					cursorpos = 3; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_5 and len(menu) >= 5:
					cursorpos = 4; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_6 and len(menu) >= 6:
					cursorpos = 5; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_7 and len(menu) >= 7:
					cursorpos = 6; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_8 and len(menu) >= 8:
					cursorpos = 7; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_9 and len(menu) >= 9:
					cursorpos = 8; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_a and len(menu) >= 10:
					cursorpos = 9; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_b and len(menu) >= 11:
					cursorpos = 10; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_c and len(menu) >= 12:
					cursorpos = 11; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_d and len(menu) >= 13:
					cursorpos = 12; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_e and len(menu) >= 14:
					cursorpos = 13; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_f and len(menu) >= 15:
					cursorpos = 14; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_g and len(menu) >= 16:
					cursorpos = 15; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_h and len(menu) >= 17:
					cursorpos = 16; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_i and len(menu) >= 18:
					cursorpos = 17; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_j and len(menu) >= 19:
					cursorpos = 18; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_k and len(menu) >= 20:
					cursorpos = 19; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_l and len(menu) >= 21:
					cursorpos = 20; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_m and len(menu) >= 22:
					cursorpos = 21; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_n and len(menu) >= 23:
					cursorpos = 22; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_o and len(menu) >= 24:
					cursorpos = 23; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_p and len(menu) >= 25:
					cursorpos = 24; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_q and len(menu) >= 26:
					cursorpos = 25; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_r and len(menu) >= 27:
					cursorpos = 26; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_s and len(menu) >= 28:
					cursorpos = 27; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_t and len(menu) >= 29:
					cursorpos = 28; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_u and len(menu) >= 30:
					cursorpos = 29; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_v and len(menu) >= 31:
					cursorpos = 30; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_w and len(menu) >= 32:
					cursorpos = 31; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_x and len(menu) >= 33:
					cursorpos = 32; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_y and len(menu) >= 34:
					cursorpos = 33; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_z and len(menu) >= 35:
					cursorpos = 34; ArrowPressed = True; exitMenu = True
				elif event.key == pygame.K_UP:
					ArrowPressed = True
					if cursorpos == 0:
						cursorpos = len(menu) - 1
					else:
						cursorpos -= 1
				elif event.key == pygame.K_DOWN:
					ArrowPressed = True
					if cursorpos == len(menu) - 1:
						cursorpos = 0
					else:
						cursorpos += 1
				elif event.key == pygame.K_KP_ENTER or \
				     event.key == pygame.K_RETURN:
							exitMenu = True

	return cursorpos

if __name__ == '__main__':
    main()
