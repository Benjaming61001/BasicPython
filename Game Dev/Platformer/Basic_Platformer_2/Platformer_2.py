import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# Define font
font = pygame.font.SysFont('Press Start K', 50)
font_score = pygame.font.SysFont('Press Start K', 30)

# Define game variables
tile_size = 50
game_over = 0
main_menu = True
level = 1
max_levels = 7
score = 0

# Define colours
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Load images
sun_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/sun.png')
bg_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/sky.png')
restart_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/restart_btn.png')
start_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/start_btn.png')
exit_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/exit_btn.png')

# Load sounds
pygame.mixer.music.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sfx/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sfx/img_coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sfx/img_jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sfx/img_game_over.wav')
game_over_fx.set_volume(0.5)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Funtion to resset level
def reset_level(level):
    player.reset(100, screen_height - 130)
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()

    # Load in level data and create world
    if path.exists(f'D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/levels/level{level}_data'):
        pickle_in = open(f'D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/levels/level{level}_data', 'rb')
        World_data = pickle.load(pickle_in)
    world = World(World_data)

    return world

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button
        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            # Get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == -1:
                    self.image = self.image_left[self.index]
                if self.direction == 1:
                    self.image = self.image_right[self.index]

            # Handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.image_right):
                    self.index = 0
                if self.direction == -1:
                    self.image = self.image_left[self.index]
                if self.direction == 1:
                    self.image = self.image_right[self.index]

            # Add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            
            # Check for collision
            self.in_air = True
            for tile in world.tile_list:
                # Check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # Check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                
            # Check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()
            # Check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()
            # Check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # Check for collision with platform
            for platform in platform_group:
                # Collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Check if below the platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # Check if above the platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # Move sideways with platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # Update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font, red, (screen_width // 2) - 250, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5 

        # Draw player
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.image_right = []
        self.image_left = []
        self.index = 0
        self.counter = 0
        for num in range (1, 5):
            img_right = pygame.image.load(f'D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_right.append(img_right)
            self.image_left.append(img_left)
        self.dead_image = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/ghost.png')
        self.image = self.image_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []

        # Load images
        dirt_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/dirt.png')
        grass_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                col_count += 1 
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        plarform_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/platform.png')
        self.image = pygame.transform.scale(plarform_img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        lava_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/lava.png')
        self.image = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        coin_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/coin.png')
        self.image = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        exit_img = pygame.image.load('D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/asset/sprite/exit.png')
        self.image = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# Load in level data and create world
if path.exists(f'D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/levels/level{level}_data'):
    pickle_in = open(f'D:/BasicPython/Game Dev/Platformer/Basic_Platformer_2/levels/level{level}_data', 'rb')
    World_data = pickle.load(pickle_in)
world = World(World_data)

# Create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu:
        if start_button.draw():
            main_menu = False
        if exit_button.draw():
            run = False

    else:
        world.draw()

        if game_over == 0:
            blob_group.update()
            platform_group.update()
            # Update score
            # Check if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text('X ' + str(score), font_score, white, tile_size + 8, 12)

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        # If player has died
        if game_over == -1:
            if restart_button.draw():
                World_data = []
                world = reset_level(level)
                game_over = 0
                score = 0

        # If player has completes the level
        if game_over == 1:
            # Reset game and go to next level
            level += 1
            if level <= max_levels:
                # Reset level
                World_data = []
                world = reset_level(level)
                game_over = 0
            else:
                #restart game
                draw_text('YOU WIN!', font, red, (screen_height // 2) - 250, screen_height // 2)
                if restart_button.draw():
                    level = 1
                    World_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()