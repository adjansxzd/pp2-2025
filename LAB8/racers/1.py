import pygame
import random
import time

pygame.init() # initializes all the pygame sub-modules

# Set screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCORE = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # creating a game window
# set_mode() takes a tuple as an argument

# Load images
image_background = pygame.image.load('AnimatedStreet.png')
image_player = pygame.image.load('Player.png')
image_enemy = pygame.image.load('Enemy.png')
image_coin = pygame.image.load("Coin.png")

# Load and play background music
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1) # -1 means infinite loop
sound_crash = pygame.mixer.Sound('crash.wav')
sound_coin = pygame.mixer.Sound('coin_hit.mp3')
# Create fonts
font = pygame.font.SysFont("Verdana", 60) 
font_small = pygame.font.SysFont("Verdana", 20)
# Game over text
image_game_over = font.render("Game Over", True, "black") # Font.render(text, antialias, color, background=None)
image_game_over_rect = image_game_over.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # centers the text

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2 # start at this point(horizontally centered)
        self.rect.bottom = SCREEN_HEIGHT # at the bottom
        self.speed = 3 # my speed

    def move(self): # move_ip moves rect in position (x, y)
        keys = pygame.key.get_pressed() # check key presses
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0,5)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        # Prevent player from going off the boundaries    
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 7
        
    def generate_random_rect(self):
        self.rect.left = random.randint(0, SCREEN_WIDTH - self.rect.w)
        self.rect.bottom = 0 # start at top of screen but randomly

    def move(self):
        self.rect.move_ip(0, self.speed) # move enemy down
        if self.rect.top > SCREEN_HEIGHT: # if it leaves screen...
            self.generate_random_rect() # ..respawn at the top
#Class coin random
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(image_coin, (30, 30))
        self.rect = self.image.get_rect()
        self.generate_random_position()

    def generate_random_position(self):
        self.rect.left = random.randint(50, SCREEN_WIDTH - 50)
        self.rect.top = random.randint(100, SCREEN_HEIGHT - 200)

    def move(self): # moneta prosto stoit na meste, poka ne collected
        pass        

running = True

# this object allows us to set the FPS
clock = pygame.time.Clock()
FPS = 60
# Create sprites(game objects)
P1 = Player()
E1 = Enemy()
C1 = Coin()
# Create sprtie groups for org and collision checks
all_sprites = pygame.sprite.Group() # Group() makes it easy to draw and update many sprites at once.
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

all_sprites.add(P1, E1, C1)
enemy_sprites.add(E1)
coin_sprites.add(C1)

while running: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:
            running = False

    P1.move()

    screen.blit(image_background, (0, 0))
    # Render and display coin at the top right corner
    coin_text = font_small.render(f"Coins: {SCORE}", True, "black")
    screen.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10)) # screen blit It draws one surface (like an image or text) onto another surface (usually the screen).

    # Move and draw all sprites
    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)
    # Coin collection check
    if pygame.sprite.spritecollideany(P1, coin_sprites):
        sound_coin.play()
        SCORE  += 1    
        C1.generate_random_position()
    # Collision with enemy check
    if pygame.sprite.spritecollideany(P1, enemy_sprites): # This function checks if one sprite is colliding with any sprite in a group.
        sound_crash.play()
        time.sleep(1)
        # Show game over screen
        running = False
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip() # updates the screen

        time.sleep(2)
        
    
    pygame.display.flip() # updates the screen
    clock.tick(FPS) # sets the FPS

pygame.quit()