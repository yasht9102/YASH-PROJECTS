import pygame, sys

pygame.init()
WIDTH, HEIGHT = 800, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hardcore Mario Clone")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36, bold=True)

# Colors
DARK = (15, 15, 35)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)

player = pygame.Rect(50, 400, 40, 50)
vel_y = 0
gravity = 0.6
on_ground = False
score = 0
lives = 3
level = 1

def create_level(level_num):
    platforms = [pygame.Rect(0, 430, 800, 50)]
    enemies = [pygame.Rect(600, 400, 40, 50), pygame.Rect(200, 400, 40, 50)]
    coins = [pygame.Rect(100 + i*120, 380 - (i % 3)*50, 15, 15) for i in range(5 + level_num)]

    for i in range(level_num + 2):
        platforms.append(pygame.Rect(150 + i*100, 380 - i*30, 100, 15))

    return {
        "platforms": platforms,
        "coins": coins,
        "enemies": enemies,
        "enemy_dirs": [-1, 1]
    }

def draw(level_data):
    win.fill(DARK)
    for plat in level_data["platforms"]:
        pygame.draw.rect(win, GREEN, plat)
    for coin in level_data["coins"]:
        pygame.draw.rect(win, YELLOW, coin)
    for enemy in level_data["enemies"]:
        pygame.draw.rect(win, BLUE, enemy)
    pygame.draw.rect(win, RED, player)
    win.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    win.blit(font.render(f"Lives: {lives}", True, WHITE), (10, 40))
    win.blit(font.render(f"Level: {level}", True, WHITE), (10, 70))
    pygame.display.update()

def game_over():
    win.fill(DARK)
    msg = font.render("💀 GAME OVER 💀 Press R to Restart or ESC to Quit", True, RED)
    win.blit(msg, (150, HEIGHT // 2))
    pygame.display.update()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def level_complete():
    win.fill(DARK)
    msg = font.render("✅ LEVEL COMPLETE! Press SPACE to continue.", True, GREEN)
    win.blit(msg, (180, HEIGHT // 2))
    pygame.display.update()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                return

def you_win():
    win.fill(DARK)
    msg1 = big_font.render("🎉 YOU BEAT ALL 5 LEVELS! 🎉", True, YELLOW)
    msg2 = font.render("You're a true platforming champion!", True, WHITE)
    msg3 = font.render("Enemies, gravity, coins — you conquered it all.", True, WHITE)
    msg4 = font.render("Thank you for playing!", True, WHITE)
    win.blit(msg1, (100, HEIGHT // 2 - 50))
    win.blit(msg2, (200, HEIGHT // 2))
    win.blit(msg3, (140, HEIGHT // 2 + 30))
    win.blit(msg4, (270, HEIGHT // 2 + 60))
    pygame.display.update()
    pygame.time.wait(6000)
    pygame.quit()
    sys.exit()

# Main Game Loop
running = True
while running:
    player.x, player.y = 50, 400
    vel_y = 0
    current = create_level(level)

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.x -= 5
        if keys[pygame.K_RIGHT]: player.x += 5
        if keys[pygame.K_SPACE] and on_ground:
            vel_y = -12
            on_ground = False

        vel_y += gravity
        player.y += vel_y

        on_ground = False
        for plat in current["platforms"]:
            if player.colliderect(plat) and vel_y > 0:
                player.bottom = plat.top
                vel_y = 0
                on_ground = True

        for coin in current["coins"][:]:
            if player.colliderect(coin):
                current["coins"].remove(coin)
                score += 1

        for i, enemy in enumerate(current["enemies"]):
            enemy.x += current["enemy_dirs"][i] * 2
            if enemy.left < 0 or enemy.right > WIDTH:
                current["enemy_dirs"][i] *= -1

        for enemy in current["enemies"]:
            if player.colliderect(enemy):
                lives -= 1
                if lives <= 0:
                    if game_over():
                        level = 1
                        score = 0
                        lives = 3
                        break
                player.x, player.y = 50, 400
                vel_y = 0

        if not current["coins"]:
            if level < 5:
                level += 1
                level_complete()
                break
            else:
                you_win()

        draw(current)
