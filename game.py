import pygame
import random
# It's unclear whether we need this next line... comment it out for the time being
# from pygame.locals import *

ENABLE_SPLASH_SCREENS = False
DEBUG = True

pygame.init()
random.seed()

clock = pygame.time.Clock()
# framerate
fps = 125

# the width and height of our game window
screen_width = 1000
screen_height = 525

#lane definitions
lanes = [
    int(screen_height * 1/6),
    int(screen_height * 2/6),
    int(screen_height * 3/6),
    int(screen_height * 4/6),
    int(screen_height * 5/6)
]

# the fade & redrawWindow thing doesn't want to work... leaving functions here
# but they're not being called.
def redrawWindow():
    screen.blit(bg, (0, 0))

def fade(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.wait(5)



# The player is the ball in the center of the screen
class Player(pygame.sprite.Sprite):

    starting_lane = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/green_circle.png')
        self.lane = self.starting_lane
        # Set a rectangle for the player to live in. That way we can move it around later.
        self.rect = self.image.get_rect()
        # The coordinates where the rectangle's center should be
        self.rect.center = [int(screen_width / 2), lanes[self.starting_lane-1]]

    def change_lane(self, lane):
        self.rect.center = [int(screen_width / 2), lanes[lane-1]]

    def move_up(self):
        if self.lane != 1:
            self.lane -= 1
            self.change_lane(self.lane)
        
    def move_down(self):
        if self.lane != 5:
            self.lane += 1
            self.change_lane(self.lane)


# Create an enemy shape
class Enemy(pygame.sprite.Sprite):
    move_amount = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blue_square_enemy.png')
        # TODO: change to be a rando number
        self.lane = random.randint(1, 5)
        # Set a rectangle for the enemy to live in. That way we can move it around later.
        self.rect = self.image.get_rect()
        # The coordinates where the rectangle's center should be
        self.rect.center = [screen_width+150, lanes[self.lane-1]]
        if DEBUG:
            print("New enemy created.")

    def move_item(self):
        self.rect.x -= self.move_amount


# Define our game window and give it a title/name
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shapes 'n' Balls")

if ENABLE_SPLASH_SCREENS:
    # studio logo
    bg = pygame.image.load("img/Gizmo Studios_logo.png")
    screen.blit(bg, (0, 0))
    pygame.display.update()
    # need to touch the event queue or updates/wait/tick won't process.
    pygame.event.pump()
    pygame.time.wait(3000)
    #fade(screen_width, screen_height)

    # made with pygame
    bg = pygame.image.load("img/This game was created with Pygame.png")
    screen.blit(bg, (0, 0))
    pygame.display.update()
    # need to touch the event queue or updates/wait/tick won't process.
    pygame.event.pump()
    pygame.time.wait(3000)
    #fade(screen_width, screen_height)

# Create the player sprite and set its position
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

# Create an enemy sprite and set its position
enemy_group = pygame.sprite.Group()

# Set a background for main gameplay
bg = pygame.image.load("img/translucent_lake_bg.png")

# get a time before we start the loop
start = pygame.time.get_ticks()

# Main game loop
run = True
while run:
    clock.tick(fps)

    now = pygame.time.get_ticks()
    # When 2000 ms have passed.
    if now - start > 2500:
        start = now
        new_enemy = Enemy()
        enemy_group.add(new_enemy)

    pop_enemy = None
    for enemy in enemy_group.sprites():
        enemy.move_item()
        if enemy.rect.x < -60:
            pop_enemy = enemy

    if pop_enemy:
        enemy_group.remove(pop_enemy)
        if DEBUG:
            print("POPPED!")
    
    # Draw the background and the player on every loop
    screen.blit(bg, (0, 0))
    player_group.draw(screen)
    enemy_group.draw(screen)

    # Handle events
    for event in pygame.event.get():

        # If the player quit the game or pressed the close-window button, then exit
        # the loop the next time we get back to the top
        if event.type == pygame.QUIT:
            run = False

        # Handle player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_up()
            if event.key == pygame.K_DOWN:
                player.move_down()
    
    # Update the display
    pygame.display.update()

# If we ever exit the loop, quit the game.
pygame.quit()