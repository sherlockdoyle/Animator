"""Entities with basic shapes. All these methods returns a :class:`PathEntity`. These methods also takes all the
arguments of the :class:`PathEntity` constructor (*pos*)."""
from __future__ import annotations

__all__ = 'Circle', 'Ellipse', 'Rect', 'Square', 'RoundRect', 'Point', 'PolyLine', 'Line', 'Polygon'

import math
import warnings
from typing import Any, Tuple, TYPE_CHECKING, List

from .entity import PathEntity, Drawer
from .. import skia
from ..scene.Context2d import Context2d

if TYPE_CHECKING:
    from .._common_types import Point as PointType


class Circle(PathEntity):
    class Drawer(Drawer):
        __slots__ = 'r',
        r: float

        def draw(self, path: skia.Path) -> None:
            path.addCircle(0, 0, self.r)

    def __init__(self, r: float, *args: Any, **kwargs: Any):
        """
        :param r: Radius of the circle.
        """
        super().__init__(Circle.Drawer(r=r), *args, **kwargs)


class Ellipse(PathEntity):
    class Drawer(Drawer):
        __slots__ = 'rx', 'ry',
        rx: float
        ry: float

        def draw(self, path: skia.Path) -> None:
            path.addOval(skia.Rect.MakeLTRB(-self.rx, -self.ry, self.rx, self.ry))

    def __init__(self, rx: float, ry: float | None = None, *args: Any, **kwargs: Any):
        """
        :param rx: Horizontal radius of the ellipse.
        :param ry: Vertical radius of the ellipse.
        """
        if ry is None:
            ry = rx
        super().__init__(Ellipse.Drawer(rx=rx, ry=ry), *args, **kwargs)


class Rect(PathEntity):
    class Drawer(Drawer):
        __slots__ = 'w', 'h'
        w: float
        h: float

        def draw(self, path: skia.Path) -> None:
            path.addRect(0, 0, self.w, self.h)

    def __init__(self, w: float, h: float | None = None, *args: Any, **kwargs: Any):
        """
        :param w: Width of the rectangle.
        :param h: Height of the rectangle.
        """
        if h is None:
            h = w
        super().__init__(Rect.Drawer(w=w, h=h), *args, **kwargs)


class Square(PathEntity):
    class Drawer(Drawer):
        __slots__ = 'w'
        w: float

        def draw(self, path: skia.Path) -> None:
            path.addRect(0, 0, self.w, self.w)

    def __init__(self, w: float, *args: Any, **kwargs: Any):
        """
        :param w: Width of the square.
        """
        super().__init__(Square.Drawer(w=w), *args, **kwargs)


class RoundRect(PathEntity):
    class Drawer(Drawer):
        __slots__ = 'w', 'h', 'r'
        w: float
        h: float
        r: Tuple[float, float, float, float, float, float, float, float]

        def draw(self, path: skia.Path) -> None:
            path.addRoundRect(skia.Rect.MakeLTRB(0, 0, self.w, self.h), self.r)

    def __init__(self, w: float, h: float | None = None, r: float | Tuple[float, ...] = 0, *args: Any, **kwargs: Any):
        """
        :param w: Width of the rectangle.
        :param h: Height of the rectangle.
        :param r: Radius of the rounded corners. This is in clockwise direction starting from the top left corner and
            can either be

              * a number or a tuple with a single element: The radius for every corner.
              * a tuple with two elements: The x and y radius for every corner.
              * a tuple with four elements: The radius of each corner.
              * a tuple with eight elements: The x and y radius of each corner.
        """
        if h is None:
            h = w
        super().__init__(RoundRect.Drawer(w=w, h=h, r=Context2d.parse_RR_radius(r)), *args, **kwargs)


class Point(PathEntity):
    class Drawer(Drawer):
        def draw(self, path: skia.Path) -> None:
            path.moveTo(0, 0).close()

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(Point.Drawer(), *args, **kwargs)


class PolyLine(PathEntity):
    class Drawer(Drawer):
        __slots__ = 'points', 'closed'
        points: List[PointType]
        closed: bool

        def draw(self, path: skia.Path) -> None:
            if len(self.points) > 0:
                path.moveTo(self.points[0])
                for i in range(1, len(self.points)):
                    path.lineTo(self.points[i])
                if self.closed:
                    path.close()

    def __init__(self, points: List[PointType], closed: bool = False, *args: Any, **kwargs: Any):
        """
        :param points: List of points.
        :param closed: Whether the path should be closed.
        """
        super().__init__(PolyLine.Drawer(points=points, closed=closed), *args, **kwargs)

    @classmethod
    def from_flat(cls, flat: List[float], closed: bool = False, *args: Any, **kwargs: Any) -> PolyLine:
        """Create a :class:`PolyLine` from a flat list of coordinates.

        :param flat: List of x, y coordinates. Length must be even. If odd, the last coordinate is ignored.
        :param closed: Whether the path should be closed.
        """
        length = len(flat)
        if length & 1:
            warnings.warn('Length of flat list is odd, ignoring last coordinate.')
        return cls([(flat[i], flat[i + 1]) for i in range(0, length - 1, 2)], closed, *args, **kwargs)

    @classmethod
    def Line(cls, x1: float, y1: float, x2: float, y2: float, *args: Any, **kwargs: Any) -> PolyLine:
        """Create a line between two points.

        :param x1: x coordinate of the first point.
        :param y1: y coordinate of the first point.
        :param x2: x coordinate of the second point.
        :param y2: y coordinate of the second point.
        """
        return cls([(x1, y1), (x2, y2)], *args, **kwargs)

    @classmethod
    def Polygon(cls, n: int, r: float, *args: Any, **kwargs: Any) -> PolyLine:
        """Create a *n*-gon with a radius of *r*.

        :param n: Number of sides of the polygon.
        :param r: Radius of the polygon.
        """
        points: List[PointType] = [(r, 0)]
        for i in range(1, n):
            angle = math.tau * i / n
            points.append((r * math.cos(angle), r * math.sin(angle)))
        return cls(points, True, *args, **kwargs)

    def scale_points(self, sx: float, sy: float | None = None) -> PolyLine:
        """Scale the points of the polyline.

        :param sx: Scale factor in x direction.
        :param sy: Scale factor in y direction. If ``None``, the same factor is used for both directions.
        :return: Itself for chaining.
        """
        if sy is None:
            sy = sx
        for i in range(len(self.points)):
            self.drawer.points[i] = (self.drawer.points[i][0] * sx, self.drawer.points[i][1] * sy)
        return self


Line = PolyLine.Line
Polygon = PolyLine.Polygon
