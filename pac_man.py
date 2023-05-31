import random

import pygame
from pygame.sprite import Group, spritecollide

from game_object import GameObject
from text import Text

width = 640
height = 480

purple = (128, 0, 128)


class Player(GameObject):
    sprite_filename = "player"
    width = 30
    height = 30


class Wall(GameObject):
    sprite_filename = "wall"
    width = 40
    height = 40


class Chest(GameObject):
    sprite_filename = "chest"
    width = 30
    height = 30

def calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height - 2

    walls_coordinates = []
    for block_num in range(horizontal_wall_blocks_amount):
        walls_coordinates.extend([
            (block_num * wall_block_width, 0),
            (block_num * wall_block_width, screen_height - wall_block_height),
        ])
    for block_num in range(1, vertical_wall_blocks_amount + 1):
        walls_coordinates.extend([
            (0, block_num * wall_block_height),
            (screen_width - wall_block_width, block_num * wall_block_height),
        ])

    return walls_coordinates

def generate_random_maze():
    wall_coordinates = []
    for x in range(Wall.width, width - Wall.width, Wall.width):
        for y in range(Wall.height, height - Wall.height, Wall.height):
            if random.random() < 0.3:
                wall_coordinates.append((x, y))
    return wall_coordinates

def compose_context(screen, wall_coordinates):
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    return {
        "player": Player(screen.get_width() // 2, screen.get_height() // 2),
        "walls": Group(*[Wall(x, y) for (x, y) in walls_coordinates]),
        "chests": Group(),
        "changing_walls": Group(*[Wall(x, y) for (x, y) in wall_coordinates]),
        "score": 0,
    }

def draw_whole_screen(screen, context):
    screen.fill(purple)
    context["player"].draw(screen)
    context["walls"].draw(screen)
    context["changing_walls"].draw(screen)
    context["chests"].draw(screen)
    Text(f"Score: {context['score']}", (10, 10)).draw(screen)

    for chest in context["chests"]:
        chest.draw(screen)

def generate_random_chest_position():
    x = random.randint(Chest.width, width - Chest.width)
    y = random.randint(Chest.height, height - Chest.height)
    return x, y

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    player_speed = 5

    wall_coordinates = generate_random_maze()
    context = compose_context(screen, wall_coordinates)

    for _ in range(5):
        chest = Chest(*generate_random_chest_position())
        context["chests"].add(chest)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        old_player_topleft = context["player"].rect.topleft
        if keys[pygame.K_w]:
            context["player"].rect = context["player"].rect.move(0, -player_speed)
        if keys[pygame.K_s]:
            context["player"].rect = context["player"].rect.move(0, player_speed)
        if keys[pygame.K_a]:
            context["player"].rect = context["player"].rect.move(-player_speed, 0)
        if keys[pygame.K_d]:
            context["player"].rect = context["player"].rect.move(player_speed, 0)

        if spritecollide(context["player"], context["walls"], dokill=False) or spritecollide(context["player"], context["changing_walls"], dokill=False):
            context["player"].rect.topleft = old_player_topleft

        collided_chests = spritecollide(context["player"], context["chests"], dokill=True)
        context["score"] += len(collided_chests)

        for _ in range(len(collided_chests)):
            chest = Chest(*generate_random_chest_position())
            context["chests"].add(chest)

        draw_whole_screen(screen, context)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
