import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
player_img = pygame.Surface((50, 30))
player_img.fill(WHITE)
enemy_img = pygame.Surface((50, 30))
enemy_img.fill(RED)
bullet_img = pygame.Surface((5, 10))
bullet_img.fill(WHITE)


# Classes
class Player:
    def __init__(self):
        self.rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.score = 0

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def draw(self):
        screen.blit(player_img, self.rect)


class Enemy:
    def __init__(self, x, y):
        self.rect = enemy_img.get_rect(topleft=(x, y))
        self.direction = 1  # 1 for right, -1 for left

    def move(self):
        self.rect.x += self.direction * 3
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1  # Change direction
            self.rect.y += 10  # Move down

    def draw(self):
        screen.blit(enemy_img, self.rect)


class Bullet:
    def __init__(self, x, y):
        self.rect = bullet_img.get_rect(center=(x, y))

    def move(self):
        self.rect.y -= 10

    def draw(self):
        screen.blit(bullet_img, self.rect)


# Function to create enemies
def create_enemies(level):
    enemies = []
    for i in range(5 * level):  # Increase number of enemies per level
        x = random.randint(0, WIDTH - 50)
        y = random.randint(30, 150)
        enemies.append(Enemy(x, y))
    return enemies


# Game loop
def main():
    clock = pygame.time.Clock()
    player = Player()
    level = 1
    enemies = create_enemies(level)
    bullets = []
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-5)
        if keys[pygame.K_RIGHT]:
            player.move(5)
        if keys[pygame.K_SPACE]:
            bullets.append(Bullet(player.rect.centerx, player.rect.top))

        # Move bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        # Move enemies
        for enemy in enemies[:]:
            enemy.move()

        # Draw enemies
        for enemy in enemies:
            enemy.draw()

        # Draw bullets and check for collisions
        for bullet in bullets[:]:
            bullet.draw()
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    player.score += 10  # Increase score
                    break

        # Level up if all enemies are defeated
        if not enemies:
            level += 1
            enemies = create_enemies(level)

        # Draw player and score
        player.draw()
        score_text = pygame.font.Font(None, 36).render(f'Score: {player.score}', True, WHITE)
        level_text = pygame.font.Font(None, 36).render(f'Level: {level}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

