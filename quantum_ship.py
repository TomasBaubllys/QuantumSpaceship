import random

try:
    import pygame as pg
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])
    import pygame as pg

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_ESCAPE,
    K_r,
    K_f,
    K_x,
    K_h,
    K_z
)

# screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

LINE_WIDTH = 4

# enemy constants
CREATING_ENEMY_TIME_INTERVAL = 500#250 # milliseconds
ADD_ENEMY = pg.USEREVENT + 1
ENEMY_HEIGHT = 10
ENEMY_WIDTH = 20
ENEMY_CREATION_OFFSET_X_MIN = 20
ENEMY_CREATION_OFFSET_X_MAX = 100
ENEMY_SPEED_MIN = 1#5
ENEMY_SPEED_MAX = 5#15
FPS = 60

SHIP_WIDTH = 60
SHIP_HEIGHT = 20

# teleport delay in frames
TELEPORT_DELAY = FPS / 2
FREEZE_DELAY = FPS * 2
FREEZE_KEY_TIMEOUT = FPS * 2
STATE_KEY_DELAY = FPS

SCORE_OFFSET_X = 100
SCORE_OFFSET_Y = 10
SCORE_STATE_FONT_SIZE = 20

MEASUREMENT_COUNT_DOWN = FPS * 2

def displayMeasurement():
    stateTextSurface = myFontScoreState.render("Measurement: " + str(fate), False, (255, 0, 0), (0, 0, 0))
    screen.blit(stateTextSurface, (SCREEN_WIDTH / 2, SCORE_OFFSET_Y))

def gameOver():
    textSurface = myFontGameOver.render('Game Over!', False, (255, 0, 0), (0, 0, 0))
    screen.blit(textSurface, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))

def teleporShip():
    while True:
        ship_x = random.randint(0, SCREEN_WIDTH - ship.rect.width)
        ship_y = random.randint(0, SCREEN_HEIGHT - ship.rect.height)
        ship.rect = ship.surf.get_rect(center = (ship_x, ship_y))

        if not pg.sprite.spritecollideany(ship, enemies):
            break

# updates the ships position
def updateShip(pressedKeys):
    if pressedKeys[K_UP]:
        ship.rect.move_ip(0, -5)
    if pressedKeys[K_DOWN]:
        ship.rect.move_ip(0, 5)
    if pressedKeys[K_RIGHT]:
        ship.rect.move_ip(5, 0)
    if pressedKeys[K_LEFT]:
        ship.rect.move_ip(-5, 0)

    keepShipBounds()

def keepShipBounds():
    if ship.rect.left < 0:
        ship.rect.left = 0
    if ship.rect.right > SCREEN_WIDTH:
        ship.rect.right = SCREEN_WIDTH

    if classicState == 0:
        if ship.rect.bottom > SCREEN_HEIGHT / 2 - LINE_WIDTH / 2:
            ship.rect.bottom = SCREEN_HEIGHT / 2 - LINE_WIDTH / 2
        if ship.rect.top < 0:
            ship.rect.top = 0

    if classicState == 1:
        if ship.rect.top < SCREEN_HEIGHT / 2 + LINE_WIDTH / 2:
            ship.rect.top = SCREEN_HEIGHT / 2 + LINE_WIDTH / 2
        if ship.rect.bottom > SCREEN_HEIGHT:
            ship.rect.bottom = SCREEN_HEIGHT

def createEnemy():
    enemy = pg.sprite.Sprite()
    enemy.surf = pg.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
    enemy.surf.fill((255, 0, 0))
    enemy_x = random.randint(SCREEN_WIDTH + ENEMY_CREATION_OFFSET_X_MIN, SCREEN_WIDTH + ENEMY_CREATION_OFFSET_X_MAX)
    enemy_y = random.randint(0, SCREEN_HEIGHT)
    enemy.rect = enemy.surf.get_rect(center = (enemy_x, enemy_y))
    enemy.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
    enemies.add(enemy)
    allSprites.add(enemy)

def updateEnemies():
    for enemy in enemies:
        enemy.rect.move_ip(-enemy.speed, 0)
        if enemy.rect.right < 0:
            enemy.kill()

        if gameState == 1:
            if pressedKeys[K_UP]:
                enemy.rect.move_ip(0, -5)
            if pressedKeys[K_DOWN]:
                enemy.rect.move_ip(0, 5)

        if enemy.rect.bottom > SCREEN_HEIGHT:
            enemy.rect.top = 0
        elif enemy.rect.top < 0:
            enemy.rect.bottom = SCREEN_HEIGHT

# initialize pygame
pg.init()

# set the screen title
pg.display.set_caption('Quantum Ship')

# create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# setup the ship
ship = pg.sprite.Sprite()
ship.surf = pg.Surface((SHIP_WIDTH, SHIP_HEIGHT))
ship.surf.fill((0, 255, 0))
ship.rect = ship.surf.get_rect()

twinShip = pg.sprite.Sprite()
twinShip.surf = pg.Surface((SHIP_WIDTH, SHIP_HEIGHT))
twinShip.surf.fill((0, 255, 0))
twinShip.rect = twinShip.surf.get_rect()

teleportTimeOut = 0
freezeTimeOut = 0

freezeKeyTimeOut = 0

# 0 represents classic, 1 represents quantum
gameState = 0
# 0 represents |0> 1 represents |1>
classicState = 0
# 0 represents |+> 1 represents |->
quantumState = 0
# temporary fix
displayQuantumSTate = 0

stateSwitchingDelay = 0

# global score variable increases every second
playerScore = 0
tickCounter = 0

# setup the enemies
pg.time.set_timer(ADD_ENEMY, CREATING_ENEMY_TIME_INTERVAL)
enemies = pg.sprite.Group()

