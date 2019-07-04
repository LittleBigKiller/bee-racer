import pygame
import time

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

lightgray = (191, 191, 191)
gray = (127, 127, 127)
darkgray = (63, 63, 63)

gameDisplay = pygame.display.set_mode((800, 600))

gameDisplay.fill(lightgray)

pixAr = pygame.PixelArray(gameDisplay)

pixAr[10][20] = red

pygame.draw.line(gameDisplay, blue, (100, 200), (300, 450), 5)

pygame.draw.rect(gameDisplay, green, (400, 400, 25, 50))

pygame.draw.circle(gameDisplay, white, (450, 150), 100)

pygame.draw.polygon(gameDisplay, black, ((300, 0),
                                         (300, 300), (600, 150), (200, 500)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
