"""Path based entities."""
from __future__ import annotations

import math
from typing import Any, Sequence, TypeVar
from weakref import WeakSet

from animator import skia
from animator._common_types import PointLike
from animator.entity.entity import Entity
from animator.entity.text import TextEntity, TextOnPath
from animator.graphics import Context2d

PET = TypeVar('PET', bound='PathEntity')


class PathEntity(Entity):
    """Base class for entities that draw a path. These are the most common types of entities. It automatically rebuilds
    the path when any of the attributes in :attr:`_observed_attrs` change.

    :cvar _observed_attrs: The attributes that trigger a rebuild of the path when they change. This should be overridden
        in subclasses.
    :ivar preserve_stroke: Whether the stroke width should be preserved when scaling the entity.
    :ivar scale_stroke_width: Whether the stroke width should be scaled uniformly when *preserve_stroke* is ``True``.
    """

    _observed_attrs: set[str] = set()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.preserve_stroke: bool = False
        self.scale_stroke_width: bool = False

        self.__path_texts: WeakSet[TextOnPath] = WeakSet()

        self.__path: skia.Path = skia.Path()
        self.__old_attrs: dict[str, Any] = {}
        self.__old_offset: skia.Point = skia.Point(*self.offset)

    @property
    def smooth_stroke(self) -> bool:
        """Whether the strokes should be smoothed when scaling the entity."""
        return self.preserve_stroke and self.scale_stroke_width

    @smooth_stroke.setter
    def smooth_stroke(self, value: bool) -> None:
        self.preserve_stroke = self.scale_stroke_width = value

    @property
    def path(self) -> skia.Path:
        """The internal path."""
        return self.__path

    @property
    def path_length(self) -> float:
        """The length of the path."""
        self.__build_path()
        return skia.PathMeasure(self.__path).getLength()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name in self._observed_attrs and (
            __name not in self.__old_attrs or self.__old_attrs.get(__name) != __value
        ):
            self._is_dirty = True
            self.__old_attrs[__name] = __value

    def add_text_on_path(self, text: str, text_offset: float = 0, **kwargs: Any) -> TextOnPath:
        """
        Add *text* to be drawn along this :class:`PathEntity`. This takes the same arguments as :class:`TextOnPath`
        except path. This method makes sure that the text updates when the path changes.
        """
        text_on_path = TextOnPath(text, self.__path, text_offset, **kwargs)
        self.add(text_on_path)
        self.__path_texts.add(text_on_path)
        return text_on_path

    def on_build_path(self) -> None:
        """Build the path. This method should be overridden."""
        pass

    def __build_path(self) -> None:
        """Build the path if necessary."""
        if self._is_dirty or self.__old_offset != self.offset:
            if self._is_dirty:
                self.__path.rewind()
                self.on_build_path()
                self.__path.offset(*self.offset)
                self._is_dirty = False
            else:  # only offset changed
                self.__path.offset(self.offset.fX - self.__old_offset.fX, self.offset.fY - self.__old_offset.fY)
            self.__old_offset.set(*self.offset)
            for text in self.__path_texts:
                text._is_dirty = True

    @property
    def built_path(self) -> skia.Path:
        """The internal path. This is the same as :attr:`path` except it rebuilds the path if necessary."""
        self.__build_path()
        return self.__path

    def get_svg_path(self, relative: bool = False) -> str:
        """Get the SVG path string.

        :param relative: If ``True``, the returned path will use relative values.
        """
        self.__build_path()
        return skia.ParsePath.ToSVGString(
            self.__path, skia.ParsePath.PathEncoding.Relative if relative else skia.ParsePath.PathEncoding.Absolute
        )

    def transform_path(self: PET, mat: skia.Matrix | None = None) -> PET:
        """Transform the path.

        :param mat: The transformation matrix. If ``None``, the entity's transformation matrix is used and the entity's
            transformation matrix is reset.
        """
        reset = mat is None
        if reset:
            mat = self.mat
        self.__build_path()
        self.__path.transform(mat, skia.ApplyPerspectiveClip.kNo)
        if reset:
            self.mat.reset()
        return self

    def do_stroke(self, canvas: skia.Canvas) -> None:
        """Draw the stroke."""
        if self.preserve_stroke:
            stroke_paint = skia.Paint(self.style.stroke_paint)
            transformation = canvas.getTotalMatrix()
            transformed_path = self.__path.makeTransform(transformation, skia.ApplyPerspectiveClip.kNo)
            if self.scale_stroke_width:
                stroke_paint.setStrokeWidth(transformation.mapRadius(stroke_paint.getStrokeWidth()))
            fill_path, is_fill = transformed_path.fillPathWithPaint(stroke_paint)
            if is_fill:
                transformation.invert(transformation)
                fill_path.transform(transformation, skia.ApplyPerspectiveClip.kNo)
                stroke_paint.setStyle(skia.Paint.Style.kFill_Style)
                canvas.drawPath(fill_path, stroke_paint)
        else:
            canvas.drawPath(self.__path, self.style.stroke_paint)

    def do_fill(self, canvas: skia.Canvas) -> None:
        canvas.drawPath(self.__path, self.style.fill_paint)

    def on_draw(self, canvas: skia.Canvas) -> None:
        self.__build_path()
        super().on_draw(canvas)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        self.__build_path()
        if transformed:
            path = self.__path.makeTransform(self.mat, skia.ApplyPerspectiveClip.kNo)
            return path.computeTightBounds()
        return self.__path.computeTightBounds()


