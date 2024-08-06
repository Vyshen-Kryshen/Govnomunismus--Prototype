"""
## Модуль игровых классов объектов.
"""


import math
import pygame
from pygame.rect import Rect
from PCymple import ColliderCircle, Vec2
pygame.init()


class GameObject(ColliderCircle):
    """
    #### Класс игрового объекта.
    
    Является обёрткой над коллизионным кругом, по сути это аналог класса 'Sprite' из модуля 'pygame.sprite'.
    Не является наследником ABC (Abstract Base Class) по причине не ясного мне полиморфного оверхеда.

    Имеет двух наследником, а сам же может использоваться как тестовый вариант, без углубления в абстракции.
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
        self.rect: pygame.Rect = self.texture.get_rect(topleft=(self.centerX + self.radius, self.centerY + self.radius))
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
        pygame.draw.rect(self.window, "white", self.rect, 1)
        self.window.blit(self.texture, (self.centerX + self.radius, self.centerY + self.radius))
        self.rect = self.texture.get_rect(topleft=(self.centerX + self.radius, self.centerY + self.radius))


class BuildConstruction(GameObject):
    """
    #### Прототипированный класс строй-конструкции.

    Строй-конструкция это статический игровой объект, что не обладает способностью к движению.
    Предполагает в себе реализацию двух сторон боевых действий:
    ---
    1. Империалистический.
    2. Говномунистический.\n
    А так же два типа самого сооружения:
    1. Фабричный.
    2. Житейный.
    ---
    """
    side: str = ""
    whattype: str = ""

    def __init__(self, center: tuple[float, float], window: pygame.Surface, side: str, whattype: str, *args: any, **kw: any) -> None:
        """
        Инициализатор класса.
        """
        self.collect_amount: float = 1.0
        self.money_storage: float = 0.0
        self.side = side
        self.whattype = whattype
        self.has_been_selected: bool = False
        self.__f: pygame.font.Font = pygame.font.SysFont("Arial", 22)

        pict: pygame.Surface = None
        if self.side == "imperial":
            if self.whattype == "factory":
                pict = pygame.image.load("assets\Skotoro.png")
            elif self.whattype == "house":
                pict = pygame.image.load("assets\Cituman.png")
        elif self.side == "govnomun":
            if self.whattype == "factory":
                pict = pygame.image.load("assets\Submainfabric.png")
            elif self.whattype == "house":
                pict = pygame.image.load("assets\Mylivehome.png")

        super().__init__(center, (0, 0), 150.0, -1.0, pict, window, *args, **kw)

    def draw(self) -> None:
        """
        Перегруженный метод родительского класса, для отрисовки. Он так же привносит маркерованный текст.
        """
        #(self.window.get_width() - self.centerX // 2, self.window.get_height() - self.centerY // 2) -- весьма неплохое поведение текста.
        if self.side == "govnomun":
            text: str = f"income: {self.collect_amount}/секу."
            to_blit: tuple[float, float] = self.rect.x, self.rect.y - self.rect.h // 2
            pygame.draw.rect(self.window, "darkcyan", [to_blit, self.__f.size(text)], 0)
            self.window.blit(self.__f.render(text, 0, "cyan"), to_blit)
        return super().draw()

    def move(self) -> None:
        """
        Метод переопределяет поведение объекта, дабы тот не мог перемещаться самостоятельно.
        """
        if self.has_been_selected:
            self.centerX, self.centerY = pygame.mouse.get_pos()[0] - self.texture.get_width() * 1.25, pygame.mouse.get_pos()[1]  - self.texture.get_height() * 1.25
    
    def to_project(self, cam_x: float, cam_y: float) -> None:
        """
        Метод для субъективного передвижения объекта, сугубо для учёта координат камеры.
        """
        self.centerX += cam_x
        self.centerY += cam_y

    def collect_to(self, player_wallet: float) -> float:
        """
        Метод что возвращает увеличенное значение вещественно-числового типа.
        """
        if self.whattype == "factory":
            self.money_storage += self.collect_amount / 60
        elif self.whattype == "house":
            self.money_storage += self.collect_amount / 60
        result: float = player_wallet + self.money_storage
        self.money_storage = 0
        return result
    
    def select(self) -> None:
        """
        Метод для избрания постройки.
        """
        if self.side == "govnomun":
            buttons = pygame.mouse.get_pressed()
            if buttons[0]:
                rect_of_mouse: pygame.Rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
                if rect_of_mouse.colliderect(self.rect):
                    self.has_been_selected = True
            elif buttons[2]:
                self.has_been_selected = False
        if self.has_been_selected:
            self.move()


class SelectUnit(GameObject):
    """
    #### Прототипированный класс ручно-выбераемого юнита.

    Подобно строй-конструкциям имеет разновидности своей политической и экономической сторон.

    Но в отличии от зданий, является не статическим, а динамическим игровым объектом.
    """
    side: str = ""

    def __init__(self, center: tuple[float, float], direction: tuple[float, float], window: pygame.Surface, side: str, *args: any, 
                **kw: any) -> None:
        """
        Инициализатор класса.
        """
        self.side = side
        self.health: float = 100.0
        self.__speed_denominator: float = 35.0
        self.preveus_position: list[float, float] = list(center)
        self.__f: pygame.font.Font = pygame.font.SysFont("Arial", 22)

        self.__has_been_selected: bool = False
        self.__has_been_war_selected: bool = False
        self.attacked: bool = False
        self.is_stopped: bool = False
        self.is_destruct: bool = False

        self.explusion_sound: pygame.mixer.Sound = pygame.mixer.Sound(r"assets\roblox-explosion-sound.mp3")
        self.explusion_sound.set_volume(0.3)

        texture: pygame.Surface
        if self.side == "govnomun":
            texture = pygame.image.load("assets\Suprtech.png")
        elif self.side == "imperial":
            texture = pygame.image.load("assets\Tankorog.png")
        super().__init__(center, direction, 50.0, 1.0, texture, window, *args, **kw)

    def destruct(self) -> None:
        """
        Метод удаления объекта.
        """
        self.explusion_sound.play()
        del self

    def draw(self) -> None:
        """
        Перегруженный проверкой на существование родительский метод отрисовки.
        """
        if not self.is_destruct:
            text: str = f"Health: {self.health}"
            to_blit: tuple[int, int] = (self.centerX, self.centerY - self.texture.get_height() // 2)
            pygame.draw.rect(self.window, "darkcyan", [to_blit, self.__f.size(text)], 0)
            self.window.blit(self.__f.render(text, 0, "lightgreen"), to_blit)
            return super().draw()

    def __go_to_place(self, another_tech: "SelectUnit") -> None:
        """
        Метод служит для более точечного и прямолинейного движения к определённой точке.
        """
        if another_tech.centerX < self.centerX and another_tech.centerY > self.centerY:
            self.directionOnX = (another_tech.centerX - self.centerX + another_tech.texture.get_width()) / self.__speed_denominator
            self.directionOnY = (another_tech.centerY - self.centerY - another_tech.texture.get_height()) / self.__speed_denominator

        elif another_tech.centerX > self.centerX and another_tech.centerY > self.centerY:
            self.directionOnX = (another_tech.centerX - self.centerX - another_tech.texture.get_width()) / self.__speed_denominator
            self.directionOnY = (another_tech.centerY - self.centerY - another_tech.texture.get_height()) / self.__speed_denominator

        elif another_tech.centerX > self.centerX and another_tech.centerY < self.centerY:
            self.directionOnX = (another_tech.centerX - self.centerX - another_tech.texture.get_width()) / self.__speed_denominator
            self.directionOnY = (another_tech.centerY - self.centerY + another_tech.texture.get_height()) / self.__speed_denominator

        elif another_tech.centerX < self.centerX and another_tech.centerY < self.centerY:
            self.directionOnX = (another_tech.centerX - self.centerX + another_tech.texture.get_width()) / self.__speed_denominator
            self.directionOnY = (another_tech.centerY - self.centerY + another_tech.texture.get_height()) / self.__speed_denominator

        if int(self.preveus_position[0]) == int(self.centerX) and int(self.preveus_position[1]) == int(self.centerY):
            self.is_stopped = True
        else:
            self.preveus_position = (self.centerX, self.centerY)
        self.move()
            
    def attack(self, another_tech: "SelectUnit") -> None:
        """
        Метод режима включения атаки.
        """
        if self.__has_been_war_selected and another_tech.side == "imperial":
            rect_of_mouse: pygame.Rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
            if rect_of_mouse.colliderect(another_tech.rect):
                self.attacked = True
                another_tech.attacked = True
                self.__has_been_war_selected = False
        if self.attacked:
            self.__go_to_place(another_tech)
            if self.is_stopped:
                another_tech.health -= 0.1
                print(another_tech.health)
            if int(another_tech.health) == 0:
                self.attacked = False
                self.is_stopped = False
                another_tech.is_destruct = True
                another_tech.destruct()
        if int(self.health) == 0:
            self.is_destruct = True
            self.destruct()

    def select(self) -> None:
        """
        Метод для избрания юнита.
        """
        if self.side == "govnomun" and not self.is_destruct:
            buttons = pygame.mouse.get_pressed()
            if buttons[0]:
                rect_of_mouse: pygame.Rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
                if rect_of_mouse.colliderect(self.rect):
                    self.__has_been_selected = True
                    self.__has_been_war_selected = True
            elif buttons[2]:
                self.__has_been_selected = False
            if self.__has_been_selected:
                self.centerX, self.centerY = (
                    pygame.mouse.get_pos()[0] - self.texture.get_width() * 1.25, 
                    pygame.mouse.get_pos()[1]  - self.texture.get_height() * 1.25
                    )


class ObjectsGenerator(object):
    """
    #### Шаблон прототипированного генератора объектов.

    Был рождён для упрощения процесса создания и производства новых объектов.
    """
    tilesize: float = 0.0

    def __init__(self, tilesize: float) -> None:
        """
        Метод для инициализации объекта.
        """
        super().__init__()
        self.tilesize = tilesize

    def generate_build_constructions(self) -> None:
        """
        Метод позволяет сгенерировать построительные конструкции.
        """
        raise NotImplementedError("Метод не реализован, а отложен на небольшой срок!")

    def generate_hand_select_units(self) -> None:
        """
        Метод позволяет сгенерировать ручновыбираемых юнитов.
        """
        raise NotImplementedError("Метод не реализован, а отложен на небольшой срок!")


if __name__ == "__main__":
    screen: pygame.Surface = pygame.display.set_mode((1200, 600))
    clock: pygame.time.Clock = pygame.time.Clock()
    go1 = BuildConstruction((0.0, 0.0), screen, "imperial", "factory")
    go2 = BuildConstruction((600.0, 300.0), screen, "govnomun", "house")
    go3 = BuildConstruction((500.0, 200.0), screen, "govnomun", "house")

    tech1 = SelectUnit((400, 200), (0, 0), screen, "govnomun")
    tech2 = SelectUnit((600, 300), (0, 0), screen, "imperial")
    f: pygame.font.Font = pygame.font.SysFont("Arial", 30)
    money: float = 0.0
    while True:
        screen.fill("black")
        money = go2.collect_to(money)
        money = go3.collect_to(money)
        go1.draw()
        go2.draw()
        go3.draw()
        go2.select()
        go3.select()
        tech1.draw()
        if not tech2.is_destruct:
            tech2.draw()
            tech1.attack(tech2)
        tech1.select()
        screen.blit(f.render(f"M: {money}", 0, "white"), (500, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        else:
            screen.blit(f.render(f"{pygame.time.get_ticks() // 1000}", 0, "white"), (0, 0))
            pygame.display.flip()
            clock.tick(60)
