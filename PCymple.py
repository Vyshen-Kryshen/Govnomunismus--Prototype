"""
Модуль подстать питонячья адаптация сишной DLL.
"""
import ctypes


class Vec2(ctypes.Structure):
    """
    #### Прототипированный класс структуры набора из двух вещественных чисел.
    
    -- f: первый компонент.
    -- s: второй компонент.
    """
    _fields_ = [
        ("f", ctypes.c_float),
        ("s", ctypes.c_float)
    ]

    def __init__(self, first_component: float, second_component, *args: any, **kw: any) -> None:
        """
        Инициализируем данную оболочку над структурой 'typedef struct Vec2'.
        """
        super().__init__(*args, **kw)
        self.our_lib: ctypes.CDLL = ctypes.CDLL(R"C:\Users\TimoshaA - InatiK\Downloads\govnomunismPROTOTYPE\cishnoye\Cymple.dll")
        self.f = ctypes.c_float(first_component)
        self.s = ctypes.c_float(second_component)

    def __str__(self) -> str:
        """
        Метод строкового представления.
        :return: str.
        """
        return "Vec2--%d" % id(self)

    def vecrefl(self, other_item: "Vec2") -> None:
        """
        Метод, что отражает вектор.
        :param other_item: принимает экземпляр того типа (класса), чего и сам объект котору и присущ данный метод.
        :return: None.
        """
        self.our_lib.vecrefl.restype = type(self)
        if isinstance(other_item, type(self)):
            result: self = self.our_lib.vecrefl(self, other_item)
            self.f, self.s = result.f, result.s
        else:
            raise TypeError(f"You have a wrong type of other item: '{type(other_item)}'.But transmitted types is: '{type(self)}'")


def scalar_product(fvec: tuple[float, float], svec: tuple[float, float]) -> float:
    """
    Оболочная функция над сишной - 'float scalarProduct();'.
    :return: вещественное число.
    """
    our_lib: ctypes.CDLL = ctypes.CDLL(R"C:\Users\TimoshaA - InatiK\Downloads\govnomunismPROTOTYPE\cishnoye\Cymple.dll")
    our_lib.scalarProduct.restype = ctypes.c_float
    vecf: Vec2 = Vec2(fvec[0], fvec[1])
    vecs: Vec2 = Vec2(svec[0], svec[1])
    result: ctypes.c_float = our_lib.scalarProduct(vecf, vecs)
    return float(result)


class ColliderCircle(ctypes.Structure):
    """
    #### Прототипированный класс коллизионного круга.
    
    Является оболочкой и связкой пары сишных функций, что были воплощены в методы этого класса,\n
    а так же структуры данных под названием - 'ColliderCircle', в честь которой и был назван сам шаблон.

    По мимо этого тут добавлен дополнительный, высокоуровневый функционал.
    """
    our_lib: ctypes.CDLL
    _field_ = [
        ("centerX", ctypes.c_float),
        ("centerY", ctypes.c_float),
        ("directionOnX", ctypes.c_float),
        ("directionOnY", ctypes.c_float),
        ("radius", ctypes.c_float),
        ("mass", ctypes.c_int),
        ("isCollide", ctypes.c_bool),
    ]

    def __init__(self, center: tuple[float, float], direction: tuple[float, float], radius: float, mass: int,
                 *args: any, **kw: any) -> None:
        """
        Инициализируем объект типа именно здесь.
        :param center: tuple[float, float]
        :param direction: tuple[float, float]
        :param radius: float
        :param mass: int
        :param args: any
        :param kw: any
        """
        super().__init__(*args, **kw)
        self.our_lib: ctypes.CDLL = ctypes.CDLL(R"C:\Users\TimoshaA - InatiK\Downloads\govnomunismPROTOTYPE\cishnoye\Cymple.dll")
        self.centerX = center[0]
        self.centerY = center[1]
        self.directionOnX = direction[0]
        self.directionOnY = direction[1]
        self.radius = radius
        self.mass = mass
        self.isCollide = False

    def __repr__(self) -> str:
        """
        В случае кастинга к стрингу.
        :return: str
        """
        return "ColliderCircle-%d" % id(self)

    def __str__(self) -> str:
        """
        В случае принта воссоздаёт строковое представления объекта здешнего типа.
        :return: str
        """
        return "ColliderCircle-%d" % id(self)

    def __getitem__(self, item: int) -> float | int | bool:
        """
        Метод для поэлементного обращения к атрибутам объекта.
        :param item: int
        :return: float | int | bool
        """
        match item:
            case 0:
                return self.centerX
            case 1:
                return self.centerY
            case 2:
                return self.directionOnX
            case 3:
                return self.directionOnY
            case 4:
                return self.radius
            case 5:
                return self.mass
            case 6:
                return self.isCollide

    def check_collision(self, other_item: str) -> bool:
        """
        Оболочка над сишной функцией проверки на столкновение.
        :param other_item: принимает объект того же типа, только в строковом виде для аннотации.
        :return: bool
        """
        self.our_lib.checkCollision.restype = ctypes.c_bool
        if isinstance(other_item, type(self)):
            subresult: ctypes.c_bool = self.our_lib.checkCollision(ctypes.pointer(self), ctypes.pointer(other_item))
            result: bool = bool(subresult)
            self.isCollide = result
            other_item.isCollide = result
            return result
        else:
            raise TypeError(f"You have a wrong type of other item: '{type(other_item)}'.But transmitted types is: '{type(self)}'")

    def handle_of_collide(self, other_item: str) -> None:
        """
        Оболочка над сишной функцией для обработки столкновения.
        :param other_item: принимает объект того же типа, только в строковом виде для аннотации.
        :return: None
        """
        if isinstance(other_item, type(self)):
            self.our_lib.handleOfCollide(ctypes.pointer(self), ctypes.pointer(other_item))
        else:
            raise TypeError(f"You have a wrong type of other item: '{type(other_item)}'.But transmitted types is: '{type(self)}'")


if __name__ == '__main__':
    first_collider_circle: ColliderCircle = ColliderCircle((0, 0), (-1, -1), 10, 2)
    second_collider_circle: ColliderCircle = ColliderCircle((10, 0), (1, 1), 10, 5)

    result: bool = first_collider_circle.check_collision(second_collider_circle)
    print(result)

    print(second_collider_circle.directionOnX, second_collider_circle.directionOnY)
    first_collider_circle.handle_of_collide(second_collider_circle)
    print(second_collider_circle.directionOnX, second_collider_circle.directionOnY)

    print(scalar_product((0.0, 1.0), (1.5, -9.3)))

    vec1: Vec2 = Vec2(-1.0, -1.0)
    vec2: Vec2 = Vec2(1.0, -1.0)

    print(vec2.f, vec2.s)
    vec2.vecrefl(vec1)
    print(vec2.f, vec2.s)
