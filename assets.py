import pygame
import math

def make_sword_image(x, y):
    # define a surface (RECTANGLE)
    image_orig = pygame.Surface((100 , 100))
    # for making transparent background while rotating an image
    image_orig.set_colorkey((0, 0, 0))
    # fill the rectangle / surface with green color
    image_orig.fill((0, 255, 0))
    # creating a copy of orignal image for smooth rotation
    image = image_orig.copy()
    image.set_colorkey((0, 0, 0))
    # define rect for placing the rectangle at the desired position
    return image.get_rect(), image


def draw_rectangle(screen, x, y, width, height, color, rotation=0):
    points = []
    # x -= width / 2
    # y -= height / 2
    
    # The distance from the center of the rectangle to
    # one of the corners is the same for each corner.
    radius = math.sqrt((height / 2)**2 + (width / 2)**2)

    # Get the angle to one of the corners with respect
    # to the x-axis.
    angle = math.atan2(height / 2, width / 2)

    # Transform that angle to reach each corner of the rectangle.
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]

    # Convert rotation from degrees to radians.
    rot_radians = (math.pi / 180) * rotation

    # Calculate the coordinates of each point.
    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rot_radians)
        x_offset = radius * math.cos(angle + rot_radians)
        points.append((x + x_offset, y + y_offset))

    pygame.draw.polygon(screen, color, points)