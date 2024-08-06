"""
## ГЛАВНЫЙ МОДУЛЬ. СБОРКА!
"""


import os
import requests
import pygame
from testbuttons import ButtonWithLink, CommonButton
from gameobjects import BuildConstruction, GameObject, SelectUnit, ObjectsGenerator
pygame.init()


class GameChunkSystem(object):
    """
    #### Прототипированный шаблон для системы игровых чанков.

    С помощью него можно создать систему кусочков текстур игрового мира\n
    оптимизируя их.
    """
    window: pygame.Surface
    map_size: int = 0

    def __init__(self, window: pygame.Surface, map_size: int):
        """
        Инить.
        """
        super().__init__()
        self.window = window
        self.map_size = map_size
        self.texture_path: str = "assets/sandstonebg.jpg"

        if not os.path.exists(self.texture_path):
            with open(self.texture_path, "wb") as f:
                response: requests.Response = requests.get("https://txtrs.ru/textures/sandstone/sandstone-5.jpg")
                f.write(response.content)
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, self.window.get_size())
        
        self.chunks: list[pygame.Surface] = []
        self.chunk_coords: list[tuple[int, int]] = []
        self.chunks_rect: list[pygame.Rect] = []

        for x in range(-self.window.get_width() * self.map_size, self.window.get_width() * self.map_size, self.window.get_width()):
            for y in range(-self.window.get_height() * self.map_size, self.window.get_height() * self.map_size, self.window.get_height()):
                self.chunk_coords.append((x, y))
                self.chunks.append(self.texture)

        for i, chunk in enumerate(self.chunks):
            self.chunks_rect.append(chunk.get_rect(topleft=self.chunk_coords[i]))

        self.cam: pygame.Rect = self.window.get_rect(topleft=(0, 0))
    
    def to_draw(self, new_win: pygame.Surface, cam_x: float, cam_y: float) -> None:
        """
        Метод реализует поведение объекта.
        """
        self.window = new_win
        self.cam = self.window.get_rect(topleft=(0, 0))
        
        for i, chunk in enumerate(self.chunks):
            self.chunks_rect[i].x += cam_x
            self.chunks_rect[i].y += cam_y
            self.chunk_coords[i] = (self.chunks_rect[i].x, self.chunks_rect[i].y) 
            self.chunks_rect[i] = chunk.get_rect(topleft=self.chunk_coords[i])

            if self.cam.colliderect(chunk.get_rect(topleft=self.chunk_coords[i])):
                self.window.blit(chunk, self.chunk_coords[i])
                pygame.draw.rect(self.window, "red", self.chunks_rect[i], 1)


