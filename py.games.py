import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
GRAVITY = 1
JUMP_HEIGHT = -15
ENEMY_SPEED = 5
PROJECTILE_SPEED = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load stick figure image
         # Load stick figure image
        image_path = os.path.join("images", "player.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - PLAYER_SIZE)
        self.velocity = 0
        self.jump = False
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_SPACE] and not self.jump:
            self.velocity = JUMP_HEIGHT
            self.jump = True

        # Apply gravity
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Check for ground collision
        if self.rect.y >= HEIGHT - PLAYER_SIZE:
            self.rect.y = HEIGHT - PLAYER_SIZE
            self.jump = False

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - PLAYER_SIZE

    def update(self):
        self.rect.x -= ENEMY_SPEED
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = HEIGHT - PLAYER_SIZE

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = player_rect.x + PLAYER_SIZE
        self.rect.y = player_rect.y + PLAYER_SIZE // 2

    def update(self):
        self.rect.x += PROJECTILE_SPEED
        if self.rect.left > WIDTH:
            self.kill()

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple 2D Game")
    clock = pygame.time.Clock()

    player = Player()
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    level = 1
    score = 0
    health = 100
    lives = 3

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Shoot projectiles on key press
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                projectile = Projectile(player.rect)
                all_sprites.add(projectile)
                projectiles.add(projectile)

        # Update
        all_sprites.update()
        enemies.update()
        projectiles.update()

        # Check for collisions
        if pygame.sprite.spritecollide(player, enemies, True):
            health -= 10

        if pygame.sprite.groupcollide(projectiles, enemies, True, True):
            score += 10

        # Draw
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        enemies.draw(screen)
        projectiles.draw(screen)

        # Display score, health, and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        health_text = font.render(f"Health: {health}%", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))
        screen.blit(lives_text, (10, 90))

        pygame.display.flip()
        clock.tick(30)

        # Increase difficulty with levels
        if score >= level * 100:
            level += 1
            for _ in range(level):
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Check for game over
        if health <= 0:
            lives -= 1
            if lives == 0:
                print("Game Over")
                pygame.quit()
                sys.exit()
            else:
                health = 100

if __name__ == "__main__":
    main()