class Path(PathEntity):
    def __init__(self, path: skia.Path | str, **kwargs: Any) -> None:
        """
        :param path: The path. If a string is passed, it is parsed as an SVG path.
        """
        super().__init__(**kwargs)
        self.__svg_path = skia.ParsePath.FromSVGString(path) if isinstance(path, str) else path

    def on_build_path(self) -> None:
        self.path.addPath(self.__svg_path)


class Circle(PathEntity):
    _observed_attrs = {'r'}

    def __init__(self, r: float, **kwargs: Any) -> None:
        """
        :param r: Radius of the circle.
        """
        super().__init__(**kwargs)
        self.r = r

    def on_build_path(self) -> None:
        self.path.addCircle(0, 0, self.r)


class Ellipse(PathEntity):
    _observed_attrs = {'rx', 'ry'}

    def __init__(self, rx: float, ry: float | None = None, **kwargs: Any) -> None:
        """
        :param rx: The radius of the ellipse in the x-direction.
        :param ry: The radius of the ellipse in the y-direction. If ``None``, it'll be same as *rx*.
        """
        super().__init__(**kwargs)
        self.rx = rx
        self.ry = rx if ry is None else ry

    def on_build_path(self) -> None:
        self.path.addOval(skia.Rect.MakeLTRB(-self.rx, -self.ry, self.rx, self.ry))


class Rect(PathEntity):
    _observed_attrs = {'w', 'h'}

    def __init__(self, w: float, h: float | None = None, **kwargs: Any) -> None:
        """
        :param w: Width of the rectangle.
        :param h: Height of the rectangle. If ``None``, it'll be same as *w* and make a square.
        """
        super().__init__(**kwargs)
        self.w = w
        self.h = w if h is None else h

    @classmethod
    def from_ltrb(cls, l: float, t: float, r: float, b: float, **kwargs: Any) -> Rect:
        """Create a rectangle from left, top, right, and bottom coordinates."""
        kwargs.setdefault('pos', (0, 0))
        rect = cls(r - l, b - t, **kwargs)
        rect.offset.set(l, t)
        return rect

    def on_build_path(self) -> None:
        self.path.addRect(0, 0, self.w, self.h)


