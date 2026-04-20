# Copyright (c) 2026 Alexander Suvorov. All right reserved.
import pygame
from typing import List, Tuple

from core.utils.colors import Colors
from core.utils.direction import Direction
from core.utils.position import Position

class Snake:
    def __init__(self, start_pos: Position, color: Tuple[int, int, int] = Colors.SNAKE_GREEN):
        self.body: List[Position] = [start_pos]
        self.direction = Direction.RIGHT
        self.color = color
        self.grow_flag = False

    def move(self) -> None:
        head = self.body[-1]
        new_head = Position(
            head.x + self.direction.value[0] * 20,
            head.y + self.direction.value[1] * 20
        )
        self.body.append(new_head)

        if not self.grow_flag:
            self.body.pop(0)
        else:
            self.grow_flag = False

    def change_direction(self, new_direction: Direction) -> None:
        if (self.direction == Direction.UP and new_direction != Direction.DOWN or
                self.direction == Direction.DOWN and new_direction != Direction.UP or
                self.direction == Direction.LEFT and new_direction != Direction.RIGHT or
                self.direction == Direction.RIGHT and new_direction != Direction.LEFT):
            self.direction = new_direction

    def grow(self) -> None:
        self.grow_flag = True

    def check_collision(self, width: int, height: int) -> bool:
        head = self.body[-1]
        if head.x < 0 or head.x >= width or head.y < 0 or head.y >= height:
            return True
        for segment in self.body[:-1]:
            if segment.x == head.x and segment.y == head.y:
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        for i, segment in enumerate(self.body):
            if i == len(self.body) - 1:
                color = tuple(min(c + 40, 255) for c in self.color)
            else:
                color = self.color

            pygame.draw.rect(surface, color, (segment.x, segment.y, 20, 20), border_radius=5)

            if i != len(self.body) - 1:
                highlight_rect = pygame.Rect(segment.x + 2, segment.y + 2, 16, 8)
                pygame.draw.rect(surface, (255, 255, 255, 50), highlight_rect, border_radius=3)

            if i == len(self.body) - 1:
                eye_size = 4
                if self.direction == Direction.RIGHT:
                    pygame.draw.circle(surface, Colors.TEXT_PRIMARY, (segment.x + 15, segment.y + 6), eye_size)
                    pygame.draw.circle(surface, Colors.TEXT_PRIMARY, (segment.x + 15, segment.y + 14), eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), (segment.x + 16, segment.y + 6), 2)
                    pygame.draw.circle(surface, (0, 0, 0), (segment.x + 16, segment.y + 14), 2)
                    pygame.draw.circle(surface, (255, 255, 255), (segment.x + 15, segment.y + 5), 1)
                    pygame.draw.circle(surface, (255, 255, 255), (segment.x + 15, segment.y + 13), 1)
                elif self.direction == Direction.LEFT:
                    pygame.draw.circle(surface, Colors.TEXT_PRIMARY, (segment.x + 5, segment.y + 6), eye_size)
                    pygame.draw.circle(surface, Colors.TEXT_PRIMARY, (segment.x + 5, segment.y + 14), eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), (segment.x + 4, segment.y + 6), 2)
                    pygame.draw.circle(surface, (0, 0, 0), (segment.x + 4, segment.y + 14), 2)
                    pygame.draw.circle(surface, (255, 255, 255), (segment.x + 5, segment.y + 5), 1)
                    pygame.draw.circle(surface, (255, 255, 255), (segment.x + 5, segment.y + 13), 1)
                elif self.direction == Direction.UP:
                    pygame.draw.circle(surface, Colors.TEXT_PRIMARY, (segment.x + 6, segment.y + 5), eye_size)
                    pygame.draw.circle(surface, Colors.TEXT_PRIMARY, (segment.x + 14, segment.y + 5), eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), (segment.x + 6, segment.y + 4), 2)
                    pygame.draw.circle(surface, (0, 0, 0), (segment.x + 14, segment.y + 4), 2)
                    pygame.draw.circle(surface, (255, 255, 255), (segment.x + 5, segment.y + 5), 1)
                    pygame.draw.circle(surface, (255, 255, 255), (segment.x + 13, segment.y + 5), 1)
                else:
                    pygame.draw.circle(surface, Colors.TEXT_PRIMARY, (segment.x + 6, segment.y + 15), eye_size)
                    pygame.draw.circle(surface, Colors.TEXT_PRIMARY, (segment.x + 14, segment.y + 15), eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), (segment.x + 6, segment.y + 16), 2)
                    pygame.draw.circle(surface, (0, 0, 0), (segment.x + 14, segment.y + 16), 2)
                    pygame.draw.circle(surface, (255, 255, 255), (segment.x + 5, segment.y + 15), 1)
                    pygame.draw.circle(surface, (255, 255, 255), (segment.x + 13, segment.y + 15), 1)