# group all sprites
allSprites = pg.sprite.Group()
allSprites.add(ship)

running = True
thereIsMessage = False

# font variable
myFontGameOver= pg.font.SysFont('Arial', 48)
myFontScoreState = pg.font.SysFont('Arial', SCORE_STATE_FONT_SIZE)

measurementCountDown = 0

# used to store the measurements
fate = 0

while running:
    rand = random.randint(0, 300)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == ADD_ENEMY and freezeTimeOut == 0:
            createEnemy()

    # black background
    screen.fill((0, 0, 0))

    # update the ship
    pressedKeys = pg.key.get_pressed()

    # if escape key was pressed quit
    if pressedKeys[K_ESCAPE]:
        running = False

    if pressedKeys[K_f] and freezeKeyTimeOut > FREEZE_KEY_TIMEOUT:
        freezeTimeOut = FREEZE_DELAY
        freezeKeyTimeOut = 0

    if ((pressedKeys[K_x] and stateSwitchingDelay >= STATE_KEY_DELAY) or rand == 100 or rand == 200 )and gameState == 0:
        stateSwitchingDelay = 0
        ship_x = ship.rect.centerx
        ship_y = ship.rect.centery
        if classicState == 0:
            classicState = 1
            ship.rect = ship.surf.get_rect(center = (ship_x, ship_y + SCREEN_HEIGHT / 2))
        elif classicState == 1:
            classicState = 0
            ship.rect = ship.surf.get_rect(center = (ship_x, ship_y - SCREEN_HEIGHT / 2))

    if ((pressedKeys[K_z] and stateSwitchingDelay >= STATE_KEY_DELAY) or rand == 50 or rand == 250 ) and gameState == 1:
        stateSwitchingDelay = 0
        if displayQuantumSTate == 0:
            displayQuantumSTate = 1
        elif displayQuantumSTate == 1:
            displayQuantumSTate = 0

    if pressedKeys[K_h] and stateSwitchingDelay >= STATE_KEY_DELAY or rand == 150:
        if gameState == 0:
            gameState = 1
            twinShip_x = ship.rect.centerx
            twinShip_y = ship.rect.centery

            if classicState == 0:
                twinShip_y += SCREEN_HEIGHT / 2 + SHIP_HEIGHT / 2 + LINE_WIDTH / 2
            else:
                twinShip_y -= SCREEN_HEIGHT / 2

            quantumState = classicState
            twinShip.rect = ship.surf.get_rect(center = (twinShip_x, twinShip_y))
        elif gameState == 1:
            gameState = 0
        stateSwitchingDelay = 0

    if gameState == 0:
        if pg.sprite.spritecollideany(ship, enemies):
            ship.kill()
            running = False
            # create  text surface
            gameOver()
            thereIsMessage = True
    else:
        if pg.sprite.spritecollideany(twinShip, enemies):
            fate = random.randint(0, 1)
            print("Measured: " + str(fate))
            if quantumState == fate:
                gameState = 0
                classicState = quantumState
                measurementCountDown = MEASUREMENT_COUNT_DOWN

            else:
                twinShip.kill()
                ship.kill()
                gameOver()
                displayMeasurement()
                running = False
                thereIsMessage = True

        elif pg.sprite.spritecollideany(ship, enemies):
            fate = random.randint(0, 1)
            print("Measured: " + str(fate))
            if quantumState == fate:
                twinShip.kill()
                ship.kill()
                gameOver()
                displayMeasurement()
                running = False
                thereIsMessage = True
            else:
                gameState = 0
                classicState = fate
                measurementCountDown = MEASUREMENT_COUNT_DOWN

    # update the sprites
    if freezeTimeOut > 0:
        freezeTimeOut -= 1
    else:
        updateEnemies()

    if gameState == 0:
        updateShip(pressedKeys)

    # display the ships
    for entity in allSprites:
        screen.blit(entity.surf, entity.rect)

    if gameState == 1:
        screen.blit(twinShip.surf, twinShip.rect)

    # display the score and state
    scoreTextSurface = myFontScoreState.render("Score: " +  str(playerScore) , False, (255, 0, 0))
    screen.blit(scoreTextSurface, (SCREEN_WIDTH - SCORE_OFFSET_X, SCORE_OFFSET_Y))


    if gameState == 0:
        stateTextSurface = myFontScoreState.render("State: |" + str(classicState) + ">", False, (255, 0, 0), (0, 0, 0))
    else:
        charState = '+'
        if displayQuantumSTate == 1:
            charState = '-'
        stateTextSurface = myFontScoreState.render("State: |" + charState + ">", False, (255, 0, 0), (0, 0, 0))

    screen.blit(stateTextSurface, (SCREEN_WIDTH - SCORE_OFFSET_X, SCORE_OFFSET_Y * 2 + SCORE_STATE_FONT_SIZE))

    # draw a line in the middle of the screen
    pg.draw.line(screen, (255, 255, 255), (0, SCREEN_HEIGHT / 2), (SCREEN_WIDTH, SCREEN_HEIGHT / 2), LINE_WIDTH)

    if measurementCountDown > 0:
        measurementCountDown -= 1
        displayMeasurement()

    pg.display.flip()

    if thereIsMessage:
        pg.time.wait(2000)

    if tickCounter > FPS:
        tickCounter = 0
        playerScore += 1

    if pressedKeys[K_r]:
        if teleportTimeOut > TELEPORT_DELAY:
            teleporShip()
            teleportTimeOut = 0

    stateSwitchingDelay += 1
    teleportTimeOut += 1
    freezeKeyTimeOut += 1

    tickCounter += 1
    # 60 fps
    pg.time.Clock().tick(FPS)
