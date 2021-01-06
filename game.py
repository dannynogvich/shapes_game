import pygame
# It's unclear whether we need this next line... comment it out for the time being
# from pygame.locals import *

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/green_circle.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


screen_width = 800
screen_height = 600
player_x = int(screen_width / 2)
player_y = int(screen_height / 2)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shapes 'n' Balls")

player_group = pygame.sprite.Group()
player = Player(player_x, player_y)
player_group.add(player)


bg = pygame.image.load("img/background.png")

run = True
while run:
    screen.blit(bg, (0, 0))
    player_group.draw(screen)

    player.rect.x -= 3 
    player.rect.y -= 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()
