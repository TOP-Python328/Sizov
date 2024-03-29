from itertools import pairwise

class Point:
    """
    Класс описывающий двумерную точку
    """
    # ИСПРАВИТЬ: конструктор точки не должен содержать значения по умолчанию
    def __init__(self, x: float, y: float):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x: float):
        raise TypeError(f"'{self.__class__.__name__}' object does not support coordinate assignment")

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, y: float):
        raise TypeError(f"'{self.__class__.__name__}' object does not support coordinate assignment")

    def __repr__(self):
        return f'({self.__x}, {self.__y})'

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__x == other.__x and self.__y == other.__y
        else:
            raise TypeError('')


class Line:
    """
    Класс описывающий отрезок
    """

    def __init__(self, start_point: Point, end_point: Point):
        self.__start = start_point
        self.__end = end_point
        self.__length = self.__length_calc(start_point, end_point)

    @staticmethod
    def __length_calc(point1: Point, point2: Point) -> float:
        """Вычисляет расстояние между двумя точками."""
        delta_x = point2.x - point1.x 
        delta_y = point2.y - point1.y 
        return (delta_x**2 + delta_y**2)**0.5


    @property
    def start(self) -> Point:
        return self.__start

    @start.setter
    # ДОБАВИТЬ: аннотацию типа параметра
    def start(self, new_point: Point):
        if isinstance(new_point, self.start.__class__):
            # КОММЕНТАРИЙ: класс Point по замыслу должен имитировать неизменяемый объект, на это указывают запрещающие сеттеры
            # ИСПРАВИТЬ: замените значение в атрибуте __start текущего экземпляра отрезка, а не пытайтесь изменить координаты уже имеющейся точки
#            self.__start._Point__x = new_point.x
#            self.__start._Point__y = new_point.y
            self.__start = new_point
            self.__length = self.__length_calc(self.start, self.end)
        else:
            raise TypeError(f"'start' attribute of '{self.__class__.__name__}' object supports only '{self.start.__class__.__name__}' object assignment")

    @property
    def end(self) -> Point:
        return self.__end

    @end.setter
    def end(self, new_point: Point):
        if isinstance(new_point, self.end.__class__):
            # ИСПРАВИТЬ: аналогично
#            self.__end._Point__x = new_point.x
#            self.__end._Point__y = new_point.y
            self.__end = new_point
            self.__length = self.__length_calc(self.start, self.end)
        else:
            raise TypeError(f"'end' attribute of '{self.__class__.__name__}' object supports only '{self.end.__class__.__name__}' object assignment")

    @property
    def length(self) -> float:
        return self.__length

    @length.setter
    # УДАЛИТЬ: аннотацию возвращаемого значения — этот метод никогда не сможет вернуть None
    def length(self, new_length: float):
        raise TypeError(f"'{self.__class__.__name__}' object does not support length assignment")

    def __repr__(self):
        # ИСПРАВИТЬ: используйте строковое представление целой точки
#        return f'({self.__start.x}, {self.__start.y})———({self.__end.x}, {self.__end.y})'
        return f'{self.start}———{self.end}'

    def __str__(self):
        return self.__repr__()


class Polygon(list):
    """
    Класс описывающий многоугольник
    """
    def __init__(self, side1: Line, side2: Line, side3: Line, *sides: Line):
        # ИСПОЛЬЗОВАТЬ: переопределение локальной переменной sides:
        sides = side1, side2, side3, * sides
        # ИСПРАВИТЬ: с учётом нового значения sides
        super().__init__([])
        for side in sides:
            super().append(side)

    def _is_closed(self) -> bool:
        """Проверяет, формируют ли отрезки замкнутый многоугольник."""
        # ИСПРАВИТЬ: используйте функцию pairwise() из модуля стандартной библиотеки itertools
#        print(*pairwise(self))
        for i in range(len(self)-1):
            if self[i].end.x != self[i+1].start.x or self[i].end.y != self[i+1].start.y:
                return False
        if self[-1].end.x != self[0].start.x or self[-1].end.y != self[0].start.y:
            return False
        return True

    @property
    def perimeter(self) -> float:
        """Вычисляет периметр многоугольника."""
        if self._is_closed():
            # ИСПРАВИТЬ: используйте встроенную функцию sum()
            perimeter = sum(side.length for side in self)
#            for side in self:
#                perimeter += side.length
            return perimeter
        else:
            raise ValueError("line items doesn't form a closed polygon")



# >>> p1 = Point(0, 3)
# >>> p2 = Point(4, 0)
# >>> p3 = Point(8, 3)
# >>> p1
# (0.0, 3.0)
# >>> repr(p1) == str(p1)
# True
# >>> p1 == Point(0, 3)
# True
# >>> p2 == Point(0, 3)
# False
# >>> p1.x, p1.y
# (0.0, 3.0)
# >>> p2.y = 5
# ...
# TypeError: 'Point' object does not support coordinate assignment
# >>>
# >>> l1 = Line(p1, p2)
# >>> l1
# (0.0, 3.0)———(4.0, 0.0)
# >>> l2 = Line(p2, p3)
# >>> l3 = Line(p3, p1)
# >>> repr(l1) == str(l1)
# True
# >>> l1.length
# 5.0
# >>> l1.length = 10
# ...
# TypeError: 'Line' object does not support length assignment
# >>> l3.start = 12
# ...
# TypeError: 'start' attribute of 'Line' object supports only 'Point' object assignment
# >>> l1.end = p3
# >>> l1
# (0.0, 3.0)———(8.0, 3.0)
# >>> l1.length
# 8.0
# >>>
# >>> Polygon(l1,l2,l3)
# [(0.0, 3.0)———(4.0, 0.0), (4.0, 0.0)———(8.0, 3.0), (8.0, 3.0)———(0.0, 3.0)]
# >>> pol1=Polygon(l1,l2,l3)
# >>> pol1.perimeter
# 18.0
# >>>
# >>> pol1.perimeter = 20
# ...
# AttributeError: property 'perimeter' of 'Polygon' object has no setter
# >>>