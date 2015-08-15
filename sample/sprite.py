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

ENEMY_FOCUS = .25

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

    def __init__(self, spawnpoint, player, area, *groups):
        super(Enemy, self).__init__(*groups)
        self.image = enemy_image.copy()
        self.rect = self.image.get_rect()
        self.player = player
        self.area = area
        self.x, self.y = spawnpoint
        self.target = area.center
        self.rect.center = int(self.x), int(self.y)
        target = self.target[0] - self.x, self.target[1] - self.y
        length = math.hypot(*target)
        self.velocity = target[0] / length * 10.0, target[1] / length * 10.0
        self.focus = ENEMY_FOCUS
        self.accel = 100

    def update(self, time):
        # Move
        old_position = self.x, self.y
        self.x += self.velocity[0] * time
        self.y += self.velocity[1] * time
        facing = self.x - old_position[0], self.y - old_position[1]
        self.image = pygame.transform.rotate(enemy_image, math.degrees(math.atan2(*facing)))
        self.rect = self.image.get_rect()
        self.rect.center = int(self.x), int(self.y)
        # If off screen, move to other side
        if self.rect.bottom < self.area.top:
            self.rect.top = self.area.bottom
        elif self.rect.top > self.area.bottom:
            self.rect.bottom = self.area.top

        if self.rect.right < self.area.left:
            self.rect.left = self.area.right
        elif self.rect.left > self.area.right:
            self.rect.right = self.area.left

        self.x, self.y = self.rect.center


        # Decrement focus

        self.focus += -time
        print self.focus

        # Choose new Target
        if self.focus <= 0:
            self.target = self.player.rect.center
            self.focus = ENEMY_FOCUS

        new_x = self.target[0] - self.x
        new_y = self.target[1] - self.y
        length = math.hypot(new_x, new_y)
        acceleration = new_x / length * self.accel * time, new_y / length * self.accel * time
        self.velocity = self.velocity[0] + acceleration[0], self.velocity[1] + acceleration[1]

        speed = math.hypot(*self.velocity)
        if speed > 300:
            self.velocity = self.velocity[0] / speed * 300.0, self.velocity[1] / speed * 300.0


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