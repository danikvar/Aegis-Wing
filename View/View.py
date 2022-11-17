import pygame
import os
from pygame.locals import *

"""
Set variables
"""
screenWidth = 800
screenHeight = 600
time = 0

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Aegis Wing')

"""
Define FPS
"""
clock = pygame.time.Clock()
fps = 60

"""
Load images image
"""
#background nebula
nebula = pygame.image.load("../Assets/nebula_brown.png")
nebula = pygame.transform.scale(nebula, (screenWidth, screenHeight))

#background debris
debris = pygame.image.load("../Assets/debris2_brown.png")
debris = pygame.transform.scale(debris, (screenWidth, screenHeight))

#object images
playerSpriteSheet = pygame.image.load("../Assets/double_ship.png")
bulletSprite = pygame.image.load("../Assets/shot2.png")

#Sounds
soundMixer = pygame.mixer
soundMixer.init()
thrusterSound = soundMixer.Sound("../Assets/thrust.mp3")


# Key map
def KeyMap():
    def __init__(self):
        self.keys = pygame.key.get_pressed()

    def up(self):
        return self.keys[pygame.K_UP] or self.keys[pygame.K_w]

    def down(self):
        return self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]


# Ship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = spriteSheet.subsurface(0, 0, 90, 90)
        self.image2 = spriteSheet.subsurface(90, 0, 90, 90)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.sound = thrusterSound
        self.thrusters_off()
        self.lastShot = pygame.time.get_ticks()


    def thrusters_off(self):
        self.image = self.image1
        self.sound.stop()

    def thrusters_on(self):
        self.image = self.image2
        if not soundMixer.get_busy():
           self.sound.play(-1)

    def update(self):
        #set movement speed
        speed = 9
        cooldown = 300 #milliseconds

        #get key press
        key = pygame.key.get_pressed()
        #movement of ship
        if (key[pygame.K_UP] or key[pygame.K_w]) and (self.rect.top > 0):
            self.thrusters_on()
            self.rect.y -= speed
        if (key[pygame.K_DOWN] or key[pygame.K_s]) and (self.rect.bottom < screenHeight):
            self.thrusters_on()
            self.rect.y += speed
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and (self.rect.left > 0):
            self.thrusters_on()
            self.rect.x -= speed
        if (key[pygame.K_RIGHT] or key[pygame.K_d]) and (self.rect.right < screenWidth):
            self.thrusters_on()
            self.rect.x += speed
        #shoot
        timeNow = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and (timeNow - self.lastShot > cooldown):
            bullet = Bullets(self.rect.right, self.rect.centery)
            bulletGroup.add(bullet)
            self.lastShot = timeNow

        if not any(key):
            self.thrusters_off()


# Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletSprite
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.x += 10
        if self.rect.left > screenWidth:
            self.kill()


# create sprite group
spaceshipGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()

# create player
playerShip = Spaceship(playerSpriteSheet, 100, 100)
spaceshipGroup.add(playerShip)


"""
The game event loop
"""
run = True
while run:
    #frame rate
    clock.tick(fps)

    #draw and animate background
    time += 1
    wtime = (time / 4) % screenWidth
    screen.blit(nebula, (0, 0))
    screen.blit(debris, (0 - wtime, 0))
    screen.blit(debris, (600 - wtime, 0))

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update spaceship
    playerShip.update()

    #update
    bulletGroup.update()

    #draw sprite groups
    spaceshipGroup.draw(screen)
    bulletGroup.draw(screen)

    #update display
    pygame.display.update()

pygame.quit()