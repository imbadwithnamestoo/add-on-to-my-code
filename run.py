import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Bricks Challenge v1.1")

clock = pygame.time.Clock()

player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height
player_speed = 5

brick_width = 50
brick_height = 50
bricks = []

shield_width = 50
shield_height = 50
shield_duration = 5000
shield_active = False
shield_timer = 0

score_font = pygame.font.Font(None, 36)
score = 0

game_over = False

timer = pygame.time.get_ticks()

shield_image = pygame.Surface((shield_width, shield_height))
shield_image.fill(BLUE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        current_time = pygame.time.get_ticks()
        if shield_active and current_time - shield_timer >= shield_duration:
            shield_active = False

        for brick in bricks.copy():
            brick[1] += 3
            if brick[1] > SCREEN_HEIGHT:
                bricks.remove(brick)

            if (
                brick[1] + brick_height > player_y
                and brick[1] < player_y + player_height
                and brick[0] + brick_width > player_x
                and brick[0] < player_x + player_width
            ):
                if brick in bricks:
                    if brick[0] + brick_width <= SCREEN_WIDTH:
                        bricks.remove(brick)
                        if not shield_active:
                            game_over = True
                    else:
                        if not shield_active:
                            shield_active = True
                            shield_timer = current_time
                        bricks.remove(brick)

        if random.randint(0, 100) < 3:
            if random.randint(0, 1) == 0:
                bricks.append([random.randint(0, SCREEN_WIDTH - brick_width), 0])
            else:
                bricks.append([random.randint(0, SCREEN_WIDTH - shield_width), 0])

        current_time = pygame.time.get_ticks()
        if current_time - timer >= 1000:
            score += 1
            timer = current_time

        screen.fill(WHITE)

        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        for brick in bricks:
            if brick[0] + brick_width <= SCREEN_WIDTH:
                pygame.draw.rect(screen, RED, (brick[0], brick[1], brick_width, brick_height))
            else:
                screen.blit(shield_image, (brick[0], brick[1]))

        score_text = score_font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (10, 10))

        if shield_active:
            shield_text = score_font.render("Shield Active", True, BLUE)
            screen.blit(shield_text, (SCREEN_WIDTH // 2 - shield_text.get_width() // 2, 10))
    else:
        game_over_text = score_font.render("Game Over", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
