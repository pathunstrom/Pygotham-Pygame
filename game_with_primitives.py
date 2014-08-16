import pygame
import os
import random


PLAYERIMPACT = 25


def main_loop(screen, clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    game_loop(screen, clock)
                elif event.key == pygame.K_ESCAPE:
                    running = False
        draw_title(screen)
        clock.tick(60)


def draw_title(screen):
    screen.fill((0, 0, 0))
    spacing = 10
    screen_width = screen.get_width()

    title = pygame.font.Font(None, 40)
    instruction = pygame.font.Font(None, 16)
    combined_height = title.get_height() + instruction.get_height() + spacing

    top = (screen.get_height() - combined_height) / 2
    newline = title.render("Primitives", True, (255, 255, 255))
    left = (screen_width - newline.get_width()) / 2
    screen.blit(newline, (left, top))

    top += newline.get_height() + spacing
    newline = instruction.render("Press Enter to Begin", True, (255, 255, 255))
    left = (screen_width - newline.get_width()) / 2
    screen.blit(newline, (left, top))
    pygame.display.flip()


def game_loop(screen, clock):
    player = {"rect": pygame.Rect(0, 540, 30, 50), "vector": [0, 0]}
    enemies = []
    bullets = []
    game_time = 0
    model = {"p": player, "e": enemies, "b": bullets,
             "t": {"game": game_time, "spawn": game_time}}
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player["vector"][0] += 3
                elif event.key == pygame.K_LEFT:
                    player["vector"][0] += -3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player["vector"][0] += -3
                elif event.key == pygame.K_LEFT:
                    player["vector"][0] += 3
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == PLAYERIMPACT:
                running = False
                game_over_loop(screen, clock)
        simulate(model)
        draw_game(screen, model)
        tick = clock.tick(60)
        model["t"]["game"] += tick
        model["t"]["spawn"] += tick


def draw_game(screen, model):
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), model["p"]["rect"], 2)
    for e in model["e"]:
        pygame.draw.rect(screen, (255, 0, 0), e["rect"], 1)
    pygame.display.flip()


def simulate(model):
    player = model["p"]
    player["rect"].centerx += player["vector"][0]
    if player["rect"].left < 0:
        player["rect"].left = 0
    elif player["rect"].right > 300:
        player["rect"].right = 300

    enemies = model["e"]
    for enemy in enemies:
        enemy["rect"].centerx += enemy["vector"][0]
        enemy["rect"].centery += enemy["vector"][1]
        if enemy["vector"][0] >= 10:
            enemy["change"] = -1
        elif enemy["vector"][0] <= -10:
            enemy["change"] = 1
        enemy["vector"][0] += enemy["change"]
        if enemy["rect"].top > 600:
            enemies.remove(enemy)
        if enemy["rect"].colliderect(player["rect"]):
            pygame.event.post(pygame.event.Event(25))
    if model["t"]["spawn"] > 500:
        enemies.append(spawn_enemy())
        model["t"]["spawn"] += -500


def spawn_enemy():
    direction = random.choice((-1, 1))
    return {"rect": pygame.Rect(random.randint(0, 380), -30, 20, 30),
            "vector": [direction, 3],
            "change": direction}


def game_over_loop(screen, clock):
    pass


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    game_screen = pygame.display.set_mode((300, 600))
    pygame.display.set_caption("Pacifist")
    game_clock = pygame.time.Clock()

    main_loop(game_screen, game_clock)
    pygame.quit()