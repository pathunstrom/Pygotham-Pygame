import pygame.sprite as sprite
import pygame.image as image
import pygame.mouse as mouse
import pygame.key as keyboard
import pygame.transform
from pygame import K_w
from pygame import Surface
import math

player_image = image.load("images/player_ship.png")
enemy_image = image.load("images/enemy_ship.png")


def init(display):
    player_image.convert(display)
    enemy_image.convert(display)


class Player(sprite.Sprite):

    def __init__(self, screen, thruster = None, *groups):
        super(Player, self).__init__(*groups)
        self.image = player_image.copy()
        self.image.set_colorkey((255, 174, 201))
        self.rect = self.image.get_rect()
        self.x = screen.centerx
        self.y = screen.centery
        self.facing = 0, -1
        self.velocity = 0, 0
        self.thruster = thruster if thruster is not None else K_w
        self.acceleration = 160
        self.screen = screen

    def update(self, time):
        # Move position
        self.x, self.y = self.x + (self.velocity[0] * time), self.y + (self.velocity[1] * time)

        # Check new rotation
        mouse_pos = mouse.get_pos()
        facing = mouse_pos[0] - self.x, mouse_pos[1] - self.y
        length = math.hypot(*facing)
        self.facing = facing[0] / length, facing[1] / length

        # Rotate Image
        self.image = pygame.transform.rotate(player_image, math.degrees(math.atan2(*self.facing)))
        self.rect = self.image.get_rect()
        self.rect.center = int(self.x), int(self.y)

        # If off screen, move to other side
        if self.rect.bottom < self.screen.top:
            self.rect.top = self.screen.bottom
        elif self.rect.top > self.screen.bottom:
            self.rect.bottom = self.screen.top

        if self.rect.right < self.screen.left:
            self.rect.left = self.screen.right
        elif self.rect.left > self.screen.right:
            self.rect.right = self.screen.left

        self.x, self.y = self.rect.center

        # Accelerate
        key = keyboard.get_pressed()
        if key[self.thruster]:
            x = self.velocity[0] + (self.facing[0] * self.acceleration * time)
            y = self.velocity[1] + (self.facing[1] * self.acceleration * time)
            self.velocity = x, y

    def fire(self, player_shots, baddies):
        x = self.x + (self.facing[0] * 25)
        y = self.y + (self.facing[1] * 25)
        start_point = x, y

        direction = self.facing[0] * 200, self.facing[1] * 200
        Bullet(start_point,
               direction,
               (255, 255, 255),
               baddies,
               player_shots)





class Enemy(sprite.Sprite):

    def __init__(self, spawnpoint, player, *groups):
        super(Enemy, self).__init__(*groups)
        self.image = enemy_image.copy()
        self.rect = self.image.get_rect()
        self.player = player
        self.x, self.y = spawnpoint
        self.facing = 0, 1
        self.velocity = 0, 0

    def update(self, time):
        pass


class Bullet(sprite.Sprite):

    def __init__(self, point, direction, color, targets, *groups):
        super(Bullet, self).__init__(*groups)
        self.image = Surface((2, 2))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = point[0]
        self.y = point[1]
        self.rect.center = int(self.x), int(self.y)
        self.velocity = direction
        self.targets = targets

    def update(self, time):
        self.x = self.x + (self.velocity[0] * time)
        self.y = self.y + (self.velocity[1] * time)
        self.rect.center = int(self.x), int(self.y)
        sprite.spritecollide(self, self.targets, True)