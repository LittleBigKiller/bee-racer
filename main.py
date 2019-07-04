import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

color_black = (0, 0, 0)
color_white = (255, 255, 255)

color_lightgray = (191, 191, 191)
color_gray = (127, 127, 127)
color_darkgray = (63, 63, 63)

color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('bee-racer')
clock = pygame.time.Clock()

tempCar = pygame.image.load('assets/sprites/F1Car_Red.png')


class Player:
    def __init__(self, name, x, y):
        self.image = pygame.image.load('assets/sprites/F1Car_Red.png')
        self.name = name
        self.x = y
        self.y = y
        self.speed = 0
        self.distance = 0
        self.score = 0
        self.playerInput = dict(
            left=False,
            right=False,
            up=False,
            down=False,
            fire=False,
        )

    def printname(self):
        print("Issa me, " + self.name + "!")

    def draw(self, debugHitbox=False):
        if debugHitbox:
            pygame.draw.rect(gameDisplay, color_green, [
                             self.x, self.y, tempCar.get_width(), tempCar.get_height()])
        gameDisplay.blit(self.image, (self.x, self.y - self.speed))

    def checkinputs(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.playerInput['left'] = True
            elif event.key == pygame.K_RIGHT:
                self.playerInput['right'] = True
            elif event.key == pygame.K_UP:
                self.playerInput['up'] = True
            elif event.key == pygame.K_DOWN:
                self.playerInput['down'] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.playerInput['left'] = False
            elif event.key == pygame.K_RIGHT:
                self.playerInput['right'] = False
            elif event.key == pygame.K_UP:
                self.playerInput['up'] = False
            elif event.key == pygame.K_DOWN:
                self.playerInput['down'] = False

    def reactinput(self):
        if self.playerInput['left']:
            self.x -= 5
        if self.playerInput['right']:
            self.x += 5
        if self.playerInput['down']:
            if self.speed > 0:
                self.speed -= 5
        if self.playerInput['up']:
            if self.speed < 180:
                self.speed += 1

        if self.x < 0:
            self.x = 0
        if self.x > display_width - self.image.get_width():
            self.x = display_width - self.image.get_width()

        self.distance += self.speed

        if self.speed >= 50:
            self.score += 1
        if self.speed >= 100:
            self.score += 1
        if self.speed >= 150:
            self.score += 1


def car(x, y, debugHitbox=False):
    if debugHitbox:
        pygame.draw.rect(gameDisplay, color_green, [
                         x, y, tempCar.get_width(), tempCar.get_height()])
    gameDisplay.blit(tempCar, (x, y))


def debug_display_speed(value):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Speed: " + str(value), True, color_black)
    gameDisplay.blit(text, text.get_rect(
        bottomright=(display_width - 5, display_height - 5)))
    pygame.display.update()


def display_score(value):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(value), True, color_black)
    gameDisplay.blit(text, (5, 5))
    pygame.display.update()


def game_loop():
    x = (display_width / 2 - tempCar.get_width()/2)
    y = (display_height / 2 + 200 - tempCar.get_height()/2)

    player = Player("LMAO", x, y)

    score = 0
    distance = 0

    while True:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            player.checkinputs(event)

        # Early Frame Code
        player.reactinput()

        # Draw Game Objects
        gameDisplay.fill(color_white)

        player.draw()

        # UI
        debug_display_speed(player.speed)
        display_score(player.score)

        # Late Frame Code

        pygame.display.update()
        clock.tick(60)


game_loop()

pygame.quit()
quit()
