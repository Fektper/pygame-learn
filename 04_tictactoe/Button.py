import pygame
from typing import Callable, Union

def text_fits_rect(text: str, size: int, area: pygame.Rect) -> bool:
    text_surface: pygame.Surface = pygame.font.SysFont(None, size).render(text, False, "black")
    if text_surface.get_rect().w <= area.w and text_surface.get_rect().h <= area.h:
        return True
    
    return False

def get_max_fit_fontsize(text, area, max_font_size = None):
    top = 1
    if max_font_size is None:
        while text_fits_rect(text, top, area):
            top = 2 * top
    else:
        top = max_font_size

    bot = 1
    while top > bot + 1:
        mid = int((top + bot)/2)
        if text_fits_rect(text, mid, area):
            bot = mid
        else:
            top = mid

    if text_fits_rect(text, top, area):
        return top
    else:
        return bot

class PrerenderedButton:
    def __init__(self, text: str, area_rect: pygame.Rect, text_color: pygame.Color, background_color: pygame.Color, 
                 max_font_size: int = 30, pixel_grow_amout: int = 10):
        self.text = text
        self.text_color = text_color
        self.max_font_size = max_font_size

        self.area_rect = area_rect
        self.background_color = background_color

        if not text_fits_rect(text, max_font_size, area_rect):
            self.max_font_size = get_max_fit_fontsize(text, max_font_size)

        self.text_rendered = pygame.font.SysFont(None, self.max_font_size).render(self.text, True, self.text_color)

        x_offset = self.area_rect.x + int((self.area_rect.width - self.text_rendered.get_rect().width)/2)
        y_offset = self.area_rect.y + int((self.area_rect.height - self.text_rendered.get_rect().height)/2)
        self.text_pos = pygame.Rect.move(self.text_rendered.get_rect(), x_offset, y_offset)

        self.callback: Union[None, Callable] = None

        self.hover_end_time: float = 0.1
        self.hover_time: float = 0
        self.grow_x: int = int(pixel_grow_amout * area_rect.w / max(area_rect.w, area_rect.h))
        self.grow_y: int = int(pixel_grow_amout * area_rect.h / max(area_rect.w, area_rect.h))

    def render_on(self, screen: pygame.Surface):
        dx = int(self.grow_x * (self.hover_time / self.hover_end_time))
        dy = int(self.grow_y * (self.hover_time / self.hover_end_time))
        new_rct = self.area_rect.copy()
        new_rct.h += dy
        new_rct.w += dx
        of_x = -int(dx / 2)
        of_y = -int(dy / 2)
        pygame.draw.rect(screen, self.background_color, new_rct.move(of_x, of_y))
        # pygame.draw.rect(screen, self.background_color,self.area_rect)

        screen.blit(self.text_rendered, self.text_pos)

    def bind_func(self, func: Callable):
        self.callback = func

    def update(self, mouse_pos, mouse_clicked: bool, dt: float):
        mouse_over = self.area_rect.collidepoint(*mouse_pos)

        if mouse_clicked and mouse_over and not self.callback is None:
            self.callback()

        if mouse_over:
            self.hover_time += dt
            self.hover_time = min(self.hover_end_time, self.hover_time)
        else:
            self.hover_time = 0
        