import pygame
import random
import os

# Constants
FPS = 60
COLORKEY = (255, 174, 201)
SPAWNRATE = 1500
path = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(path, "images")

# Events
PLAYERSHOT = 25
GAMEOVER = 26
ENEMYSHOT = 27


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        image_path = os.path.join(image_dir, "player_ship.png")
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey(COLORKEY)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = 150, 600
        self.x = self.rect.centerx * 1000
        self.speed = 100

        self.move_right = False
        self.move_left = False
        self.shooting = False
        self.cooling = 0

    def update(self, time):
        if self.move_right:
            self.x += self.speed * time
            self.rect.centerx = self.x / 1000
        if self.move_left:
            self.x += -1 * self.speed * time
            self.rect.centerx = self.x / 1000

        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.centerx * 1000
        elif self.rect.right > 300:
            self.rect.right = 300
            self.x = self.rect.centerx * 1000

        if self.shooting and not self.cooling:
            shot = pygame.event.Event(PLAYERSHOT, {"pos": self.rect.midtop})
            pygame.event.post(shot)
            self.cooling = 200
        if self.cooling:
            self.cooling += -1 * time
            self.cooling = 0 if self.cooling < 0 else self.cooling


class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, turn, player):
        pygame.sprite.Sprite.__init__(self)
        image_path = os.path.join(image_dir, "enemy_ship.png")
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey(COLORKEY)
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.centerx = pos
        self.forward = 1
        self.lateral = turn
        self.x = self.rect.centerx * 1000
        self.y = self.rect.centery * 1000
        self.speed = 75
        self.lat_speed = 0
        self.acceleration = 10
        self.accelerating = True
        self.cooldown = 0
        self.player = player

    def update(self, time):
        self.y += self.speed * time * self.forward
        self.rect.centery = self.y / 1000
        self.x += self.lat_speed * time * self.lateral
        self.rect.centerx = self.x / 1000
        if self.accelerating:
            self.lat_speed += self.acceleration
            if self.lat_speed > 150:
                self.accelerating = not self.accelerating
        else:
            self.lat_speed += self.acceleration * -1
            if self.lat_speed < 10:
                self.accelerating = not self.accelerating
                self.lateral *= -1

        if not self.cooldown:
            shot = pygame.event.Event(ENEMYSHOT, {"pos": self.rect.midbottom})
            pygame.event.post(shot)
            self.cooldown = 1593
        self.cooldown = 0 if self.cooldown < 0 else self.cooldown - time

        if pygame.sprite.spritecollide(self, self.player, True):
            pygame.event.post(pygame.event.Event(GAMEOVER))



class Bullet (pygame.sprite.Sprite):
    def __init__(self, origin, vector, friendly, enemies, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 2))
        self.rect = pygame.Rect(0, 0, 2, 2)
        self.image.fill((255, 255, 255))
        self.rect.center = origin
        self.vector = vector
        self.speed = 300
        self.y = self.rect.centery * 1000
        self.friendly = friendly
        self.player = player
        self.enemies = enemies

    def update(self, time):
        self.y += time * self.speed * self.vector[1]
        self.rect.centery = self.y / 1000
        if self.friendly:
            if pygame.sprite.spritecollide(self, self.enemies, True):
                self.kill()
        else:
            if pygame.sprite.spritecollide(self, self.player, True):
                pygame.event.post(pygame.event.Event(GAMEOVER ))


class Spawner(object):

    def __init__(self, enemies, player):
        self.timer = 0
        self.enemies = enemies
        self.player = player

    def update(self, time):
        self.timer += time
        if self.timer > SPAWNRATE:
            self.timer += -1 * SPAWNRATE
            pos = random.randint(45, 255)
            turn = random.choice([-1, 1])
            self.enemies.add(Enemy(pos, turn, self.player))


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
    newline = title.render("Sprites", True, (255, 255, 255))
    left = (screen_width - newline.get_width()) / 2
    screen.blit(newline, (left, top))

    top += newline.get_height() + spacing
    newline = instruction.render("Press Enter to Begin", True, (255, 255, 255))
    left = (screen_width - newline.get_width()) / 2
    screen.blit(newline, (left, top))
    pygame.display.flip()


def game_loop(screen, clock):
    player = pygame.sprite.GroupSingle(Player())
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    spawner = Spawner(enemies, player)
    screen.fill((0, 0, 0))
    pygame.display.flip()
    running = True

    while running:
        running = handle_game_events(player, bullets, enemies)
        time = clock.tick(FPS)
        player.update(time)
        enemies.update(time)
        bullets.update(time)
        spawner.update(time)
        screen.fill((0, 0, 0))
        player.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)
        pygame.display.flip()


def handle_game_events(p, b, e):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                p.sprite.move_left = True
            elif event.key == pygame.K_RIGHT:
                p.sprite.move_right = True
            elif event.key == pygame.K_SPACE:
                p.sprite.shooting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                p.sprite.move_left = False
            elif event.key == pygame.K_RIGHT:
                p.sprite.move_right = False
            elif event.key == pygame.K_SPACE:
                p.sprite.shooting = False
            elif event.key == pygame.K_ESCAPE:
                return False
        elif event.type == PLAYERSHOT:
            b.add(Bullet(event.dict["pos"], (0, -1), True, e, p))
        elif event.type == ENEMYSHOT:
            b.add(Bullet(event.dict["pos"], (0, 1), False, e, p))
        elif event.type == GAMEOVER:
            return False
    return True


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    game_screen = pygame.display.set_mode((300, 600))
    pygame.display.set_caption("Sprites")
    game_clock = pygame.time.Clock()

    main_loop(game_screen, game_clock)
    pygame.quit()
