from typing import NamedTuple

import pygame

screen_height = 600
screen_width = 600
gravity = 9.8
framerate = 5000

# Player
acceleration = 0.1 / framerate
max_speed = 5000 / framerate

move_keys = pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN

# Frictions
class FrictionType(NamedTuple):
    static: float
    kinetic: float
    
class friction:
    ice = FrictionType(0.059, 0.0046)
