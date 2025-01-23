import pygame
from abc import ABC, abstractmethod
from typing import Callable, Iterable, Union
from Button import PrerenderedButton
import math
from TicTacToe import make_move, check_win

class Scene(ABC):

    @abstractmethod
    def update(self, events: Iterable[pygame.Event], dt: float):
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass

    @abstractmethod
    def bind_scene_switch(self, func: Callable):
        pass


class GameScene(Scene):
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.grid: list[list[int]] = [[0 for _ in range(3)] for _ in range(3)]

        self.player_turn = True
        self.winner = 0
        self.win_timeout = 3
        self.win_fade_time = 2
        self.scene_switch_func = None
        pass

    def update(self, events, dt):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = any([x.type == pygame.MOUSEBUTTONDOWN for x in events])
        self.winner = check_win(self.grid)

        if not self.winner == 0 and self.win_fade_time <= 0:
            if self.win_timeout > 0:
                self.win_timeout -= dt
            elif not self.scene_switch_func is None:
                self.scene_switch_func()

            return
        elif not self.winner == 0:
            self.win_fade_time -= dt
            return
        
        if self.player_turn and mouse_clicked:
            x = int(mouse_pos[0] / (self.width / 3))
            y = int(mouse_pos[1] / (self.width / 3))
            x = min(x, 2)
            y = min(y, 2)

            if self.grid[y][x] == 0:
                self.grid[y][x] = 1
                self.player_turn = False
        elif not self.player_turn:
            x, y = make_move(self.grid)
            self.grid[y][x] = 2
            self.player_turn = True
        

    def render(self, screen):
        if not self.winner == 0 and self.win_fade_time <= 0:
            text = f"Player {self.winner} won!"
            win_text = pygame.font.SysFont(None, 150).render(text, True, "#2c3e50")
            screen.blit(win_text, (int((self.width - win_text.get_width())/2), int((self.height - win_text.get_height())/2)))
            return
        
        grid_line_width = 10
        grid_box_width = math.ceil((self.width - 2 * grid_line_width) / 3)
        grid_box_height = math.ceil((self.height - 2 * grid_line_width) / 3)

        pygame.draw.rect(screen, "#2c3e50", (0, 0, self.width, self.height))

        for x in range(3):
            x_pos = x * (grid_line_width + grid_box_width)
            for y in range(3):
                y_pos = y * (grid_line_width + grid_box_height)
                pygame.draw.rect(screen, "white", (x_pos, y_pos, grid_box_width, grid_box_height))

                if self.grid[y][x] == 1:
                    pygame.draw.circle(screen, "red", (x_pos + int(grid_box_width/2), y_pos + int(grid_box_height/2)), int(min(grid_box_height, grid_box_width)/2) - 10)
                elif self.grid[y][x] == 2:
                    pygame.draw.rect(screen, "blue", (x_pos + 10, y_pos + 10, grid_box_width - 20, grid_box_height - 20))

    def bind_scene_switch(self, func):
        menu_scene = MenuScene(self.width, self.height)
        menu_scene.bind_scene_switch(func)
        swap_scene_func = lambda: func(menu_scene)
        self.scene_switch_func = swap_scene_func

class MenuScene(Scene):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        button_width = int(width / 2)
        button_height = 75
        first_button_rect = pygame.Rect(int(width/2 - button_width/2), 300, button_width, button_height)

        self.play_game_button = PrerenderedButton("Play", first_button_rect, "white", "#27ae60", 90)# Button()
        self.quit_button = PrerenderedButton("Quit", first_button_rect.move(0, button_height + 50), "white", "#c0392b", 90) # Button

        self.play_game_button.bind_func(lambda: self.create_game_scene_and_swap())
        self.quit_button.bind_func(lambda: pygame.event.post(pygame.Event(pygame.QUIT)))

        self.scene_switch_func: Union[None, Callable] = None

    def update(self, events: Iterable[pygame.Event], dt: float):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = any([x.type == pygame.MOUSEBUTTONDOWN for x in events])

        self.play_game_button.update(mouse_pos, mouse_clicked, dt)
        self.quit_button.update(mouse_pos, mouse_clicked, dt)
        

    def render(self, screen: pygame.Surface):
        title_font = pygame.font.SysFont(None, 120).render("Tic Tac Toe", True, "#2c3e50")
        screen.blit(title_font, (int(self.width/2) - int(title_font.get_rect().width/2), 150))
        self.play_game_button.render_on(screen)
        self.quit_button.render_on(screen)

    def bind_scene_switch(self, func):
        self.scene_switch_func = func

    def create_game_scene_and_swap(self):
        game_scene = GameScene(self.width, self.height)
        game_scene.bind_scene_switch(self.scene_switch_func)
        if not self.scene_switch_func is None:
            self.scene_switch_func(game_scene)