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

tempCar = pygame.image.load('assets/sprites/F1Car.png')


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

    playerInput = dict(
        left=False,
        right=False,
        up=False,
        down=False,
        fire=False,
    )

    speed = 0

    score = 0
    distance = 0

    while True:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerInput['left'] = True
                elif event.key == pygame.K_RIGHT:
                    playerInput['right'] = True
                elif event.key == pygame.K_UP:
                    playerInput['up'] = True
                elif event.key == pygame.K_DOWN:
                    playerInput['down'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    playerInput['left'] = False
                elif event.key == pygame.K_RIGHT:
                    playerInput['right'] = False
                elif event.key == pygame.K_UP:
                    playerInput['up'] = False
                elif event.key == pygame.K_DOWN:
                    playerInput['down'] = False

        # Early Frame Code
        if playerInput['left']:
            x -= 5
        if playerInput['right']:
            x += 5
        if playerInput['down']:
            if speed > 0:
                speed -= 5
        if playerInput['up']:
            if speed < 180:
                speed += 1

        if x < 0:
            x = 0
        if x > display_width - tempCar.get_width():
            x = display_width - tempCar.get_width()

        distance += speed

        if speed >= 50:
            score += 1
        if speed >= 100:
            score += 1
        if speed >= 150:
            score += 1

        # Draw Game Objects
        gameDisplay.fill(color_white)

        car(x, y - speed)

        # UI
        debug_display_speed(speed)
        display_score(score)

        # Late Frame Code

        pygame.display.update()
        clock.tick(60)


game_loop()

pygame.quit()
quit()
