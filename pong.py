# Ibrar Yunus - University of St. Andrews
# Based on a Tutorial by Trevor Appleton @ http://trevorappleton.blogspot.co.uk/2014/04/writing-pong-using-python-and-pygame.html


import pygame
import sys
from pygame.locals import *


print("pygame-pong-0.1")
print("Ibrar Yunus ~ University of St. Andrews, United Kingdom")
print("\n\n\ninitializing")

# Frames per second
FPS = 500

# Window parameters
WINDOWWIDTH = 400 * 2
WINDOWHEIGHT = 300 * 2

# Setting up game environment parameters
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

# Setting up colour-scheme
WHITE = (255,255,255)
BLACK = (0,0,0)

def drawArena():
    DISPLAYSURF.fill((0,0,0))
    # Sketch the marking of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS*2)
    # The central line
    pygame.draw.line(DISPLAYSURF, WHITE, (int(WINDOWWIDTH/2), 0), (int(WINDOWWIDTH/2), WINDOWHEIGHT), int(LINETHICKNESS/4))

def drawPaddle(paddle):
    # Keeps the paddle from moving too low
    if(paddle.bottom > WINDOWHEIGHT - LINETHICKNESS):
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    # Keeps the paddle from moving too high
    if(paddle.top < LINETHICKNESS):
        paddle.top = LINETHICKNESS
    # Draw the paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if(ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS)):
        ballDirY = ballDirY * -1
    if(ball.left == LINETHICKNESS or ball.right == (WINDOWWIDTH - LINETHICKNESS)):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

def checkPaddleCollision(ball, paddle1, paddle2, ballDirX):
    if(ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom):
        return -1
    elif(ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom):
        return -1
    else:
        return 1

def computerPlayerAI(ball, ballDirX, paddle2):
    # if ball is moving away, center the paddle
    if (ballDirX == -1):
        if(paddle2.centery < (WINDOWHEIGHT/2)):
            paddle2.y += 1
        elif(paddle2.centery > (WINDOWHEIGHT/2)):
            paddle2.y -= 1
    # if ball is moving towards the paddle, track the movement
    elif ballDirX == 1:
        if(paddle2.centery < ball.centery):
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2

def checkPointScored(paddle1, ball, score, ballDirX):
    # if wall is hit
    if(ball.left == LINETHICKNESS):
        return 0;
    elif(ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom):
        score += 1
        return score
    else:
        return score

def showScores(score):
    resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

# The MAIN definition, starting point of the program
def main():
    pygame.init()
    global DISPLAYSURF
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("pygame-pond-0.1")

    # Initializing the starting positions
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE)/2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE)/2
    score = 0
    # This keeps track of the ball direction
    # Currently set movement is left and up
    ballDirX = -1
    ballDirY = -1

    # Creating rectangles for ball and the paddles
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball =  moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(paddle1, ball, score, ballDirY)
        ballDirX = ballDirX * checkPaddleCollision(ball, paddle1, paddle2, ballDirX)
        paddle2 = computerPlayerAI(ball, ballDirX, paddle2)

        showScores(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()