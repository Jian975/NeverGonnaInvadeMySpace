import pygame
import random
import math
from pygame import mixer

#Initializing pygame
pygame.init()

#Make screen
screen = pygame.display.set_mode((800, 600))

#Background
#https://www.freepik.com/free-vector/realistic-galaxy-background_4665545.htm#query=space&position=0&from_view=search&track=sph
background = pygame.image.load('spaceBackground.jpg')

#Background music
#https://archive.org/details/Rick_Astley_Never_Gonna_Give_You_Up
mixer.music.load('fullSong.mp3')
mixer.music.play(-1)

#Title and icon
pygame.display.set_caption("Never Gonna Invade My Space")
icon = pygame.image.load('rickAstley')
pygame.display.set_icon(icon)

#Score

scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
gameOverFont = pygame.font.Font('freesansbold.ttf', 64)
textX = 10
textY = 10

#Rick player
rickImg = pygame.image.load("smallRick.png")
rickX = 370
rickY = 480
rickXChange = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
numOfEnemies = 7

for i in range(numOfEnemies):
    #https://www.flaticon.com/free-icon/alien-pixelated-shape-of-a-digital-game_41993?term=alien&page=1&position=6&origin=search&related_id=41993
    enemyImg.append(pygame.image.load("digitalAlien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(0.1)
    enemyYChange.append(40)

#Bullet
#ready - Bullet can't be seen
#fire - Bullet is moving currently
#https://www.flaticon.com/free-icons/google-play-music
bulletImg = pygame.image.load("musicalBullet.png")
bulletX = 0
bulletY = 480
bulletYChange = 0.5
bulletState = "ready"

def showScore(x, y):
    score = font.render("Times I Said Goodbye: " + str(-scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))
    
def rickPlayer(x, y):
    screen.blit(rickImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 35, y + 50))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    #Distance formula
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 40

def gameOverText():
    gameOverText = gameOverFont.render("I've Let You Down...", True, (255, 255, 255))
    screen.blit(gameOverText, (130, 250))
    mixer.music.stop()
    


#Game loop
running = True
while running:
    
    #Background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():

        #For shutting down game
        if event.type == pygame.QUIT:
            running = False

        #Player movement with keystroke  
        if event.type == pygame.KEYDOWN:

            #Left and right movement
            if event.key == pygame.K_LEFT:
                rickXChange = -0.3
            if event.key == pygame.K_RIGHT:
                rickXChange = 0.3
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    #Play sound when shooting
                    neverGonnaGiveYouUpSound = mixer.Sound('neverGonnaGiveYouUp.mp3')
                    neverGonnaGiveYouUpSound.play()
                    #Save the x position the bullet was shot from
                    bulletX = rickX
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                rickXChange = 0
             
    #Bullet movement
    #Resets bullet when bullet goes off screen
    if bulletY <= 0:
        bulletY = 480
        bulletState = 'ready'
            
    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange
            
    #Enemy movement
    #Move down and change directions once the enemy hits edge
    for i in range(numOfEnemies):

        #Game over
        if enemyY[i] > 440:
            iLetYouDown = mixer.Sound('iLetYouDown.mp3')
            iLetYouDown.play()
            #Hide all enemies
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOverText()
            break

        if enemyX[i] <= 0:
            enemyXChange[i] = 0.1
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] >= 736:
            enemyXChange[i] = -0.1
            enemyY[i] += enemyYChange[i]

        #Updating coordinates
        enemyX[i] += enemyXChange[i]

        #Collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            neverGonnaLetYouDownSound = mixer.Sound('neverGonnaLetYouDown.mp3')
            neverGonnaLetYouDownSound.play()
            bulletY = 480
            bulletState = "ready"
            scoreValue += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #Update player coordinates
    rickX += rickXChange

    #Setting boundaries (Part of the player icon is blank space, so boundary goes into negative instead of stopping at 0)
    if rickX <= -25:
        rickX = -25
    elif rickX >= 725:
        rickX = 725

    #Updating locations
    rickPlayer(rickX, rickY)
    showScore(textX, textY)
    
    pygame.display.update()