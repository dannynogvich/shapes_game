import pygame
import random

ENABLE_SPLASH_SCREENS = False
DEBUG = True

pygame.init()
random.seed()

clock = pygame.time.Clock()
# starting framerate
fps = 125
game_over = False
level_clear = False

# the shape we want to hit for points
desired_shape = "square"

# the width and height of our game window
screen_width = 1000
screen_height = 525

pygame.mixer.init()
game_over_channel = pygame.mixer.Channel(5)
level_clear_channel = pygame.mixer.Channel(6)

#Set up the sound effects
game_over_sound = pygame.mixer.Sound("sounds/game_over_sound_effect.mp3")
level_clear_sound = pygame.mixer.Sound("sounds/level_clear_sound_effect.mp3")

#lane definitions
lanes = [
    int(screen_height * 1/6),
    int(screen_height * 2/6),
    int(screen_height * 3/6),
    int(screen_height * 4/6),
    int(screen_height * 5/6)
]

# The player is the ball in the center of the screen
class Player(pygame.sprite.Sprite):

    starting_lane = 3
    player_score = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lane = self.starting_lane
        self.mouth_open()

    def mouth_open(self):
        self.image = pygame.image.load('img/player_player_mouth_open.png')
        self.rect = self.image.get_rect()
        self.rect.center = [int(screen_width / 2), lanes[self.lane-1]]

        self.mouth = 'open'
        
    def mouth_closed(self):
        self.image = pygame.image.load('img/player_player_mouth_closed.png')
        self.rect = self.image.get_rect()
        self.rect.center = [int(screen_width / 2), lanes[self.lane-1]]

        self.mouth = 'closed'

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
    collided = False
    images = [
        { "shape": "square",    "img": "burger_enemy.png"    },
        { "shape": "triangle",  "img": "fries_enemy.png"  },
        { "shape": "rectangle", "img": "sub_enemy.png" },
        { "shape": "circle",    "img": "beverage_enemy.png"    },
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        enemy_data = self.images[random.randint(0, 3)]
        self.image = pygame.image.load('img/' + enemy_data["img"])
        self.shape = enemy_data["shape"]
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

    # made with pygame
    bg = pygame.image.load("img/This game was created with Pygame.png")
    screen.blit(bg, (0, 0))
    pygame.display.update()
    # need to touch the event queue or updates/wait/tick won't process.
    pygame.event.pump()
    pygame.time.wait(3000)

# Create the player sprite and set its position
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

# Create an enemy sprite and set its position
enemy_group = pygame.sprite.Group()

# Set a background for main gameplay
bg = pygame.image.load("img/translucent_lake_bg.png")

# for text 
font = pygame.font.Font('freesansbold.ttf', 32)
game_over_font = pygame.font.Font('freesansbold.ttf', 75)
level_clear_font = pygame.font.Font('freesansbold.ttf', 75)
game_over_option_1_font = pygame.font.Font('freesansbold.ttf', 15)

#Setting up the blurred overlay
blurred_overlay = pygame.image.load("img/transparent_white.png")

# get a time before we start the loop
start = pygame.time.get_ticks()
mouth_timer = pygame.time.get_ticks()

# Main game loop
run = True
while run:
    clock.tick(fps)

    now = pygame.time.get_ticks()

    if game_over:
        for enemy in enemy_group.sprites():
            enemy.kill()

    # When 2500 ms have passed.
    if not game_over:
        if now - start > 2500:
            start = now
            new_enemy = Enemy()
            enemy_group.add(new_enemy)
        if player.mouth == 'closed' and now - mouth_timer > 2000:
            player.mouth_open()

        for enemy in enemy_group.sprites():
            enemy.move_item()
            if enemy.rect.x < -160:
                enemy.kill()
            if enemy.rect.colliderect(player.rect):
                if not enemy.collided:
                    enemy.collided = True
                    enemy.kill()
                    if enemy.shape == desired_shape:
                        player.player_score += 1
                        player.mouth_closed()
                        mouth_timer = pygame.time.get_ticks()

                    else:
                        game_over = True
                        game_over_playsound = True
                        game_over_timer = pygame.time.get_ticks()
                    if  DEBUG:
                        print("collided")

        if player.player_score == 1:
            level_clear = True


    # Draw the background and the player on every loop
    screen.blit(bg, (0, 0))
    player_group.draw(screen)
    enemy_group.draw(screen)
    score = font.render(str(player.player_score),True,(255,255,255))
    screen.blit(score, (20,0))

    if game_over:
        screen.blit(blurred_overlay, (0, 0))
        player.player_score = 0
        death_text = game_over_font.render(str("Game Over"),True,(255,0,0))
        game_over_option_1_text = game_over_option_1_font.render(str("Press Any Key to Play Again"), True, (255, 255, 255))
        screen.blit(death_text, (300,125))
        screen.blit(game_over_option_1_text, (400, 275))
        if game_over_playsound:
            game_over_playsound = False
            game_over_channel.play(game_over_sound)

    if level_clear:
        screen.blit(blurred_overlay, (0, 0))
        level_clear_text = level_clear_font.render(str("Level Clear!"),True,(0,255,255))
        screen.blit(level_clear_text, (300,125))
        if not level_clear_channel.get_busy():
            level_clear_channel.play(level_clear_sound)
            

    # Handle events
    for event in pygame.event.get():

        # If the player quit the game or pressed the close-window button, then exit
        # the loop the next time we get back to the top
        if event.type == pygame.QUIT:
            run = False

        # Handle player movement
        if event.type == pygame.KEYDOWN:
            if game_over:
                game_over = False
            elif event.key == pygame.K_UP:
                player.move_up()
            elif event.key == pygame.K_DOWN:
                player.move_down()
    
    # Update the display
    pygame.display.update()

# If we ever exit the loop, quit the game.
pygame.quit()
