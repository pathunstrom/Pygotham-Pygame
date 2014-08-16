import pygame


def main_loop():
    pygame.init()
    display = pygame.display.set_mode((300, 300), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display.fill((0, 0, 0))
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    main_loop()