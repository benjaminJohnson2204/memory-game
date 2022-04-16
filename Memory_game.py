import pygame
import math
import random

pygame.init()


def randomize_order(a_list):
    return random.sample(a_list, len(a_list))


window_width = 1000
window_height = 1000
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Memory Game")
clock = pygame.time.Clock()
success_message = pygame.image.load('Success Message.png')

board_x = 5
board_y = 5
frames_per_second = 10

#         R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 200, 25)
CYAN = (0, 200, 255)
ORANGE = (255, 128, 0)
VIOLET = (128, 0, 255)
colors_used = [RED, GREEN, BLUE, MAGENTA, YELLOW, CYAN, ORANGE, VIOLET]
sides_used = [3, 4, 5, 6]


class Polygon:
    radius = 35

    def __init__(self, center_x, center_y, side_number, color):
        self.x_center = center_x
        self.y_center = center_y
        self.number_of_sides = side_number
        self.color = color

    def get_points(self):
        points = []
        internal_angles = 360 / self.number_of_sides
        theta = 0
        while theta < 360:
            x = self.radius * math.cos(theta * math.pi / 180) + self.x_center
            y = - self.radius * math.sin(theta * math.pi / 180) + self.y_center
            points.append([int(x), int(y)])
            theta += internal_angles
        return points

    def draw(self):
        pygame.draw.polygon(window, self.color, self.get_points())


def assign_shapes(quantity):
    if quantity > len(sides_used) * len(colors_used):
        return False
    result = []
    while len(result) < quantity:
        candidate = [random.choice(sides_used), random.choice(colors_used)]
        if candidate not in result:
            result.append(candidate)
    return result


class MemoryTile:
    spacing = 20
    width = 150
    height = 150
    color = WHITE

    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.x_position = x_coord * (self.width + self.spacing) + self.spacing
        self.center_x = int(self.x_position + self.width / 2)
        self.y_coord = y_coord
        self.y_position = y_coord * (self.height + self.spacing) + self.spacing
        self.center_y = int(self.y_position + self.height / 2)
        self.icon = None
        self.flipped = False
        self.paired = False

    def draw(self):
        if not self.paired:
            pygame.draw.rect(window, self.color, (self.x_position, self.y_position, self.width, self.height))
            if self.flipped:
                self.icon.draw()

    def is_selected(self, x_indicator, y_indicator):
        result = x_indicator * (self.width + self.spacing) + self.spacing == self.x_position and \
                 y_indicator * (self.height + self.spacing) + self.spacing == self.y_position
        return result

    def flip_over(self):
        self.flipped = True

    def moused_over(self, mouse_x, mouse_y):
        return self.x_position <= mouse_x <= self.x_position + self.width and \
               self.y_position <= mouse_y <= self.y_position + self.height


def are_same_icon(icon1, icon2):
    return icon1.number_of_sides == icon2.number_of_sides and icon1.color == icon2.color


def tile_index_to_position(index, is_x):
    dimension = MemoryTile.width if is_x else MemoryTile.height
    return int(index * (dimension + MemoryTile.spacing) + MemoryTile.spacing / 2)


def redraw_game(tiles, x_indicator, y_indicator):
    window.fill(BLACK)
    pygame.draw.rect(window, RED,
                     (tile_index_to_position(x_indicator, True), tile_index_to_position(y_indicator, False),
                      MemoryTile.width + MemoryTile.spacing, MemoryTile.height + MemoryTile.spacing),
                     int(MemoryTile.spacing / 4))
    for tile in tiles:
        tile.draw()
    pygame.display.update()


def play():
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    indicator_tile_x = 0
    indicator_tile_y = 0
    tiles = []
    for y in range(board_y):
        for x in range(board_x):
            tiles.append(MemoryTile(x, y))
    shapes_used = assign_shapes(board_x * board_y / 2)
    shapes_used_2 = randomize_order(shapes_used)
    shapes_used.extend(shapes_used_2)
    for i in range(len(tiles)):
        tiles[i].icon = Polygon(tiles[i].center_x, tiles[i].center_y, shapes_used[i][0], shapes_used[i][1])
    playing = True
    paired_tiles_indices = []
    while playing:
        clock.tick(frames_per_second)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            for tile in tiles:
                if tile.moused_over(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    indicator_tile_x = tile.x_coord
                    indicator_tile_y = tile.y_coord
                    tile.flip_over()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            first_try = "left"
        elif keys[pygame.K_RIGHT]:
            first_try = "right"
        elif keys[pygame.K_UP]:
            first_try = "up"
        elif keys[pygame.K_DOWN]:
            first_try = "down"
        else:
            first_try = None
        success = False
        shifted = 0
        maximum = board_x if first_try in ["left", "right"] else board_y
        while [indicator_tile_x % board_x, indicator_tile_y % board_y] in paired_tiles_indices:
            shifted += 1
            if first_try == "left":
                indicator_tile_x -= 1
            elif first_try == "right":
                indicator_tile_x += 1
            elif first_try == "up":
                indicator_tile_y -= 1
            elif first_try == "down":
                indicator_tile_y += 1
            if shifted > maximum:
                break
        else:
            if first_try == "left":
                indicator_tile_x -= 1
            elif first_try == "right":
                indicator_tile_x += 1
            elif first_try == "up":
                indicator_tile_y -= 1
            elif first_try == "down":
                indicator_tile_y += 1
            success = True
        if not success:
            if first_try in ["left", "right"]:
                indicator_tile_x += 1 if first_try == "left" else -1
                for tile in tiles:
                    if (not tile.paired) and tile.x_coord == indicator_tile_x:
                        indicator_tile_y = tile.y_coord
                        break
            else:
                indicator_tile_y += 1 if first_try == "down" else -1
                for tile in tiles:
                    if (not tile.paired) and tile.y_coord == indicator_tile_y:
                        indicator_tile_x = tile.x_coord
                        break
        indicator_tile_x, indicator_tile_y = indicator_tile_x % board_x, indicator_tile_y % board_y
        if keys[pygame.K_SPACE]:
            for tile in tiles:
                if tile.is_selected(indicator_tile_x, indicator_tile_y):
                    tile.flip_over()
        redraw_game(tiles, indicator_tile_x, indicator_tile_y)
        flipped_tiles = []
        for tile in tiles:
            if tile.flipped:
                flipped_tiles.append(tile)
        if len(flipped_tiles) >= 2:
            flipped_tiles[0].flipped = False
            flipped_tiles[1].flipped = False
            if are_same_icon(flipped_tiles[0].icon, flipped_tiles[1].icon):
                flipped_tiles[0].paired = True
                flipped_tiles[1].paired = True
                paired_tiles_indices.append([flipped_tiles[0].x_coord, flipped_tiles[0].y_coord])
                paired_tiles_indices.append([flipped_tiles[1].x_coord, flipped_tiles[1].y_coord])
            clock.tick(frames_per_second / 5)

        if len(paired_tiles_indices) >= len(tiles):
            window.fill(BLACK)
            window.blit(success_message, (int(window_width / 2), int(window_height / 2)))
            pygame.display.update()
            keys = pygame.key.get_pressed()
            for i in range(frames_per_second * 10):
                clock.tick(frames_per_second)
                if keys[pygame.K_SPACE]:
                    break
            else:
                pygame.quit()


if __name__ == "__main__":
    play()
