"""
## Модуль графических кнопок.
"""


import os
import webbrowser
import requests
import pygame
from webserver import run_protosite
pygame.init()


class CommonButton(object):
    """
    #### Прототипированный класс обычной кнопки.

    Реализует простое кнопочное поведение виджета.
    """
    width: int = 0
    height: int = 0
    has_been_click: bool
    position: tuple[int, int] = (0, 0)

    def __init__(self, width: int, height: int, position: tuple[int, int]) -> None:
        """
        :param position: принимает два целочисленных значения в виде кортежа.
        """
        self.width = width
        self.height = height
        self.position = position
        self.has_been_click: bool = False

        self.path: str = r"assets\butpng.png"

        if not os.path.exists(self.path):
            response: requests.Response = requests.get("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQa57563qvcJ0uB9eRc7oVW1DBd2WQSE5xYA&s")
            with open(self.path, "wb") as file:
                file.write(response.content)

        self.texture: pygame.Surface = pygame.image.load(self.path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.texture.set_colorkey(pygame.Color(255, 255, 255))

        self.rect: pygame.Rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.__i: float = 0.0

        self.sound: pygame.mixer.Sound = pygame.mixer.Sound("assets\knopka-schelchok-shumnyii-blizkii1.mp3")
        self.sound.set_volume(0.2)

    def __str__(self) -> str:
        """
        Строковое представление.
        """
        return "CommonButton--%d" % id(self)

    def if_click(self, event: pygame.event.Event) -> None:
        """
        :param event: принимает тип данных события - 'event.Event'.
        Метод реализующий простенькую логику вседствии нажатия на кнопку.
        """
        rect: pygame.Rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        if rect.colliderect(self.rect):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.sound.play()
                self.has_been_click = True
                self.texture.set_alpha(200)
            else:
                self.texture.set_alpha(255)
                self.has_been_click = False
                self.__i = 0.0

    def draw(self, window: pygame.Surface, text: pygame.Surface = None, vert_or_hor: str = None, to_mark: bool = False) -> None:
        """
        :param window: принимает экземпляр типа 'pygame.Surface'.
        :param text: принимает в качестве аргумента текстовую поверхность типа 'pygame.Surface'.
        Метод для отрисовки обычной кнопки.
        """
        window.blit(self.texture, self.position)
        if text:
            if vert_or_hor == "hor" or not vert_or_hor:
                if to_mark:
                    pygame.draw.rect(window, "darkcyan", text.get_rect(topleft=(self.position[0], self.position[1] - self.height // 2)), 0)
                window.blit(text, (self.position[0], self.position[1] - self.height // 2))
            elif vert_or_hor == "vert":
                if to_mark:
                    pygame.draw.rect(window, "darkcyan", text.get_rect(topleft=(self.position[0] + self.height * 2.25, self.position[1])), 0)
                window.blit(text, (self.position[0] + self.height * 2.25, self.position[1]))


class ButtonWithLink(CommonButton):
    """
    #### Класс прототипированной кнопки с ссылкой на сайт.

    Пожалуй единственный класс-наследник имеющий столь узкую специализацию.
    """

    def __init__(self, width: int, height: int, position: tuple[int, int]) -> None:
        """
        Инициализация объекта этого типа.
        """
        super().__init__(width, height, position)

    def __str__(self) -> str:
        """
        Строковое представление.
        """
        return "ButtonWithLink--%d" % id(self)
    
    def if_click(self, event: pygame.event.Event) -> None:
        """
        Перегруженный метод из 'CommonButton'.
        """
        if self.has_been_click:
            webbrowser.open("http://localhost:7000/")
            run_protosite()
        return super().if_click(event)
        

if __name__ == "__main__":
    pass
