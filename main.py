import math
import random
import time

import pygame

pygame.init()

display_width = 1280
display_height = 720

color_black = (0, 0, 0)
color_white = (255, 255, 255)

color_lightgray = (191, 191, 191)
color_gray = (127, 127, 127)
color_darkgray = (63, 63, 63)

color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)

color_cyan = (0, 255, 255)
color_magenta = (255, 0, 255)
color_yellow = (255, 255, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height + 80))
pygame.display.set_caption('bee-racer')
clock = pygame.time.Clock()

settings_imagesize = 20
settings_maxlaps = 3
settings_p0KeyLeft = pygame.K_LEFT
settings_p1KeyLeft = pygame.K_a
settings_p2KeyLeft = pygame.K_f
settings_p3KeyLeft = pygame.K_j
settings_bgpattern = pygame.image.load('assets/backgrounds/pat_grass.jpg')

players = []
gameOver = False
winner = -1
player_count = 2


def checkinputs(event):
    if event.type == pygame.KEYDOWN:
        if event.key == settings_p0KeyLeft:
            try:
                players[0].turnL = True
            except IndexError:
                return
        elif event.key == settings_p1KeyLeft:
            try:
                players[1].turnL = True
            except IndexError:
                return
        elif event.key == settings_p2KeyLeft:
            try:
                players[2].turnL = True
            except IndexError:
                return
        elif event.key == settings_p3KeyLeft:
            try:
                players[3].turnL = True
            except IndexError:
                return

    if event.type == pygame.KEYUP:
        if event.key == settings_p0KeyLeft:
            try:
                players[0].turnL = False
            except IndexError:
                return
        elif event.key == settings_p1KeyLeft:
            try:
                players[1].turnL = False
            except IndexError:
                return
        elif event.key == settings_p2KeyLeft:
            try:
                players[2].turnL = False
            except IndexError:
                return
        elif event.key == settings_p3KeyLeft:
            try:
                players[3].turnL = False
            except IndexError:
                return


def createPlayer():
    newPlayer = Player(len(players))

    newPlayer.updateVel(0)
    newPlayer.draw()

    players.append(newPlayer)


class Player:
    def __init__(self, ident):
        self.ident = ident
        # Set movement parameters
        self.v = 5
        self.x = 340
        self.y = 560 + ident * 40
        self.vx = 0
        self.vy = 0
        self.a = math.pi / 2

        # Set lap counting variables
        self.holdStart = 0
        self.doChecks = True
        self.check0 = True
        self.check1 = True
        self.check2 = True
        self.check3 = True
        self.lapCount = 0

        # Set player color
        if ident == 0:
            self.color = (0, 0, 0)
        elif ident == 1:
            self.color = (255, 0, 0)
        elif ident == 2:
            self.color = (0, 255, 0)
        elif ident == 3:
            self.color = (0, 0, 255)

        # Misc variables
        self.trail = []
        self.alive = True
        self.turnL = False
        self.image = pygame.image.load(
            'assets/sprites/p' + str(ident) + '.png')
        self.image = pygame.transform.scale(
            self.image, (settings_imagesize, settings_imagesize))

    def updateVel(self, angle):
        self.a += angle
        self.vx = self.v * math.sin(self.a)
        self.vy = self.v * math.cos(self.a)

    def holdChecks(self):
        self.holdStart = pygame.time.get_ticks()
        self.doChecks = False

    def resumeChecks(self):
        if not self.doChecks and pygame.time.get_ticks() - self.holdStart >= 200:
            self.doChecks = True

    def draw(self):
        dispImage = pygame.transform.rotate(self.image, math.degrees(self.a))
        gameDisplay.blit(
            dispImage, (self.x - settings_imagesize / 2, self.y - settings_imagesize / 2))

    def updateLapCounter(self):
        font = pygame.font.SysFont(None, 36)
        text = font.render('Player ' + str(self.ident), True, self.color)
        gameDisplay.blit(text, (80 + self.ident * 320, 730))
        if self.alive:
            text = font.render('Lap: ' + str(self.lapCount) +
                               '/' + str(settings_maxlaps), True, self.color)
            gameDisplay.blit(text, (80 + self.ident * 320, 760))
        else:
            text = font.render('DEAD', True, self.color)
            gameDisplay.blit(text, (80 + self.ident * 320, 760))


