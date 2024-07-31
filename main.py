"""
## ГЛАВНЫЙ МОДУЛЬ. СБОРКА!
"""
import requests
import pygame
from testbuttons import ButtonWithLink, CommonButton
from gameobjects import GameObject, BuildConstruction, HandSelectUnit
pygame.init()


class ObjectsGenerator(object):
    """
    #### Шаблон прототипированного генератора объектов.

    Был рождён для упрощения процесса создания и производства новых объектов.
    """

    def __init__(self) -> None:
        """
        Метод для инициализации объекта.
        """
        super().__init__()

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


class SimulationApplicationPROTOTYPE(object):
    """
    #### Шаблон прототипа.
    """

    def __init__(self) -> None:
        """
        Инициализатор.
        """
        super().__init__()
        self.screen: pygame.Surface = pygame.display.set_mode((1425, 750), flags=pygame.RESIZABLE)
        self.display: pygame.Surface = pygame.Surface((self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        
        self.zoom: float = 1
        self.depth: int = 0
        self.zoom_stop: bool = False

        self.cam_x: float = 0.0
        self.cam_y: float = 0.0

        self.set_decor_icon()

        with open("assets/menuBG.png", "wb") as f:
            response: requests.Response = requests.get("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0taNk6d21PPVNWZKT9TWSbLm3IqDvpQ78SpTGR98-1UYvU-ouZsWYa0OWvMOlndUA380&usqp=CAU")
            f.write(response.content)
        
        self.menu_bg: pygame.Surface = pygame.image.load("assets/menuBG.png")
        self.menu_bg = pygame.transform.scale(self.menu_bg, (280, 280))
        self.menu_bg.set_alpha(65)

        self.menu_buttons: list[CommonButton, ButtonWithLink] = [CommonButton(100, 80, (285 * 2, 645)), ButtonWithLink(100, 80, (285 * 2.5, 645))]
        self.buy_buttons: list[CommonButton] = [CommonButton(50, 40, (30, 40)), CommonButton(50, 40, (30, 160))]
        
        self.bgha: pygame.Surface = pygame.image.load("assets\photo_2024-07-29_02-40-03.jpg")
        self.bgha = pygame.transform.scale(self.bgha, self.screen.get_size())

        self.base_font: pygame.font.Font = pygame.font.SysFont("Arial", 35)
        self.texts: list[pygame.Surface] = [self.base_font.render("Играть", 0, "white"), self.base_font.render("Сайт", 0, "white")]

        self.main_mus: pygame.mixer.Sound = pygame.mixer.Sound("assets/Breaktime.mp3")
        self.gameplay_mus: pygame.mixer.Sound = pygame.mixer.Sound(r"assets\05-06. The Dealer's Shuffle.mp3")

        self.main_mus.set_volume(0.1)
        self.gameplay_mus.set_volume(0.6)

    @staticmethod
    def set_decor_icon() -> None:
        """
        Статический метод, для установки названия и иконки для игры.
        """
        pygame.display.set_caption("prototype-A")
        response: requests.Response = requests.get("https://static.wikia.nocookie.net/spore/images/9/9e/Happiness_Booster_Icon.png/revision/latest/thumbnail/width/360/height/450?cb=20100802232515")
        with open("assets/smile_icon.png", "wb") as f:
            f.write(response.content)
        game_icon: pygame.Surface = pygame.image.load("assets/smile_icon.png")
        pygame.display.set_icon(game_icon)

    def draw_shop(self) -> None:
        """
        Метод позволяет отрисовать боковою меню магазина.
        """
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.draw.rect(self.screen, "white", self.menu_bg.get_rect(topleft=(0, 0)), 1, 1)
        self.screen.blit(self.menu_bg, (0, 0))

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
        Метод главного тестирования и запуска.
        """
        self.test_menu_scene()
        run: bool = True
        blacksurf: pygame.Surface = pygame.Surface(self.screen.get_size())
        i: float = 255
        self.gameplay_mus.play()
        my_rect: pygame.Rect = pygame.Rect(600, 300, 100, 100)
        rect_array: list[pygame.Rect] = []

        while run:
            self.screen.fill("black")

            try:
                self.display = pygame.transform.scale(self.display, 
                (self.screen.get_width() // self.zoom, self.screen.get_height() // self.zoom))
            except ZeroDivisionError:
                self.zoom = 0.01
            self.display.fill("black")
            pygame.draw.rect(self.display, "white", my_rect, 0)

            for i in range(len(rect_array)):
                pygame.draw.rect(self.display, "white", rect_array[i], 0)
                rect_array[i].x += self.cam_x
                rect_array[i].y += self.cam_y

            self.draw_shop()

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.cam_y += 1 / self.zoom
            elif keys[pygame.K_s]:
                self.cam_y -= 1 / self.zoom
            if keys[pygame.K_a]:
                self.cam_x += 1 / self.zoom
            elif keys[pygame.K_d]:
                self.cam_x -= 1 / self.zoom
            
            for buy_button in self.buy_buttons:
                buy_button.draw(self.screen)
            else:
                for event in pygame.event.get():
                    for buy_button in self.buy_buttons:
                        buy_button.if_click(event)

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
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        rect_array.append(pygame.Rect(pygame.mouse.get_pos()[0] / self.zoom, pygame.mouse.get_pos()[1] / self.zoom, 50, 50))
                else:
                    if i != 0:
                        blacksurf.set_alpha(i)
                        self.screen.blit(blacksurf, (0, 0))
                        i -= 1
                    
                    self.screen.blit(pygame.font.SysFont("Arial", 17).render(f"FPS--{self.clock.get_fps()}", 0, "white"), (0, 0))
                    self.screen.blit(pygame.font.SysFont("Arial", 17).render(f"ZOOM -- {self.depth}", 0, "white"), (195, 0))

                    pygame.display.flip()
                    self.clock.tick(60.0)
        else:
            self.gameplay_mus.stop()


if __name__ == "__main__":
    simapp: SimulationApplicationPROTOTYPE = SimulationApplicationPROTOTYPE()
    simapp.test_run()
