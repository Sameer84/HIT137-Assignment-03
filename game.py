import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Human-like Character Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(100, HEIGHT - 150, 30, 90)  # Adjusted position and size for the character
        self.speed = 5
        self.jump_height = -20  # Increased jump height
        self.gravity = 1
        self.vel_y = 0
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        self.vel_y += self.gravity

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.rect.bottom >= HEIGHT:
            self.vel_y = self.jump_height

        self.rect.y += self.vel_y

        # Check if the player is on the ground
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 10, 10)  # Adjusted position for the projectile
        self.speed = 8

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - 50), 30, 30)  # Adjusted position for the enemy
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - 30), 20, 20)  # Adjusted position for the collectible
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                projectile = Projectile(player.rect.right, player.rect.centery - 5)
                projectiles.add(projectile)
                all_sprites.add(projectile)

    # Spawn enemies
    if random.randint(1, 100) < 4:
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)

    # Spawn collectibles
    if random.randint(1, 300) == 1:
        collectible = Collectible()
        collectibles.add(collectible)
        all_sprites.add(collectible)

    # Update
    all_sprites.update()

    # Check for collisions
    for enemy in pygame.sprite.spritecollide(player, enemies, True):
        player.health -= 10
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            if player.lives == 0:
                running = False

    for enemy, projectile in pygame.sprite.groupcollide(enemies, projectiles, True, True).items():
        # Increase score or other actions for defeating enemies
        pass

    for collectible in pygame.sprite.spritecollide(player, collectibles, True):
        # Implement actions for collecting items (e.g., health boost, extra life)
        pass

    # Draw
    screen.fill(BLACK)

    # Draw the player
    pygame.draw.ellipse(screen, WHITE, player.rect)  # Head
    pygame.draw.rect(screen, WHITE, (player.rect.left + 7, player.rect.top + 15, 5, 20))  # Body
    pygame.draw.line(screen, WHITE, (player.rect.left + 2, player.rect.top + 18), (player.rect.left - 10, player.rect.top + 25), 2)  # Left arm
    pygame.draw.line(screen, WHITE, (player.rect.right + 3, player.rect.top + 18), (player.rect.right + 13, player.rect.top + 25), 2)  # Right arm
    pygame.draw.line(screen, WHITE, (player.rect.left + 7, player.rect.bottom), (player.rect.left + 3, player.rect.bottom + 10), 2)  # Left leg
    pygame.draw.line(screen, WHITE, (player.rect.right - 3, player.rect.bottom), (player.rect.right - 7, player.rect.bottom + 10), 2)  # Right leg

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy.rect)

    # Draw collectibles
    for collectible in collectibles:
        pygame.draw.rect(screen, WHITE, collectible.rect)

    # Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, player.health * 2, 20))

    # Draw lives
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 150, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
