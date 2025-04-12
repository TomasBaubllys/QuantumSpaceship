# TODO

# add shooting
# add enemy freezing

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
    K_f
)

# screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# enemy constants
CREATING_ENEMY_TIME_INTERVAL = 250 # milliseconds
ADD_ENEMY = pg.USEREVENT + 1
ENEMY_HEIGHT = 10
ENEMY_WIDTH = 20
ENEMY_CREATION_OFFSET_X_MIN = 20
ENEMY_CREATION_OFFSET_X_MAX = 100
ENEMY_SPEED_MIN = 5
ENEMY_SPEED_MAX = 15
FPS = 60

# teleport delay in frames
TELEPORT_DELAY = FPS / 2
FREEZE_DELAY = FPS * 2

SCORE_OFFSET = 10

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
    if ship.rect.top < 0:
        ship.rect.top = 0
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

# initialize pygame
pg.init()

# set the screen title
pg.display.set_caption('Quantum Ship')

# create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# setup the ship
ship = pg.sprite.Sprite()
ship.surf = pg.Surface((60, 20))
ship.surf.fill((0, 255, 0))
ship.rect = ship.surf.get_rect()
teleportTimeOut = 0
freezeTimeOut = 0

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
myFont = pg.font.SysFont('Arial', 48)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == ADD_ENEMY:
            createEnemy()

    # black background
    screen.fill((0, 0, 0))

    # update the ship
    pressedKeys = pg.key.get_pressed()

    # if escape key was pressed quit
    if pressedKeys[K_ESCAPE]:
        running = False

    if pressedKeys[K_f]:
        freezeTimeOut = FREEZE_DELAY


    if pg.sprite.spritecollideany(ship, enemies):
        ship.kill()
        running = False

        # create  text surface
        textSurface = myFont.render('Game Over!', False, (255, 0, 0), (0, 0, 0))
        screen.blit(textSurface, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
        thereIsMessage = True


    # update the sprites

    if freezeTimeOut > 0:
        freezeTimeOut -= 1
    else:
        updateEnemies()

    updateShip(pressedKeys)

    # display the ship
    for entity in allSprites:
        screen.blit(entity.surf, entity.rect)

    # display the score
    scoreTextSurface = myFont.render(str(playerScore), False, (255, 0, 0))
    screen.blit(scoreTextSurface, (SCORE_OFFSET, SCORE_OFFSET))

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

    teleportTimeOut += 1

    tickCounter += 1
    # 60 fps
    pg.time.Clock().tick(FPS)