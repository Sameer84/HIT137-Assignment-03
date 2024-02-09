import pygame
import sys
import random

#Initialize Pygame
pygame.init()

#Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Human-like Character Game")

#Clock for controlling the frame rate
clock = pygame.time.Clock()

#Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create the player's image
        self.image = pygame.Surface((30, 90))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midleft=(100, HEIGHT - 150))  # Adjusted position for the character
        self.speed = 5
        self.jump_height = -20
        self.gravity = 1
        self.vel_y = 0
        self.health = 100
        self.lives = 3

    def update(self):
        #Get keyboard input for player movement and jumping
        keys = pygame.key.get_pressed()
        self.vel_y += self.gravity

        #Move left and right
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        #Jump when spacebar is pressed
        if keys[pygame.K_SPACE] and self.rect.bottom >= HEIGHT:
            self.vel_y = self.jump_height

        #Apply gravity
        self.rect.y += self.vel_y

        #Check if the player is on the ground
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0

#Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #Create the projectile's image
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midleft=(x, y))  #Adjusted position for the projectile
        self.speed = 8

    def update(self):
        #Move projectile horizontally
        self.rect.x += self.speed
        #Remove projectile if it goes out of the screen
        if self.rect.x > WIDTH:
            self.kill()

#Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Create the enemy's image
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(midright=(WIDTH, random.randint(0, HEIGHT - 50)))  #Adjusted position for the enemy
        self.speed = random.randint(3, 6)

    def update(self):
        #Move enemy towards the left
        self.rect.x -= self.speed
        #Remove enemy if it goes out of the screen
        if self.rect.right < 0:
            self.kill()

#Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Create the collectible's image
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midright=(WIDTH, random.randint(0, HEIGHT - 30)))  #Adjusted position for the collectible
        self.speed = 3

    def update(self):
        #Move collectible towards the left
        self.rect.x -= self.speed
        #Remove collectible if it goes out of the screen
        if self.rect.right < 0:
            self.kill()

#Create sprite groups
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

#Create player
player = Player()
all_sprites.add(player)

#Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                #Create projectile when spacebar is pressed
                projectile = Projectile(player.rect.right, player.rect.centery - 5)
                projectiles.add(projectile)
                all_sprites.add(projectile)

    #Spawn enemies randomly
    if random.randint(1, 100) < 4:
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)

    #Spawn collectibles randomly
    if random.randint(1, 300) == 1:
        collectible = Collectible()
        collectibles.add(collectible)
        all_sprites.add(collectible)

    #Update all sprites
    all_sprites.update()

    #Check for collisions
    for enemy in pygame.sprite.spritecollide(player, enemies, True):
        #Decrease player's health when colliding with enemies
        player.health -= 10
        #Check for game over conditions
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            if player.lives == 0:
                running = False

    for enemy, projectile in pygame.sprite.groupcollide(enemies, projectiles, True, True).items():
        #Handle collisions between enemies and projectiles (e.g., increase score)
        pass

    for collectible in pygame.sprite.spritecollide(player, collectibles, True):
        #Handle collection of collectibles (e.g., health boost, extra life)
        pass

    #Draw all sprites
    screen.fill(BLACK)
    all_sprites.draw(screen)

    #Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, player.health * 2, 20))

    #Draw remaining lives
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 150, 10))

    #Update display
    pygame.display.flip()

    #Cap the frame rate
    clock.tick(FPS)

#Quit Pygame
pygame.quit()
sys.exit()