# this file contains all the sprite(characters) for the game
import pygame
from settings import *
import os
import random

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        # reference for a game, going to use this to find platforms
        self.game = game
        self.walking = False
        self.jumping = False
        self.can_collide = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frame
        # clearing background color of the sprite
        self.rect = self.image.get_rect()
        # moving sprite into the center of the image
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        # vector for velocity
        self.vel = vec(0, 0)
        # vector for acceleration
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frame = self.game.player_spritesheet.get_image(0, 196, 66, 92)
        self.standing_frame.set_colorkey(BLACK)
        self.jump_frame_r = self.game.player_spritesheet.get_image(438, 93, 67, 94)
        self.jump_frame_r.set_colorkey(BLACK)
        self.jump_frame_l = pygame.transform.flip(self.jump_frame_r, True, False)
        self.jump_frame_l.set_colorkey(BLACK)
        self.walk_frame_r = [self.game.player_spritesheet.get_image(0, 0, 72, 97),
                             self.game.player_spritesheet.get_image(146, 0, 72, 97),
                             self.game.player_spritesheet.get_image(73, 98, 72, 97),
                             self.game.player_spritesheet.get_image(219, 0, 72, 97),
                             self.game.player_spritesheet.get_image(219, 98, 72, 97),
                             self.game.player_spritesheet.get_image(292, 98, 72, 97)]
        self.walk_frame_l = []
        for frame in self.walk_frame_r:
            frame.set_colorkey(BLACK)
            self.walk_frame_l.append(pygame.transform.flip(frame, True, False))

    def jump(self):
        # we are going to jump only when we stand on a platform
        # move down the sprite temporarily 1 pixel to check if there is any platform
        self.jumping = True
        self.can_collide = True
        self.rect.x += 1
        # check if sprite collides
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        # move sprite back to its original position
        self.rect.x -= 1
        if hits and self.jumping:
            self.vel.y = -20
            self.can_collide = False

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pygame.K_DOWN]:
            self.acc.y = PLAYER_GRAV + 1.2

        # apply friction to the x direction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # motion equations
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        # update the position of the sprite
        self.rect.midbottom = self.pos

    def animate(self):
        current_time = pygame.time.get_ticks()
        if not self.jumping and not self.walking:
            bottom = self.rect.bottom
            self.image = self.standing_frame
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        # check if we are moving
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # walking animation
        if self.walking:
            if current_time - self.last_update > 200:
                self.last_update = current_time
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frame_r[self.current_frame]
                else:
                    self.image = self.walk_frame_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # jumping animation
        if self.jumping:
            bottom = self.rect.bottom
            if self.vel.x < 0:
                self.image = self.jump_frame_l
            else:
                self.image = self.jump_frame_r
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        images = [self.game.spritesheet.get_image(382, 408, 200, 100),
                  self.game.spritesheet.get_image(0, 96, 380, 94)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # variable to move platforms down
        self.pos = vec(x, y)
        self.vel = vec(0, 0)


class Projectile(pygame.sprite.Sprite):
    # projectiles will always come from the top
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("img", "projectile1.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 5 - PROJECTILE_HEIGHT
        self.pos = vec(self.rect.x, self.rect.y)
        self.vel = vec(0, 0)

    def update(self):
        self.vel = vec(0, PROJECTILE_SPEED)
        self.pos.y += self.vel.y

        self.rect.midtop = self.pos


class Spritesheet:
    # class for loading and parsing sprite sheets
    def __init__(self, filename):
        filename = os.path.join("img", filename)
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image
