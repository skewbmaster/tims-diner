import pygame, os, sys, json
from pygame.locals import *
pygame.init()

width, height = 800, 800
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((width,height), HWSURFACE|DOUBLEBUF|NOFRAME)
clock = pygame.time.Clock()

def slideAnim(position, start, end, maxspeed):
    dx, dy = end[0] - position[0], end[1] - position[1]
    fx = dx / (end[0]-start[0])
    newspeedx = (-((2*fx - 1)**2) + 1) * maxspeed
    return (position[0]+newspeedx, 350)

go = False
data = [(50,350), (49,350), 10]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                go = True

    screen.fill((0,0,0))

    pygame.draw.rect(screen, (255,255,255), [data[0], (100,100)])

    if go:
        data[0] = slideAnim(data[0], data[1], (650,350), data[2])

    pygame.display.update()
    clock.tick(75)
