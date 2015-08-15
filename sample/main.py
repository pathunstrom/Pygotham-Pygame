import pygame
import sprite

running = True
FIRE = pygame.USEREVENT + 1

def main_loop():
    pygame.init()
    display = pygame.display.set_mode((600, 600))
    sprite.init(display)
    display_area = display.get_rect()
    clock = pygame.time.Clock()
    player = pygame.sprite.GroupSingle()
    player_shots = pygame.sprite.Group()
    baddies = pygame.sprite.Group()

    sprite.Player(display_area, pygame.K_w, player)
    sprite.Enemy((20, 20), player.sprite, display_area, baddies)
    display.blit(sprite.player_image, (0, 0))

    def stop():
        global running
        running = False

    while running:
        time = clock.tick() / 1000.0

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.sprite.fire(player_shots, baddies)
        player.update(time)
        player_shots.update(time)
        baddies.update(time)

        # Draw
        display.fill((0, 0, 0))
        player.draw(display)
        player_shots.draw(display)
        baddies.draw(display)

        pygame.display.update()


if __name__ == "__main__":
    main_loop()