class RoundRect(PathEntity):
    _observed_attrs = {'w', 'h', 'r'}

    def __init__(self, w: float, h: float | None = None, r: float | tuple[float, ...] = 0, **kwargs: Any) -> None:
        """
        :param w: Width of the rectangle.
        :param h: Height of the rectangle.
        :param r: Radius of the corners in clockwise order starting from the top-left corner. It can be

            * a single number or a tuple with a single number: all corners have the same radius.
            * a tuple with two numbers: x and y radius of the corners.
            * a tuple with four numbers: radius of each corner.
            * a tuple with eight numbers: x and y radius of each corner.
        """
        super().__init__(**kwargs)
        self.w = w
        self.h = w if h is None else h
        self.r = Context2d.parse_RR_radius(r)

    def on_build_path(self) -> None:
        self.path.addRoundRect(skia.Rect.MakeLTRB(0, 0, self.w, self.h), self.r)


class Point(PathEntity):
    def __init__(self, width: float | None = None, **kwargs: Any) -> None:
        """
        :param width: Width of the point. If provided, this will set the stroke width of the style.
        """
        super().__init__(**kwargs)
        if width is not None:
            self.style.stroke_width = width

    def on_build_path(self) -> None:
        self.path.moveTo(0, 0).close()


class PolyLine(PathEntity):
    _observed_attrs = {'points', 'closed'}

    def __init__(self, points: Sequence[PointLike], closed: bool = False, **kwargs: Any) -> None:
        """
        :param points: List of points.
        :param closed: Whether to close the path.
        """
        super().__init__(**kwargs)
        self.points: list[skia.Point] = [skia.Point(*p) for p in points]
        self.closed: bool = closed

    def on_build_path(self) -> None:
        self.path.addPoly(self.points, self.closed)

    @classmethod
    def from_flat(cls, flat: list[float], closed: bool = False, **kwargs: Any) -> PolyLine:
        """Create a polyline from a list of points in the form of ``[x1, y1, x2, y2, ...]``.

        :param flat: List of points in the form of ``[x1, y1, x2, y2, ...]``. If the length is odd, the last value is
            ignored.
        :param closed: Whether to close the path.
        """
        return cls([(flat[i], flat[i + 1]) for i in range(0, len(flat) - 1, 2)], closed, **kwargs)

    @classmethod
    def line(cls, x1: float, y1: float, x2: float, y2: float, **kwargs: Any) -> PolyLine:
        """Create a line from ``(x1, y1)`` to ``(x2, y2)``."""
        return cls([(x1, y1), (x2, y2)], **kwargs)

    @classmethod
    def polygon(cls, n: int, r: float, **kwargs: Any) -> PolyLine:
        """Create a regular polygon with *n* sides and radius *r*."""
        points: list[skia.Point] = []
        for i in range(n):
            theta = i * math.tau / n
            points.append(skia.Point(r * math.cos(theta), r * math.sin(theta)))
        return cls(points, True, **kwargs)

    @classmethod
    def star(cls, n: int, outer_r: float, inner_r: float | None = None, **kwargs: Any) -> PolyLine:
        """Create a regular star with *n* points and outer radius *outer_r* and inner radius *inner_r*."""
        if inner_r is None:
            inner_r = outer_r / 2
        points: list[skia.Point] = []
        for i in range(n):
            theta = i * math.tau / n
            points.append(skia.Point(outer_r * math.cos(theta), outer_r * math.sin(theta)))
            theta += math.tau / (2 * n)
            points.append(skia.Point(inner_r * math.cos(theta), inner_r * math.sin(theta)))
        return cls(points, True, **kwargs)

    def scale_points(self, sx: float, sy: float | None = None) -> PolyLine:
        """Scale the points by *sx* and *sy*. If *sy* is ``None``, it'll be same as *sx*."""
        if sy is None:
            sy = sx
        for i in range(len(self.points)):
            self.points[i].fX *= sx
            self.points[i].fY *= sy
        return self


Line = PolyLine.line
Polygon = PolyLine.polygon
Star = PolyLine.star


class PathText(PathEntity, TextEntity):
    """Text represented by a path. Not much different from :class:`SimpleText` except being a single path."""

    _observed_attrs = {'text'}

    def __init__(self, text: str, **kwargs: Any):
        """
        :param text: The text to display.
        """
        super().__init__(**kwargs)
        self.text: str = text

    def on_build_path(self) -> None:
        self.path.addPath(skia.Path.GetFromText(self.text, 0, 0, self.font_style.font))