class SimulationApplicationPROTOTYPE(object):
    """
    #### Шаблон прототипа.
    
    Приветствую, это самых жирнющий класс, что и является своей сущностью как выходная программа.
    Пояснение за методы я распишу как-нибудь позже, а пока есть это, небольшое и кратенькое описание...
    """

    def __init__(self) -> None:
        """
        Инициализатор всего приложения, один из самых километровых методов во всём проекте.
        """
        super().__init__()
        self.screen: pygame.Surface = pygame.display.set_mode((1425, 750), flags=pygame.RESIZABLE)
        self.display: pygame.Surface = pygame.Surface((self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.CENTER_TEST_OBJECT: pygame.Rect = pygame.Rect(self.screen.get_width() // 2, self.screen.get_height() // 2, 1, 1)
        
        self.zoom: float = 1
        self.depth: int = 0
        self.zoom_stop: bool = False

        self.cam_x: float = 0.0
        self.cam_y: float = 0.0
        self.cam_obj: pygame.Rect = self.display.get_rect(topleft=(0, 0))

        self.true_cam_x: float = self.cam_obj.centerx - self.CENTER_TEST_OBJECT.x / self.zoom
        self.true_cam_y: float = self.cam_obj.centery - self.CENTER_TEST_OBJECT.y / self.zoom

        self.money_value: float = 200.0

        self.sys_obj: GameChunkSystem = GameChunkSystem(self.display, 3)

        self.texture_paths: list[str] = ["assets/menuBG.png", "assets/smile_icon.png", "assets/sandstonebg.jpg"]
        self.set_decor_icon()
        if not os.path.exists(self.texture_paths[0]):
            with open(self.texture_paths[0], "wb") as f:
                response: requests.Response = requests.get("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0taNk6d21PPVNWZKT9TWSbLm3IqDvpQ78SpTGR98-1UYvU-ouZsWYa0OWvMOlndUA380&usqp=CAU")
                f.write(response.content)
        
        self.menu_bg: pygame.Surface = pygame.image.load(self.texture_paths[0])
        self.menu_bg = pygame.transform.scale(self.menu_bg, (350, 350))
        self.menu_bg.set_alpha(120)

        self.menu_buttons: list[CommonButton, ButtonWithLink] = [
            CommonButton(100, 80, (285 * 2, 645)), ButtonWithLink(100, 80, (285 * 2.5, 645))
            ]
        self.buy_buttons: list[CommonButton] = [
            CommonButton(50, 40, (30, 40)), CommonButton(50, 40, (30, 160)), CommonButton(50, 40, (30, 280))
            ]
        self.ui_buttons: list[CommonButton, ButtonWithLink] = [
            CommonButton(75, 60, (self.screen.get_width() - 90, self.screen.get_height() - 60)), 
            ButtonWithLink(75, 60, (self.screen.get_width() - 180, self.screen.get_height() - 60))
        ]

        self.buy_the_first: bool = False
        self.buy_the_second: bool = False
        self.buy_the_third: bool = False

        self.bgha: pygame.Surface = pygame.image.load("assets\photo_2024-07-29_02-40-03.jpg")
        self.bgha = pygame.transform.scale(self.bgha, self.screen.get_size())

        self.ui_font: pygame.font.Font = pygame.font.SysFont("Arial", 22)
        self.base_font: pygame.font.Font = pygame.font.SysFont("Arial", 35)
        self.texts: list[pygame.Surface] = [self.base_font.render("Играть", 0, "white"), self.base_font.render("Сайт", 0, "white")]
        self.texts: list[pygame.Surface] = [self.base_font.render("Выход", 0, "white"), self.base_font.render("Сайт", 0, "white")]
        self.tovar_names: list[str] = ["Фабрика (150)", "Дом жилья (100)", "Танк (50)"]

        self.temp_object: GameObject
        self.game_object_list: list[GameObject] = [
            BuildConstruction((600, 300), self.display, "govnomun", "factory"),
            SelectUnit((400, 500), (1, 0), self.display, "govnomun"),
            SelectUnit((300, 600), (0, 1), self.display, "imperial")
        ]

        self.main_mus: pygame.mixer.Sound = pygame.mixer.Sound("assets/Breaktime.mp3")
        self.gameplay_mus: pygame.mixer.Sound = pygame.mixer.Sound(r"assets\05-06. The Dealer's Shuffle.mp3")
        self.bought_sound: pygame.mixer.Sound = pygame.mixer.Sound(r"assets\victory.mp3")

        self.main_mus.set_volume(0.4)
        self.gameplay_mus.set_volume(0.6)
        self.bought_sound.set_volume(0.5)

    def set_decor_icon(self) -> None:
        """
        Метод, для установки названия и иконки для игры.
        """
        pygame.display.set_caption("prototype-A2")
        if not os.path.exists(self.texture_paths[1]):
            response: requests.Response = requests.get("https://static.wikia.nocookie.net/spore/images/9/9e/Happiness_Booster_Icon.png/revision/latest/thumbnail/width/360/height/450?cb=20100802232515")
            with open(self.texture_paths[1], "wb") as f:
                f.write(response.content)
        game_icon: pygame.Surface = pygame.image.load(self.texture_paths[1])
        pygame.display.set_icon(game_icon)

    def drawui(self) -> None:
        """
        Метод позволяет отрисовать боковою меню магазина и прочий пользовательский интерфейс.
        """
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.draw.rect(self.screen, "white", self.menu_bg.get_rect(topleft=(0, 0)), 1, 1)
        self.screen.blit(self.menu_bg, (0, 0))

        self.true_cam_x: float = self.cam_obj.centerx - self.CENTER_TEST_OBJECT.x / self.zoom
        self.true_cam_y: float = self.cam_obj.centery - self.CENTER_TEST_OBJECT.y / self.zoom

        fps: pygame.Surface = self.ui_font.render(f"FPS--{self.clock.get_fps()}", 0, "white")
        depth: pygame.Surface = self.ui_font.render(f"ZOOM -- {self.depth}", 0, "white")
        money: pygame.Surface = self.ui_font.render(f"MONEY -- {self.money_value.__round__(3)}", 0, "green")
        cam_speed: pygame.Surface = self.ui_font.render(f"CAMSPEED -- {self.cam_x}:::{self.cam_y}", 0, "white")
        cam_coords: pygame.Surface = self.ui_font.render(f"CAMCOORDS -- {self.true_cam_x}:::{self.true_cam_y}", 0, "white")

        pygame.draw.rect(self.screen, "darkcyan", fps.get_rect(topleft=(self.screen.get_width() - 180, 0)), 0)
        pygame.draw.rect(self.screen, "darkcyan", depth.get_rect(topleft=(self.screen.get_width() - 90, 22)), 0)
        pygame.draw.rect(self.screen, "darkcyan", money.get_rect(topleft=(self.screen.get_width() - 150, 44)), 0)
        pygame.draw.rect(self.screen, "darkcyan", cam_speed.get_rect(topleft=(self.screen.get_width() - 180, 66)), 0)
        pygame.draw.rect(self.screen, "darkcyan", cam_coords.get_rect(topleft=(self.screen.get_width() - 250, 88)), 0)

        self.screen.blit(fps, (self.screen.get_width() - 180, 0))
        self.screen.blit(depth, (self.screen.get_width() - 90, 22))
        self.screen.blit(money, (self.screen.get_width() - 150, 44))
        self.screen.blit(cam_speed, (self.screen.get_width() - 180, 66))
        self.screen.blit(cam_coords, (self.screen.get_width() - 250, 88))

        for i, buy_button in enumerate(self.buy_buttons):
            buy_button.draw(self.screen, self.base_font.render(self.tovar_names[i], 0, "white"), "vert")

        for i, ui_button in enumerate(self.ui_buttons):
            ui_button.draw(self.screen, self.texts[i])

    def if_buy(self) -> None:
        """
        Метод для реализации алгоритма покупки товаров из магазины.
        """
        mouse_buttons: tuple[bool, bool, bool] = pygame.mouse.get_pressed()

        if self.buy_buttons[0].has_been_click and not self.buy_the_first:
            if self.money_value - 150 > 0:
                self.bought_sound.play()
                self.money_value -= 150
                self.buy_the_first = True
                self.temp_object = BuildConstruction(pygame.mouse.get_pos(), self.display, "govnomun", "factory")
                self.game_object_list.append(self.temp_object)
        elif self.buy_buttons[1].has_been_click and not self.buy_the_second:
            if self.money_value - 100 > 0:
                self.bought_sound.play()
                self.money_value -= 100
                self.buy_the_second = True
                self.temp_object = BuildConstruction(pygame.mouse.get_pos(), self.display, "govnomun", "house")
                self.game_object_list.append(self.temp_object)
        elif self.buy_buttons[2].has_been_click and not self.buy_the_third:
            if self.money_value - 50 > 0:
                self.bought_sound.play()
                self.money_value -= 50
                self.buy_the_third = True
                self.temp_object = SelectUnit(pygame.mouse.get_pos(), (0, 0), self.display, "govnomun")
                self.game_object_list.append(self.temp_object)
            
        if self.buy_the_first:
            if mouse_buttons[2]:
                self.buy_the_first = False
        elif self.buy_the_second:
            if mouse_buttons[2]:
                self.buy_the_second = False
        elif self.buy_the_third:
            if mouse_buttons[2]:
                self.buy_the_third = False

    def main_but_clicks(self, event: pygame.event.Event) -> None:
        """
        Метод для придачи нажатие и обработки этих событий кнопок списков 'ui_buttons' и 'buy_buttons'.
        :param event: принимает объект типа данных - 'pygame.event.Event'.
        """
        for buy_button in self.buy_buttons:
            buy_button.if_click(event)

        for ui_button in self.ui_buttons:
            ui_button.if_click(event)

            if self.ui_buttons[0].has_been_click:
                pygame.quit()
                break
          
    def control_subsys(self) -> None:
        """
        Метод для вызова ''подсистемы'' считывания клавишных событий зажатия.
        """
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.cam_y += round(2 / self.zoom, 0)
        elif keys[pygame.K_s]:
            self.cam_y -= round(2 / self.zoom, 0)
        if keys[pygame.K_a]:
            self.cam_x += round(2 / self.zoom, 0)
        elif keys[pygame.K_d]:
            self.cam_x -= round(2 / self.zoom, 0)

    def cam_collider(self) -> None:
        """
        Метод для управления коллизией камеры.
        """
        if self.true_cam_y >= 1100 / self.zoom:
            self.cam_y = 0
            if self.cam_y == 0:
                self.cam_y += 5
        elif self.true_cam_y <= -3300 / self.zoom:
            self.cam_y = 0
            if self.cam_y == 0:
                self.cam_y -= 5

        if self.true_cam_x >= 2200 / self.zoom:
            self.cam_x = 0
            if self.cam_x == 0:
                self.cam_x += 5
        elif self.true_cam_x <= -6600 / self.zoom:
            self.cam_x = 0
            if self.cam_x == 0:
                self.cam_x -= 5

    def cam_for_project(self) -> None:
        """
        Метод реализующий камерную проекцию.
        :param rect_array: принимает список из игровых объектов.
        """
        try:
            self.display = pygame.transform.scale(self.display, 
            (self.screen.get_width() // self.zoom, self.screen.get_height() // self.zoom))
        except ZeroDivisionError:
            self.zoom = 0.01

        self.display.fill("black")
        self.sys_obj.to_draw(self.display, self.cam_x, self.cam_y)

        for elem in self.game_object_list:
            elem.window = self.display
            self.cam_obj = self.display.get_rect(topleft=(0, 0))

            if self.cam_obj.colliderect(elem.rect):
                elem.draw()
            elem.rect = elem.texture.get_rect(topleft=(elem.centerX + elem.radius, elem.centerY + elem.radius))

            if isinstance(elem, BuildConstruction):
                elem.to_project(self.cam_x, self.cam_y)
                self.money_value = elem.collect_to(self.money_value)
            else:
                elem.centerX += self.cam_x
                elem.centerY += self.cam_y
                self.game_object_list[1].attack(self.game_object_list[2])

            self.CENTER_TEST_OBJECT.x += self.cam_x
            self.CENTER_TEST_OBJECT.y += self.cam_y
            elem.select()

    def get_projection_coords(self) -> tuple[float, float]:
        """
        Метод возвращаюсь спроектированные относительно мастшаба камеры координаты.
        """
        return pygame.mouse.get_pos()[0] / self.zoom, pygame.mouse.get_pos()[1] / self.zoom

    def test_menu_scene(self) -> None:
        """
        Метод для тестового меню.
        """
        run: bool = True
        blacksurf: pygame.Surface = pygame.Surface(self.screen.get_size())
        i: float = 255
        self.main_mus.play()

        while run:
            self.screen.fill("black")
            self.screen.blit(self.bgha, (0, 0))
            
            for index, menu_button in enumerate(self.menu_buttons):
                menu_button.draw(self.screen, self.texts[index])

                if not isinstance(menu_button, ButtonWithLink):
                    if menu_button.has_been_click:
                        run = False
                        break

            for event in pygame.event.get():
                for menu_button in self.menu_buttons:
                    menu_button.if_click(event)

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
            else:
                if i != 0:
                    blacksurf.set_alpha(i)
                    self.screen.blit(blacksurf, (0, 0))
                    i -= 1

                self.screen.blit(pygame.font.SysFont("Arial", 17).render(f"FPS--{self.clock.get_fps()}", 0, "white"), (0, 0))
                pygame.display.flip()
                self.clock.tick(60.0)
        else:
            self.main_mus.stop()

    def test_run(self) -> None:
        """
        #### Метод главного тестирования и запуска.

        Самый ключевой метод во всём проекте, что является более точечным центром сборки\n
        остальных компонентов всей программы.
        """
        self.test_menu_scene()
        run: bool = True
        blacksurf: pygame.Surface = pygame.Surface(self.screen.get_size())
        i: float = 255
        self.gameplay_mus.play()

        while run:
            self.screen.fill("black")
            self.cam_for_project()
            self.control_subsys()
            self.cam_collider()
            self.if_buy()
            
            for event in pygame.event.get():
                self.main_but_clicks(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_EQUALS:
                        if self.depth < 3:
                            self.zoom *= 1.5
                            self.depth += 1
                    elif event.key == pygame.K_MINUS:
                        if self.depth > -2:
                            self.zoom /= 1.5
                            self.depth -= 1
            else: 
                self.drawui()
                if i != 0:
                    blacksurf.set_alpha(i)
                    self.screen.blit(blacksurf, (0, 0))
                    i -= 1
                pygame.display.flip()
                self.clock.tick(60.0)
        else:
            self.gameplay_mus.stop()


if __name__ == "__main__":
    simapp: SimulationApplicationPROTOTYPE = SimulationApplicationPROTOTYPE()
    simapp.test_run()
