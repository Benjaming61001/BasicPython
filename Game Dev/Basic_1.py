import pygame
import sys

pygame.init()

WIDTH = 500
HEIGHT = 500

black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic_1")

x = 50
y = 50
width = 40
height = 60
vel = 20

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and y > 0:
        y -= vel
        if y < 0:
            y = 0
    if keys[pygame.K_DOWN] and y < HEIGHT - height:
        y += vel
        if y > HEIGHT - height:
            y = HEIGHT - height
    if keys[pygame.K_LEFT] and x > 0:
        x -= vel
        if x < 0:
            x = 0
    if keys[pygame.K_RIGHT] and x < WIDTH - width:
        x += vel
        if x > WIDTH - width:
            x = WIDTH - width


    screen.fill(black)
    pygame.draw.rect(screen, white, (x, y, width, height))
    pygame.display.update()

pygame.quit()