""" def display_score(value):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(value), True, color_black)
    gameDisplay.blit(text, (5, 5))
    pygame.display.update() """


def checkAlive():
    global gameOver
    global winner
    aliveCount = 0
    for player in players:
        if player.alive:
            winner = player.ident
            aliveCount += 1
    if aliveCount == 1:
        gameOver = True


def draw_map():
    # Outside the road
    gameDisplay.fill(color_green)

    # Road
    pygame.draw.circle(gameDisplay, color_lightgray, (int(
        display_height / 2), int(display_height / 2)), int(display_height / 2 - 10))
    pygame.draw.circle(gameDisplay, color_white, (int(
        display_height / 2), int(display_height / 2)), int(display_height / 2 - 10), 4)

    pygame.draw.circle(gameDisplay, color_lightgray, (int(
        display_width - display_height / 2), int(display_height / 2)), int(display_height / 2 - 10))
    pygame.draw.circle(gameDisplay, color_white, (int(
        display_width - display_height / 2), int(display_height / 2)), int(display_height / 2 - 10), 4)

    pygame.draw.rect(gameDisplay, color_lightgray, (int(display_height / 2),
                                                    10, int(display_width - display_height + 20), int(display_height - 20)))
    pygame.draw.line(gameDisplay, color_white, (int(
        display_height / 2), 11), (int(display_width - display_height / 2 + 20), 11), 4)
    pygame.draw.line(gameDisplay, color_white, (int(display_height / 2), int(display_height - 13)),
                     (int(display_width - display_height / 2 + 20), int(display_height - 13)), 4)

    # Inside the road
    pygame.draw.circle(gameDisplay, color_green, (int(
        display_height / 2), int(display_height / 2)), 170)
    pygame.draw.circle(gameDisplay, color_white, (int(
        display_height / 2), int(display_height / 2)), 170, 4)

    pygame.draw.circle(gameDisplay, color_green, (int(
        display_width - display_height / 2), int(display_height / 2)), 170)
    pygame.draw.circle(gameDisplay, color_white, (int(
        display_width - display_height / 2), int(display_height / 2)), 170, 4)

    pygame.draw.rect(gameDisplay, color_green, (int(display_height / 2),
                                                int(display_height / 2) - 170, int(display_width - display_height), 340))
    pygame.draw.line(gameDisplay, color_white, (int(display_height / 2), int(
        display_height / 2) - 170), (int(display_width - display_height / 2), int(
            display_height / 2) - 170), 4)
    pygame.draw.line(gameDisplay, color_white, (int(display_height / 2), int(display_height / 2) + 168),
                     (int(display_width - display_height / 2), int(display_height / 2) + 168), 4)

    # Start line
    pygame.draw.line(gameDisplay, color_white, (display_height / 2, 3 *
                                                display_height / 4 - 10), (display_height / 2, display_height - 11), 4)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def intro_loop():
    global player_count
    stopIntro = False

    leftHL = False

    rightHL = False

    while not stopIntro:

        gameDisplay.fill(color_white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    leftHL = True
                    if player_count > 1:
                        player_count -= 1
                elif event.key == pygame.K_RIGHT:
                    rightHL = True
                    if player_count < 4:
                        player_count += 1
                elif event.key == pygame.K_SPACE:
                    stopIntro = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    leftHL = False
                elif event.key == pygame.K_RIGHT:
                    rightHL = False

        # Player Count Display
        textStyle = pygame.font.Font('freesansbold.ttf', 120)
        TextSurf, TextRect = text_objects(
            str(player_count), textStyle, color_red)
        TextRect.midtop = ((display_width / 2, 250))
        pygame.draw.rect(gameDisplay, color_green,
                         (TextRect.topleft[0] - 80, TextRect.topleft[1], 200, 121))
        gameDisplay.blit(TextSurf, TextRect)
        print(TextRect.midtop)

        # Arrow Left
        if leftHL:
            leftBGColor = color_red
            leftTextColor = color_green
        else:
            leftBGColor = color_green
            leftTextColor = color_red

        textStyle = pygame.font.Font('freesansbold.ttf', 120)
        TextSurf, TextRect = text_objects(
            '<', textStyle, leftTextColor)
        TextRect.topright = ((display_width / 2 - 50, 250))
        pygame.draw.rect(gameDisplay, leftBGColor,
                         TextRect)
        gameDisplay.blit(TextSurf, TextRect)

        # Arrow Right
        if rightHL:
            rightBGColor = color_red
            rightTextColor = color_green
        else:
            rightBGColor = color_green
            rightTextColor = color_red

        textStyle = pygame.font.Font('freesansbold.ttf', 120)
        TextSurf, TextRect = text_objects(
            '>', textStyle, rightTextColor)
        TextRect.topleft = ((display_width / 2 + 50, 250))
        pygame.draw.rect(gameDisplay, rightBGColor,
                         TextRect)
        gameDisplay.blit(TextSurf, TextRect)

        # Player Count Label
        textStyle = pygame.font.Font('freesansbold.ttf', 60)
        TextSurf, TextRect = text_objects(
            'Number of Players:', textStyle, color_blue)

        TextRect.midtop = ((display_width / 2, 180))
        gameDisplay.blit(TextSurf, TextRect)

        # Top banner
        pygame.draw.rect(gameDisplay, color_darkgray,
                         [0, 0, display_width, 128])
        textStyle = pygame.font.Font('freesansbold.ttf', 120)
        TextSurf, TextRect = text_objects(
            'Bee Racer', textStyle, color_green)

        TextRect.midtop = ((display_width / 2, 10))
        gameDisplay.blit(TextSurf, TextRect)

        # Press Space Info:
        textStyle = pygame.font.Font('freesansbold.ttf', 40)
        TextSurf, TextRect = text_objects(
            'Press \'Space\' to start the game', textStyle, color_yellow)
        TextRect.midtop = ((display_width / 2, 720))
        pygame.draw.rect(gameDisplay, color_blue,
                         TextRect)
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(60)


def winner_loop(winner):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        textStyle = pygame.font.Font('freesansbold.ttf', 120)
        gameDisplay.fill(color_gray)
        if winner == 0:
            TextSurf, TextRect = text_objects(
                'Player ' + str(winner) + ' wins!', textStyle, color_black)
        elif winner == 1:
            TextSurf, TextRect = text_objects(
                'Player ' + str(winner) + ' wins!', textStyle, color_red)
        elif winner == 2:
            TextSurf, TextRect = text_objects(
                'Player ' + str(winner) + ' wins!', textStyle, color_green)
        elif winner == 3:
            TextSurf, TextRect = text_objects(
                'Player ' + str(winner) + ' wins!', textStyle, color_blue)

        TextRect.center = ((display_width / 2, display_height / 2 - 20))
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(60)


def loser_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(color_black)

        textStyle = pygame.font.Font('freesansbold.ttf', 120)
        TextSurf, TextRect = text_objects('Game Over!', textStyle, color_red)
        TextRect.center = ((display_width / 2, display_height / 2 - 20))
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(60)


def game_loop():
    global player_count
    for i in range(0, player_count):
        createPlayer()

    global gameOver
    global winner

    gameOver = False
    winner = -1

    while not gameOver:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            checkinputs(event)

        # Draw Map
        draw_map()

        # Draw UI Background
        pygame.draw.rect(gameDisplay, color_darkgray, [0, 720, 1280, 80])

        # Player handling
        for player in players:
            if player.alive and not gameOver:

                # Trail drawing
                point_old = {'x': player.x, 'y': player.y}
                for point in player.trail:
                    pygame.draw.line(
                        gameDisplay, player.color, (point_old['x'], point_old['y']), (point['x'], point['y']), 8)
                    point_old = point

                # Player drawing
                player.draw()

                # Player input action
                if player.turnL:
                    player.updateVel(0.05)

                # Player movement
                player.x += player.vx
                player.y += player.vy

                # Trail size handling
                player.trail.insert(0, {'x': player.x, 'y': player.y})
                if len(player.trail) == 64:
                    player.trail.pop()

                # Collision check
                if player.x > 368 and player.x < 912:
                    if player.y + settings_imagesize / 2 > 18 and player.y - settings_imagesize / 2 < 182:
                        pass
                    elif player.y + settings_imagesize / 2 > 538 and player.y - settings_imagesize / 2 < 702:
                        pass
                    else:
                        player.alive = False
                        player.updateLapCounter()
                        if len(players) == 1:
                            gameOver = True
                        checkAlive()
                else:
                    dx0 = player.x - display_height / 2
                    dy0 = player.y - display_height / 2
                    dist0 = math.sqrt(dx0 * dx0 + dy0 * dy0)

                    dx1 = player.x - display_width + display_height / 2
                    dy1 = player.y - display_height / 2
                    dist1 = math.sqrt(dx1 * dx1 + dy1 * dy1)

                    if dist0 + settings_imagesize / 2 > 178 and dist0 - settings_imagesize / 2 < display_height / 2 - 18:
                        pass
                    elif dist1 + settings_imagesize / 2 > 178 and dist1 - settings_imagesize / 2 < display_height / 2 - 18:
                        pass
                    else:
                        player.alive = False
                        player.updateLapCounter()
                        if len(players) == 1:
                            gameOver = True
                        checkAlive()

                # Lap checks
                player.resumeChecks()
                if player.x > 635 and player.x < 645 and player.doChecks:
                    player.holdChecks()
                    if player.check1:
                        player.check3 = True
                        print('Player ' + str(player.ident) +
                              ' passed checkpoint 3')
                    else:
                        player.check1 = True
                        print('Player ' + str(player.ident) +
                              ' passed checkpoint 1')
                if player.y > 355 and player.y < 375 and player.doChecks:
                    player.holdChecks()
                    if player.check0:
                        player.check2 = True
                        print('Player ' + str(player.ident) +
                              ' passed checkpoint 2')
                    else:
                        player.check0 = True
                        print('Player ' + str(player.ident) +
                              ' passed checkpoint 0')
                if player.x > 355 and player.x < 375:
                    if player.check0 and player.check1 and player.check2 and player.check3:
                        if player.lapCount != 0:
                            print('Player ' + str(player.ident) +
                                  ' finished a lap')
                        player.check0 = False
                        player.check1 = False
                        player.check2 = False
                        player.check3 = False
                        player.lapCount += 1
                        if player.lapCount > settings_maxlaps:
                            winner = player.ident
                            gameOver = True

            else:
                # Draw dead players trail till it vanishes
                if len(player.trail) != 0:
                    player.trail.pop()

                    point_old = {'x': player.x, 'y': player.y}
                    for point in player.trail:
                        pygame.draw.line(
                            gameDisplay, player.color, (point_old['x'], point_old['y']), (point['x'], point['y']), 8)
                        point_old = point

                player.draw()

        # Update Scoreboard
        for player in players:
            player.updateLapCounter()

        pygame.display.update()
        clock.tick(60)

    if winner != -1:
        winner_loop(winner)
    else:
        loser_loop()


intro_loop()
game_loop()

pygame.quit()
quit()
