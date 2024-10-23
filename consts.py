from typing import NamedTuple

screen_height = 600
screen_width = 600
gravity = 9.8
framerate = 5000

# Player
acceleration = 0.1 / framerate
max_speed = 5000 / framerate

# Frictions
class FrictionType(NamedTuple):
    static: float
    kinetic: float
    
class friction:
    ice = FrictionType(0.0059, 0.0046)
