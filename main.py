import math
from typing import NamedTuple
import assets
import consts
from math import sin, cos, tan, asin, acos, atan, sqrt

import pygame

class GameNoun:
    def __init__(self, x, y, w, h, vx=0, vy=0, ax=0, ay=0, base_mass=0, armor_mass=0, kinetic_friction=0.0, static_friction=0.0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.base_mass = base_mass
        self.armor_mass = armor_mass
        self.kinetic_friction = kinetic_friction
        self.static_friction = static_friction
    
    def get_mass(self):
        return self.base_mass + self.armor_mass
    
    def get_velocity_magnitude(self):
        return sqrt(self.vx ** 2 + self.vy ** 2)
    
    def get_static_friction_max_speed(self):
        return (self.static_friction * consts.gravity) / consts.framerate
    
    def get_kinetic_friction_slowdown(self):
        # mu_k * n = mu_k * mg
        return (self.get_velocity_magnitude() * (self.kinetic_friction * consts.gravity)) / consts.framerate
        
    def direction_of_velocity(self):
        if not (self.vx):
            return 0
        return atan(self.vy / self.vx)
    
    def handle_friction(self):
        return
        velocity_mag = self.get_velocity_magnitude()
        highest_velocity_before_static_friction = self.get_static_friction_max_speed()
        friction_slowdown = self.get_kinetic_friction_slowdown()
        theta = self.direction_of_velocity()
        
        
        if highest_velocity_before_static_friction > velocity_mag:
            self.vx = 0
            self.vy = 0
        
        
        
        print(self.vx, self.vy, theta, highest_velocity_before_static_friction)
        
        if self.vx > 0:
            self.vx -= friction_slowdown * cos(theta)
            self.vx = max(0, self.vx)
        elif self.vx < 0:
            self.vx += friction_slowdown * cos(theta)
            self.vx = min(0, self.vx)
        if self.vy > 0:
            self.vy -= friction_slowdown * sin(theta)
            self.vy = max(0, self.vy)
        elif self.vy < 0:
            self.vy += friction_slowdown * sin(theta)
            self.vy = min(0, self.vy)
    
    def update(self):
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy
        
        self.handle_friction()
        
        if abs(self.vx) > consts.max_speed:
            self.vx = (abs(self.vx)//self.vx) * (consts.max_speed)
        if abs(self.vy) > consts.max_speed:
            self.vy = (abs(self.vy)//self.vy) * (consts.max_speed)
        
        
        if (self.y < 0 and self.vy < 0) or (self.y > consts.screen_height and self.vy > 0):
            self.vy = -self.vy
        
        if (self.x < 0 and self.vx < 0) or (self.x > consts.screen_width and self.vx > 0):
            self.vx = -self.vx
    
    def reset(self):
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0


class Player(GameNoun):
    resets = 2
    attack_frames = 0
    sword_angle = 0
    
    def attacking(self):
        return (self.sword_angle > 0)
    
    def attack(self):
        self.sword_angle = 360.0
    
    def update(self):
        super().update()
        if self.attacking():
            self.sword_angle -= 0.2
    
    def render(self, screen):
        pygame.draw.ellipse(screen, (0, 255, 0), (player.x, player.y, player.w, player.h))
        
        # old_sword_image, old_sword_screen = assets.make_sword_image(player.x, player.y)
        # new_sword_image = pygame.transform.rotate(old_sword_screen, self.sword_angle)
        # screen.blit(new_sword_image, old_sword_image)
        if self.attacking():
            assets.draw_rectangle(screen, player.x, player.y, 30, 5, (128, 128, 128), self.sword_angle)
    
    def stop(self):
        # if self.resets > 0:
        if 1:
            self.resets -= 1
            self.reset()
        
        
width, height = 600, 600

engine = pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

game_going = True
player = Player(
    100.0,
    100.0,
    10.0,
    10.0,
    base_mass=100,
    static_friction=consts.friction.ice.static,
    kinetic_friction=consts.friction.ice.kinetic,
)
nouns = [player]

while game_going:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.attack()
            if event.key == pygame.K_LSHIFT:
                player.stop()
        if event.type == pygame.QUIT:
            game_going = False
        
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.ay = -consts.acceleration
    elif keys[pygame.K_DOWN]:
        player.ay = consts.acceleration
    else:
        player.ay = 0
    
    if keys[pygame.K_LEFT]:
        player.ax = -consts.acceleration
    elif keys[pygame.K_RIGHT]:
        player.ax = consts.acceleration
    else:
        player.ax = 0
    
    
    
    player.update()
    
    player.render(screen)
    
    pygame.display.flip()
    clock.tick(consts.framerate)


pygame.quit()