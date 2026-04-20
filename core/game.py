# Copyright (c) 2026 Alexander Suvorov. All right reserved.
import os
import sys
import webbrowser
import pygame
from typing import Tuple

from core.models.button import Button
from core.models.food import Food
from core.models.input_box import InputBox
from core.models.snake import Snake
from core.utils.colors import Colors
from core.utils.direction import Direction
from core.utils.position import Position
from tools.database import save_score, get_leaderboard_records

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Game:
    def __init__(self):
        pygame.init()

        self.width = 1000
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game - Old Snake")

        try:
            self.background_image = pygame.image.load(resource_path('data/images/snake.png')).convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
            self.use_background_image = True
        except:
            self.use_background_image = False
            self.background = self.create_background()

        self.clock = pygame.time.Clock()
        self.snake_speed = 15
        self.snake_color = Colors.SNAKE_GREEN
        self.state = "START"
        self.paused = False
        self.score = 0
        self.name_input = None

        self.load_sounds()

        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)

        center_x = self.width // 2
        button_width = 250
        button_height = 60
        spacing = 25
        start_y = 300

        self.start_button = Button(center_x - button_width // 2, start_y,
                                   button_width, button_height, "START GAME",
                                   Colors.ACCENT, Colors.ACCENT_HOVER)

        self.settings_button = Button(center_x - button_width // 2, start_y + button_height + spacing,
                                      button_width, button_height, "SETTINGS",
                                      Colors.SURFACE, Colors.ACCENT)

        self.leaderboard_button = Button(center_x - button_width // 2, start_y + (button_height + spacing) * 2,
                                         button_width, button_height, "LEADERBOARD",
                                         Colors.SURFACE, Colors.ACCENT)

        self.about_button = Button(center_x - button_width // 2, start_y + (button_height + spacing) * 3,
                                   button_width, button_height, "ABOUT",
                                   Colors.SURFACE, Colors.ACCENT)

        self.speed_buttons = []
        self.color_buttons = []
        self.settings_back = None

        self.leaderboard_back = None

        self.github_button = None
        self.about_back = None

        self.reset_game()

    def load_sounds(self):
        try:
            pygame.mixer.music.load(resource_path('data/music/music.mp3'))
            self.button_click = pygame.mixer.Sound(resource_path('data/sounds/button.wav'))
            self.eat_sound = pygame.mixer.Sound(resource_path('data/sounds/eat.wav'))
            pygame.mixer.music.set_volume(0.3)
        except:
            self.button_click = None
            self.eat_sound = None

    def create_background(self) -> pygame.Surface:
        background = pygame.Surface((self.width, self.height))
        for y in range(self.height):
            color_ratio = y / self.height
            color = (
                int(Colors.BACKGROUND[0] * (1 - color_ratio) + Colors.SURFACE[0] * color_ratio),
                int(Colors.BACKGROUND[1] * (1 - color_ratio) + Colors.SURFACE[1] * color_ratio),
                int(Colors.BACKGROUND[2] * (1 - color_ratio) + Colors.SURFACE[2] * color_ratio)
            )
            pygame.draw.line(background, color, (0, y), (self.width, y))
        return background

    def reset_game(self):
        start_x = (self.width // 2) // 20 * 20
        start_y = (self.height // 2) // 20 * 20
        self.snake = Snake(Position(start_x, start_y), self.snake_color)
        self.food = Food(self.width, self.height, self.snake.body)
        self.score = 0
        self.paused = False

    def draw_grid(self):
        for x in range(0, self.width, 20):
            pygame.draw.line(self.screen, (40, 50, 60), (x, 0), (x, self.height), 1)
        for y in range(0, self.height, 20):
            pygame.draw.line(self.screen, (40, 50, 60), (0, y), (self.width, y), 1)

    def draw_background(self):
        if self.use_background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.blit(self.background, (0, 0))

    def draw_gradient_text(self, text: str, font: pygame.font.Font,
                           color: Tuple[int, int, int], rect: pygame.Rect):
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(rect.centerx + 3, rect.centery + 3))
        self.screen.blit(shadow_surface, shadow_rect)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_start_screen(self):
        self.draw_background()
        if self.use_background_image:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

        title_rect = pygame.Rect(0, 80, self.width, 100)
        self.draw_gradient_text("OLD SNAKE", self.title_font, Colors.ACCENT, title_rect)

        subtitle_rect = pygame.Rect(0, 180, self.width, 50)
        self.draw_gradient_text("Classic Snake Game", self.subtitle_font, Colors.TEXT_SECONDARY, subtitle_rect)

        mouse_pos = pygame.mouse.get_pos()
        self.start_button.update_hover(mouse_pos)
        self.settings_button.update_hover(mouse_pos)
        self.leaderboard_button.update_hover(mouse_pos)
        self.about_button.update_hover(mouse_pos)

        self.start_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.leaderboard_button.draw(self.screen)
        self.about_button.draw(self.screen)

    def draw_game_screen(self):
        if self.use_background_image:
            self.screen.fill(Colors.BACKGROUND)
        else:
            self.screen.blit(self.background, (0, 0))

        self.draw_grid()
        self.food.draw(self.screen)
        self.snake.draw(self.screen)

        score_text = f"Score: {self.score}"
        score_surface = self.text_font.render(score_text, True, Colors.TEXT_PRIMARY)
        score_panel = pygame.Rect(10, 10, 180, 50)
        pygame.draw.rect(self.screen, Colors.SURFACE, score_panel, border_radius=10)
        pygame.draw.rect(self.screen, Colors.ACCENT, score_panel, 3, border_radius=10)
        self.screen.blit(score_surface, (20, 18))

        if self.paused:
            pause_text = self.subtitle_font.render("PAUSED", True, Colors.WARNING)
            pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(pause_text, pause_rect)
            hint_text = self.small_font.render("Press SPACE to continue", True, Colors.TEXT_SECONDARY)
            hint_rect = hint_text.get_rect(center=(self.width // 2, self.height // 2 + 60))
            self.screen.blit(hint_text, hint_rect)

    def draw_game_over_screen(self):
        if self.use_background_image:
            self.screen.fill(Colors.BACKGROUND)
        else:
            self.screen.blit(self.background, (0, 0))

        self.draw_grid()

        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill(Colors.BACKGROUND)
        self.screen.blit(overlay, (0, 0))

        title_rect = pygame.Rect(0, 150, self.width, 80)
        self.draw_gradient_text("GAME OVER", self.title_font, Colors.DANGER, title_rect)

        score_text = f"Your score: {self.score}"
        score_rect = pygame.Rect(0, 250, self.width, 50)
        self.draw_gradient_text(score_text, self.subtitle_font, Colors.TEXT_PRIMARY, score_rect)

        input_width = 400
        input_height = 60
        input_x = (self.width - input_width) // 2
        input_y = 340

        if self.name_input is None:
            self.name_input = InputBox(input_x, input_y, input_width, input_height, "Enter your nickname")

        self.name_input.draw(self.screen)

        save_button = Button((self.width - 250) // 2, 430, 250, 60, "SAVE SCORE",
                             Colors.ACCENT, Colors.ACCENT_HOVER)

        mouse_pos = pygame.mouse.get_pos()
        save_button.update_hover(mouse_pos)
        save_button.draw(self.screen)

        return save_button

    def draw_settings_screen(self):
        self.draw_background()
        if self.use_background_image:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

        title_rect = pygame.Rect(0, 50, self.width, 80)
        self.draw_gradient_text("SETTINGS", self.title_font, Colors.ACCENT, title_rect)

        speed_label = self.text_font.render("Game Speed:", True, Colors.TEXT_PRIMARY)
        self.screen.blit(speed_label, (200, 180))

        speeds = [10, 15, 20, 25, 30]
        self.speed_buttons = []
        mouse_pos = pygame.mouse.get_pos()

        for i, speed in enumerate(speeds):
            x = 400 + i * 80
            if self.snake_speed == speed:
                button_color = Colors.ACCENT
                hover_color = Colors.ACCENT_HOVER
            else:
                button_color = Colors.SURFACE
                hover_color = Colors.ACCENT
            button = Button(x, 170, 70, 50, str(speed), button_color, hover_color)
            button.update_hover(mouse_pos)
            self.speed_buttons.append((button, speed))
            button.draw(self.screen)

        color_label = self.text_font.render("Snake Color:", True, Colors.TEXT_PRIMARY)
        self.screen.blit(color_label, (200, 280))

        colors = [
            ("Green", Colors.SNAKE_GREEN), ("Red", Colors.SNAKE_RED),
            ("Blue", Colors.SNAKE_BLUE), ("Yellow", Colors.SNAKE_YELLOW),
            ("Purple", Colors.SNAKE_PURPLE), ("Orange", Colors.SNAKE_ORANGE)
        ]

        self.color_buttons = []
        for i, (name, color) in enumerate(colors):
            x = 200 + (i % 3) * 160
            y = 330 + (i // 3) * 70
            if self.snake_color == color:
                button = Button(x, y, 140, 50, name, color, tuple(min(c + 50, 255) for c in color))
                button.is_selected = True
            else:
                button = Button(x, y, 140, 50, name, color, tuple(min(c + 50, 255) for c in color))
                button.is_selected = False
            button.update_hover(mouse_pos)
            self.color_buttons.append((button, color))
            button.draw(self.screen)
            if self.snake_color == color:
                pygame.draw.rect(self.screen, Colors.TEXT_PRIMARY, button.rect, 3, border_radius=12)

        self.settings_back = Button((self.width - 250) // 2, 550, 250, 60, "BACK TO MENU",
                                    Colors.SURFACE, Colors.ACCENT)
        self.settings_back.update_hover(mouse_pos)
        self.settings_back.draw(self.screen)

    def draw_leaderboard_screen(self):
        self.draw_background()
        if self.use_background_image:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

        title_rect = pygame.Rect(0, 50, self.width, 80)
        self.draw_gradient_text("LEADERBOARD", self.title_font, Colors.ACCENT, title_rect)

        records = get_leaderboard_records()
        start_y = 160
        row_height = 55

        headers = ["#", "PLAYER", "SCORE"]
        for i, header in enumerate(headers):
            x = 250 + i * 250
            text = self.text_font.render(header, True, Colors.ACCENT)
            self.screen.blit(text, (x, start_y - 40))

        for i, (nickname, score) in enumerate(records[:10]):
            y = start_y + i * row_height
            if i % 2 == 0:
                pygame.draw.rect(self.screen, Colors.SURFACE, (180, y, 640, row_height))

            number = self.text_font.render(str(i + 1), True, Colors.TEXT_SECONDARY)
            self.screen.blit(number, (250, y + 15))

            name = self.text_font.render(nickname[:20], True, Colors.TEXT_PRIMARY)
            self.screen.blit(name, (380, y + 15))

            score_display = self.text_font.render(str(score), True, Colors.WARNING)
            self.screen.blit(score_display, (650, y + 15))

        mouse_pos = pygame.mouse.get_pos()
        self.leaderboard_back = Button((self.width - 250) // 2, self.height - 100, 250, 60, "BACK TO MENU",
                                       Colors.SURFACE, Colors.ACCENT)
        self.leaderboard_back.update_hover(mouse_pos)
        self.leaderboard_back.draw(self.screen)

    def draw_about_screen(self):
        self.draw_background()
        if self.use_background_image:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

        title_rect = pygame.Rect(0, 50, self.width, 80)
        self.draw_gradient_text("ABOUT", self.title_font, Colors.ACCENT, title_rect)

        info = [
            "Classic Snake Game",
            "",
            "Controls:",
            "• Arrow Keys or WASD to move",
            "• Space to pause",
            "",
            "Version: 2.0"
        ]

        y = 180
        for line in info:
            if line:
                text = self.text_font.render(line, True, Colors.TEXT_PRIMARY)
                text_rect = text.get_rect(center=(self.width // 2, y))
                self.screen.blit(text, text_rect)
            y += 45

        mouse_pos = pygame.mouse.get_pos()

        self.github_button = Button((self.width - 200) // 2, 420, 200, 45, "GitHub",
                                    Colors.SURFACE, Colors.ACCENT)
        self.github_button.update_hover(mouse_pos)
        self.github_button.draw(self.screen)

        self.about_back = Button((self.width - 200) // 2, 480, 200, 45, "BACK",
                                 Colors.SURFACE, Colors.ACCENT)
        self.about_back.update_hover(mouse_pos)
        self.about_back.draw(self.screen)

    def run(self):
        running = True
        pygame.mixer.music.play(-1)
        save_button = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == "START":
                    if self.start_button.is_clicked(event):
                        if self.button_click: self.button_click.play()
                        self.state = "PLAYING"
                        self.reset_game()
                    elif self.settings_button.is_clicked(event):
                        if self.button_click: self.button_click.play()
                        self.state = "SETTINGS"
                    elif self.leaderboard_button.is_clicked(event):
                        if self.button_click: self.button_click.play()
                        self.state = "LEADERBOARD"
                    elif self.about_button.is_clicked(event):
                        if self.button_click: self.button_click.play()
                        self.state = "ABOUT"

                elif self.state == "PLAYING":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.paused = not self.paused

                elif self.state == "GAME_OVER":
                    if self.name_input:
                        self.name_input.handle_event(event)
                    if save_button and save_button.is_clicked(event):
                        if self.name_input and self.name_input.text:
                            save_score(self.name_input.text, self.score)
                            self.state = "LEADERBOARD"
                            self.name_input = None
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if self.name_input and self.name_input.text:
                            save_score(self.name_input.text, self.score)
                            self.state = "LEADERBOARD"
                            self.name_input = None

                elif self.state == "SETTINGS":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for button, speed in self.speed_buttons:
                            if button.is_clicked(event):
                                self.snake_speed = speed
                        for button, color in self.color_buttons:
                            if button.is_clicked(event):
                                self.snake_color = color
                        if self.settings_back and self.settings_back.is_clicked(event):
                            if self.button_click: self.button_click.play()
                            self.state = "START"

                elif self.state == "LEADERBOARD":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.leaderboard_back and self.leaderboard_back.is_clicked(event):
                            if self.button_click: self.button_click.play()
                            self.state = "START"

                elif self.state == "ABOUT":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.github_button and self.github_button.is_clicked(event):
                            if self.button_click: self.button_click.play()
                            webbrowser.open("https://www.github.com/aixandrolab")
                        elif self.about_back and self.about_back.is_clicked(event):
                            if self.button_click: self.button_click.play()
                            self.state = "START"

            if self.state == "PLAYING" and not self.paused:
                self.snake.move()

                if self.snake.body[-1].x == self.food.position.x and self.snake.body[-1].y == self.food.position.y:
                    self.snake.grow()
                    self.score += 1
                    self.food.respawn(self.snake.body)
                    if self.eat_sound: self.eat_sound.play()

                if self.snake.check_collision(self.width, self.height):
                    self.state = "GAME_OVER"
                    pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.load(resource_path('data/music/game_over.mp3'))
                        pygame.mixer.music.play()
                    except:
                        pass

            if self.state == "PLAYING" and not self.paused:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.snake.change_direction(Direction.LEFT)
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.snake.change_direction(Direction.RIGHT)
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.snake.change_direction(Direction.UP)
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.snake.change_direction(Direction.DOWN)

            if self.state == "START":
                self.draw_start_screen()
            elif self.state == "PLAYING":
                self.draw_game_screen()
            elif self.state == "GAME_OVER":
                save_button = self.draw_game_over_screen()
            elif self.state == "SETTINGS":
                self.draw_settings_screen()
            elif self.state == "LEADERBOARD":
                self.draw_leaderboard_screen()
            elif self.state == "ABOUT":
                self.draw_about_screen()

            pygame.display.flip()
            self.clock.tick(self.snake_speed)

        pygame.quit()
        sys.exit()
