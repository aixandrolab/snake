# Copyright (c) 2026 Alexander Suvorov. All right reserved.
import random
import pygame
from typing import List

from core.utils.colors import Colors
from core.utils.position import Position


class Food:
    def __init__(self, width: int, height: int, snake_body: List[Position]):
        self.width = width
        self.height = height
        self.position = self.generate_position(snake_body)
        self.animation_offset = 0

    def generate_position(self, snake_body: List[Position]) -> Position:
        max_attempts = 1000
        for _ in range(max_attempts):
            pos = Position(
                random.randrange(0, self.width - 20, 20),
                random.randrange(0, self.height - 20, 20)
            )
            if pos not in snake_body:
                return pos
        for x in range(0, self.width - 20, 20):
            for y in range(0, self.height - 20, 20):
                pos = Position(x, y)
                if pos not in snake_body:
                    return pos
        return Position(0, 0)

    def respawn(self, snake_body: List[Position]) -> None:
        self.position = self.generate_position(snake_body)

    def draw(self, surface: pygame.Surface) -> None:
        self.animation_offset = (self.animation_offset + 0.1) % (2 * 3.14159)
        scale = 1 + abs(0.15 * self.animation_offset)
        center_x = self.position.x + 10
        center_y = self.position.y + 10
        radius = int(10 * scale)

        for i in range(3):
            alpha = 255 - i * 80
            glow_surface = pygame.Surface((radius * 2 + i * 4, radius * 2 + i * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*Colors.FOOD_GLOW, alpha),
                               (radius + i * 2, radius + i * 2), radius + i * 2)
            surface.blit(glow_surface, (center_x - radius - i * 2, center_y - radius - i * 2))

        pygame.draw.circle(surface, Colors.FOOD, (center_x, center_y), radius)
        leaf_points = [
            (center_x + radius - 2, center_y - radius + 2),
            (center_x + radius + 4, center_y - radius - 2),
            (center_x + radius, center_y - radius - 4)
        ]
        pygame.draw.polygon(surface, (80, 180, 80), leaf_points)
