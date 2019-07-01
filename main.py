import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Bee Racer')
clock = pygame.time.Clock()

carImg = pygame.image.load('assets/sprites/F1Car.png')


def obstacles(x, y, w, h, color):
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])


def car(x, y, debugHitbox=False):
    if debugHitbox:
        pygame.draw.rect(gameDisplay, color_green, [
                         x, y, carImg.get_width(), carImg.get_height()])
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, color=color_black, bgColor=color_white):
    gameDisplay.fill(bgColor)

    textStyle = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, textStyle, color)
    TextRect.center = ((display_width / 2, display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()


def crash():
    time.sleep(0.5)
    message_display('Game Over!', color_red, color_black)


def game_loop():
    x = (display_width * 0.5 - carImg.get_width()/2)
    y = (display_height * 0.75 - carImg.get_height()/2)

    obstacle_startX = random.randrange(0, display_width)
    obstacle_startY = -100
    obstacle_speed = 10
    obstacle_width = 100
    obstacle_height = 100

    playerInput = dict(
        left=False,
        right=False,
        up=False,
        down=False,
        fire=False,
    )

    gameExit = False
    crashed = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerInput['left'] = True
                elif event.key == pygame.K_RIGHT:
                    playerInput['right'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    playerInput['left'] = False
                elif event.key == pygame.K_RIGHT:
                    playerInput['right'] = False

        if playerInput['left']:
            x -= 5
        if playerInput['right']:
            x += 5

        gameDisplay.fill(color_white)

        obstacle_startY += obstacle_speed

        car(x, y, True)

        obstacles(obstacle_startX, obstacle_startY,
                  obstacle_width, obstacle_height, color_black)

        if x < 0 or x > display_width - carImg.get_width():
            crash()

        if obstacle_startY > display_height:
            obstacle_startY = -obstacle_height
            obstacle_startX = random.randrange(0, display_width)

        if y < obstacle_startY + obstacle_height:
            if x > obstacle_startX and x < obstacle_startX + obstacle_width or x + carImg.get_width() > obstacle_startX and x + carImg.get_width() < obstacle_startX + obstacle_width:
                crash()

        pygame.display.update()
        clock.tick(60)


game_loop()

pygame.quit()
quit()
