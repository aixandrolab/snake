# Copyright (c) 2026 Alexander Suvorov. All right reserved.
import pygame
from typing import Tuple

from core.utils.colors import Colors


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 color: Tuple[int, int, int], hover_color: Tuple[int, int, int],
                 text_color: Tuple[int, int, int] = Colors.TEXT_PRIMARY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 32)

    def draw(self, surface: pygame.Surface) -> None:
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, Colors.TEXT_PRIMARY, self.rect, 2, border_radius=12)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update_hover(self, pos: Tuple[int, int]) -> None:
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False
