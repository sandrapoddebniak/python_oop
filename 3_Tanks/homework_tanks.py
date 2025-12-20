import pygame
import random
import os

# ================== KONFIGURACJA ==================
WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kosmiczne Czołgi – Gra Zaliczeniowa")
clock = pygame.time.Clock()

# ================== CZCIONKI ==================
font_score = pygame.font.SysFont("Arial", 26, bold=True)
font_big = pygame.font.SysFont("Arial", 48, bold=True)

# ================== TŁO ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR,"background.jpg.jpg")

try:
    bg_img = pygame.image.load(image_path).convert()
    BACKGROUND = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    print(f"Sukces! Wczytano tło z: {image_path}")
except:
    print("Nie mogę wczytać pliku background.jpg, używam ciemnego tła")
    BACKGROUND = pygame.Surface((WIDTH, HEIGHT))
    BACKGROUND.fill((10, 10, 30))


# ================== KLASA CZĄSTEK (Ogień) ==================
class Particle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(2, 5)
        self.lifetime = random.randint(15, 25)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, surf):
        if self.lifetime > 0:
            size = max(self.lifetime // 5, 1)
            pygame.draw.circle(surf, (255, 165, 0), (int(self.x), int(self.y)), size)

# ================== STANY GRY ==================
MENU = 0
PLAYING = 1
GAME_OVER = 2
state = MENU

# ================== FUNKCJE ==================
def draw_text(text, font, color, x, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def reset_game():
    return {
        "player": pygame.Rect(WIDTH//2 - 15, HEIGHT - 60, 30, 30),
        "bullets": [],
        "enemies": [],
        "score": 0,
        "health": 5,
        "spawn_timer": 0,
        "particles": [],
    }

game = reset_game()

# ================== PĘTLA GŁÓWNA ==================
running = True
while running:
    clock.tick(FPS)
    screen.blit(BACKGROUND, (0,0))  # tło na samym początku

    # ---------- ZDARZENIA ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if state in (MENU, GAME_OVER) and event.key == pygame.K_SPACE:
                game = reset_game()
                state = PLAYING

            if state == PLAYING and event.key == pygame.K_SPACE:
                bullet = pygame.Rect(
                    game["player"].centerx - 2,
                    game["player"].top,
                    4, 10
                )
                game["bullets"].append(bullet)

    # ---------- LOGIKA ----------
    if state == PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and game["player"].left > 0:
            game["player"].x -= 5
        if keys[pygame.K_d] and game["player"].right < WIDTH:
            game["player"].x += 5
        if keys[pygame.K_w] and game["player"].top > 0:
            game["player"].y -= 5
        if keys[pygame.K_s] and game["player"].bottom < HEIGHT:
            game["player"].y += 5

        # Dodawanie przeciwników
        game["spawn_timer"] += 1
        if game["spawn_timer"] > 45:
            enemy = pygame.Rect(random.randint(0, WIDTH-40), -40, 40, 40)
            game["enemies"].append(enemy)
            game["spawn_timer"] = 0

        # Ruch przeciwników
        for e in game["enemies"][:]:
            e.y += 3 + game["score"] // 1000
            if e.colliderect(game["player"]):
                game["health"] -= 1
                game["enemies"].remove(e)
                if game["health"] <= 0:
                    state = GAME_OVER
            elif e.top > HEIGHT:
                game["enemies"].remove(e)

        # Pociski
        for b in game["bullets"][:]:
            b.y -= 8
            if b.bottom < 0:
                game["bullets"].remove(b)
            for e in game["enemies"][:]:
                if b.colliderect(e):
                    if b in game["bullets"]:
                        game["bullets"].remove(b)
                    if e in game["enemies"]:
                        game["enemies"].remove(e)
                    game["score"] += 100
                    break

        # Dodawanie cząstek ognia pod graczem
        game["particles"].append(Particle(game["player"].centerx, game["player"].bottom))

        # Aktualizacja cząstek
        for p in game["particles"][:]:
            p.update()
            if p.lifetime <= 0:
                game["particles"].remove(p)

    # ---------- RYSOWANIE ----------
    if state == MENU:
        draw_text("KOSMICZNE CZOŁGI", font_big, (255,255,255), WIDTH//2, HEIGHT//2 - 40)
        draw_text("SPACJA – START", font_score, (0,255,200), WIDTH//2, HEIGHT//2 + 30)

    elif state == PLAYING:
        # Cząstki ognia
        for p in game["particles"]:
            p.draw(screen)

        # Gracz – trójkąt
        pygame.draw.polygon(screen, (0,150,255), [
            (game["player"].centerx, game["player"].top),
            (game["player"].left, game["player"].bottom),
            (game["player"].right, game["player"].bottom)
        ])

        # Pociski
        for b in game["bullets"]:
            pygame.draw.rect(screen, (255,255,0), b)

        # Przeciwnicy
        for e in game["enemies"]:
            pygame.draw.ellipse(screen, (200,100,255), e)
            # oczy przeciwnika
            pygame.draw.circle(screen, (255,255,255), (e.x+10, e.y+15), 4)
            pygame.draw.circle(screen, (255,255,255), (e.x+30, e.y+15), 4)

        # UI – punkty i pasek zdrowia
        draw_text(f"PUNKTY: {game['score']}", font_score, (255,255,255), 90, 30)
        pygame.draw.rect(screen, (100,0,0), (WIDTH-140, 20, 100, 15))
        pygame.draw.rect(screen, (0,255,0), (WIDTH-140, 20, game["health"]*20, 15))

    elif state == GAME_OVER:
        draw_text("KONIEC GRY", font_big, (255,60,60), WIDTH//2, HEIGHT//2 - 40)
        draw_text(f"WYNIK: {game['score']}", font_score, (255,255,255), WIDTH//2, HEIGHT//2 + 10)
        draw_text("SPACJA – ZAGRAJ PONOWNIE", font_score, (0,255,150), WIDTH//2, HEIGHT//2 + 50)

    pygame.display.flip()

pygame.quit()
