# Copyright (c) 2026 Alexander Suvorov. All right reserved.
import pygame

from core.utils.colors import Colors


class InputBox:
    def __init__(self, x: int, y: int, width: int, height: int, placeholder: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.placeholder = placeholder
        self.text = ""
        self.active = True
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, Colors.SURFACE, self.rect, border_radius=8)
        pygame.draw.rect(surface, Colors.ACCENT if self.active else Colors.TEXT_SECONDARY,
                         self.rect, 2, border_radius=8)

        display_text = self.text if self.text else self.placeholder
        color = Colors.TEXT_PRIMARY if self.text else Colors.TEXT_SECONDARY
        text_surface = self.font.render(display_text, True, color)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
