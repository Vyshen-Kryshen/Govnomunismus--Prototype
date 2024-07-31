"""
Модуль игровых классов объектов.
"""
import pygame
from PCymple import ColliderCircle, Vec2
pygame.init()


class GameObject(ColliderCircle):
    """
    #### Класс игрового объекта.
    """
    texture: pygame.Surface
    window: pygame.Surface

    def __init__(self, center: tuple[float, float], direction: tuple[float, float], radius: float, mass: int, texture: pygame.Surface, 
                window: pygame.Surface, *args: any, **kw: any) -> None:
        """
        Инициализатор с реализацией множественного наследования.
        """
        super().__init__(center, direction, radius, mass, *args, **kw)
        self.texture = texture
        self.texture = pygame.transform.scale(self.texture, (self.radius, self.radius))
        self.window = window

    def move(self) -> None:
        """
        Метод для движения игрового объекта.
        """
        if self.directionOnX:
            self.centerX += self.directionOnX
        if self.directionOnY:
            self.centerY += self.directionOnY

    def rot(self, dangle: float) -> None:
        """
        :param dangle: принимает вещественный тип данных в качестве угловой разницы (дельты).
        Данный метод есть воплощение механики вращения текстуры игрового тела.
        """
        self.texture = pygame.transform.rotate(self.texture, dangle)

    def draw(self) -> None:
        """
        Метод отрисовывающий игровой объект.
        """
        self.texture.fill("white")
        self.window.blit(self.texture, (self.centerX + self.radius, self.centerY + self.radius))


class BuildConstruction(GameObject):
    """
    #### Прототипированный класс строй-конструкции.
    """
    side: str = ""

    def __init__(self, center: tuple[float, float], direction: tuple[float, float], radius: float, mass: int, texture: pygame.Surface, 
                window: pygame.Surface, side: str, *args: any, **kw: any) -> None:
        """
        Инициализатор класса.
        """
        super().__init__(center, direction, radius, mass, texture, window, *args, **kw)
        self.side = side

    def do_construct(self) -> None:
        """
        Метод для постройки здания.
        """
        raise NotImplementedError("Метод не реализован, а отложен на небольшой срок!")

    def select(self) -> None:
        """
        Метод для избрания постройки.
        """
        raise NotImplementedError("Метод не реализован, а отложен на небольшой срок!")


class HandSelectUnit(GameObject):
    """
    #### Прототипированный класс ручно-выбераемого юнита.
    """
    side: str = ""

    def __init__(self, center: tuple[float, float], direction: tuple[float, float], radius: float, mass: int, texture: pygame.Surface, 
                window: pygame.Surface, side: str, *args: any, **kw: any) -> None:
        """
        Инициализатор класса.
        """
        super().__init__(center, direction, radius, mass, texture, window, *args, **kw)
        self.side = side

    def summon(self) -> None:
        """
        Метод для призыва юнита.
        """
        raise NotImplementedError("Метод не реализован, а отложен на небольшой срок!")

    def select(self) -> None:
        """
        Метод для избрания юнита.
        """
        raise NotImplementedError("Метод не реализован, а отложен на небольшой срок!")


if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    go1 = GameObject((0.0, 0.0), (0.75, 0.5), 100.0, 15.0, pygame.Surface((100, 100)), screen)
    go2 = GameObject((600.0, 300.0), (1.0, -1.0), 100.0, 15.0, pygame.Surface((100, 100)), screen)
    print(go1.directionOnX, go1.directionOnY)
    go1vec = Vec2(go1.directionOnX, go1.directionOnY)
    go2vec = Vec2(go2.directionOnX, go2.directionOnY)
    go1vec.vecrefl(go2vec)
    go1.directionOnX, go1.directionOnY = go1vec.f, go1vec.s
    print(go1.directionOnX, go1.directionOnY)
    # while True:
    #     screen.fill("black")
    #     go1.draw()
    #     go2.draw()
    #     print(go1.directionOnX, go1.directionOnY)
    #     if go1.check_collision(go2):
    #         go1.handle_of_collide(go2)
    #     go1.move()
    #     [pygame.quit() for event in pygame.event.get() if event.type == pygame.QUIT]
    #     pygame.display.flip()
    #     clock.tick(60)
