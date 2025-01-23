import pygame
from abc import ABC, abstractmethod
from typing import Callable, Iterable, Union
from Button import PrerenderedButton

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


class MenuScene(Scene):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        button_width = int(width / 2)
        button_height = 75
        first_button_rect = pygame.Rect(int(width/2 - button_width/2), 300, button_width, button_height)
        print(first_button_rect)

        self.play_game_button = PrerenderedButton("Play", first_button_rect, "white", "black", 90)# Button()
        self.quit_button = PrerenderedButton("Quit", first_button_rect.move(0, button_height + 50), "white", "black", 90) # Button

        self.play_game_button.bind_func(lambda: print("Play"))
        self.quit_button.bind_func(lambda: pygame.event.post(pygame.Event(pygame.QUIT)))

        self.scene_switch_func: Union[None, Callable] = None

    def update(self, events: Iterable[pygame.Event], dt: float):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.play_game_button.trigger_if_clicked(mouse_pos)
                self.quit_button.trigger_if_clicked(mouse_pos)

    def render(self, screen: pygame.Surface):
        title_font = pygame.font.SysFont(None, 120).render("Tic Tac Toe", True, "black")
        screen.blit(title_font, (int(self.width/2) - int(title_font.get_rect().width/2), 150))
        self.play_game_button.render_on(screen)
        self.quit_button.render_on(screen)

    def bind_scene_switch(self, func):
        self.scene_switch_func = func