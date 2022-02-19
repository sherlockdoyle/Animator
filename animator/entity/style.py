"""Class and functions to manage the style of an entity."""
from __future__ import annotations

__all__ = 'Style', 'GradientBuilder'

import enum
from typing import TYPE_CHECKING, Literal, Any, Iterable, Tuple, Dict

import numpy

from .. import skia
from ..scene.color import color

if TYPE_CHECKING:
    from .._common_types import Color
    from .entity import Entity

    Inherit = Literal['inherit']

_EMPTY_PAINT = skia.Paint(Alpha=0)


class Style:
    """Styles to use for drawing entities. Every style is bound to an entity.

    If *inherit_style* is ``True``, and any of the attributes are set to ``'inherit'``, the style will inherit the
    value from the parent entity's style. For this to work, a parent entity must be set on the entity. If
    *inherit_style* is ``False``, but any of the attributes are set to ``'inherit'``, it will be set to ``None``.
    """
    inherit_style: bool = True  #: Whether to inherit styles from the parent entity.

    stroke_width: float | Inherit = 4  #: The width of the line (stroke width). ``-1`` means no stroke.
    stroke_cap: skia.Paint.Cap | Inherit = skia.Paint.Cap.kRound_Cap  #: The cap style of the line.
    stroke_join: skia.Paint.Join | Inherit = skia.Paint.Join.kRound_Join  #: The join style for joining lines.
    miter_limit: float | Inherit = 10  #: The miter limit for miter join style.
    fill_color: Color | skia.Shader | Inherit = (0.9686274509803922, 0.7333333333333333, 0, 1)  #: The fill color.
    stroke_color: Color | skia.Shader | Inherit = (0, 0.47058823529411764, 0.8431372549019608, 1)  #: The stroke color.
    fill_opacity: float | Inherit = 1  #: The fill opacity.
    stroke_opacity: float | Inherit = 1  #: The stroke opacity.

    def __init__(self, entity: Entity):
        self._entity: Entity = entity
        self._paint: skia.Paint = skia.Paint(AntiAlias=True)
        self._is_dirty: bool = True

    def __setattr__(self, key: str, value: Any) -> None:
        super().__setattr__(key, value)
        if key in {'stroke_width', 'stroke_cap', 'stroke_join', 'miter_limit'}:
            self._is_dirty = True

    def __getattribute__(self, item: str) -> Any:
        val = super().__getattribute__(item)
        if val == 'inherit_style':
            try:
                return getattr(self._entity._parent.style, item)
            except AttributeError:
                return getattr(Style, item)
        return val

    def inherit_everything(self) -> None:
        """Inherit every attribute from the parent's style."""
        self.inherit_style = True
        self.stroke_width = self.stroke_cap = self.stroke_join = self.miter_limit = self.fill_color \
            = self.stroke_color = self.fill_opacity = self.stroke_opacity = 'inherit'

    def set_color(self, *clr: int | float | Iterable[float] | str | Color | skia.Shader) -> None:
        """Set the fill and stroke colors. If only one color is given, it will be used for both fill and stroke. If
        multiple colors are given, the first one will be used for fill, and the second one for stroke.

        This method can take colors in all the formats supported by :mod:`color`.
        """
        if isinstance(clr[0], tuple):
            clr = clr[0]
        fill_color = clr[0]
        stroke_color = fill_color if len(clr) == 1 else clr[1]

        if fill_color is not None:
            if isinstance(fill_color, skia.Shader):
                self.fill_color = fill_color
            else:
                self.fill_color = color(fill_color)

        if stroke_color is not None:
            if isinstance(stroke_color, skia.Shader):
                self.stroke_color = stroke_color
            else:
                self.stroke_color = color(stroke_color)

    color = property(fset=set_color)

    def set_opacity(self, *op: float) -> None:
        """Set the fill and stroke opacity. If only one opacity is given, it will be used for both fill and stroke.
        If multiple opacities are given, the first one will be used for fill, and the second one for stroke.

        :warning: Setting an opacity between 0 and 1 (exclusive) might cause drastic slow down.
        """
        self.stroke_opacity = op[0]
        self.fill_opacity = self.stroke_opacity if len(op) == 1 else op[1]

    opacity = property(fset=set_opacity)

    def update_paint(self) -> None:
        """Update the paint object with the current style."""
        if self._is_dirty:
            self._paint.setStrokeWidth(self.stroke_width)
            self._paint.setStrokeCap(self.stroke_cap)
            self._paint.setStrokeJoin(self.stroke_join)
            self._paint.setStrokeMiter(self.miter_limit)
            self._is_dirty = False

    def get_paints(self) -> Tuple[skia.Paint, skia.Paint, float]:
        """Get the fill and stroke paints and the opacity as a tuple of (fill paint, stroke paint, opacity). Use
        these to draw as following.

            push layer
            draw with fill paint
            draw with stroke paint
            pop and draw with alpha = opacity
        """
        self.update_paint()
        max_opacity = max(self.fill_opacity, self.stroke_opacity)
        return (getStyledPaint(self._paint, skia.Paint.Style.kFill_Style, self.fill_color,
                               1 if max_opacity == 0 else self.fill_opacity / max_opacity),
                _EMPTY_PAINT if self.stroke_width < 0 else
                getStyledPaint(self._paint, skia.Paint.Style.kStroke_Style, self.stroke_color,
                               1 if max_opacity == 0 else self.stroke_opacity / max_opacity),
                max_opacity)

    def set_from(self, other: Style) -> None:
        """Set the style from another style."""
        self.stroke_width = other.stroke_width
        self.stroke_cap = other.stroke_cap
        self.stroke_join = other.stroke_join
        self.miter_limit = other.miter_limit
        self.fill_color = other.fill_color
        self.stroke_color = other.stroke_color
        self.fill_opacity = other.fill_opacity
        self.stroke_opacity = other.stroke_opacity

        self._paint = skia.Paint(other._paint)
        self._is_dirty = other._is_dirty

    def __copy__(self) -> Style:
        """Return a copy of the style."""
        style: Style = object.__new__(type(self))
        style.set_from(self)
        return style


def getStyledPaint(orig_paint: skia.Paint, style: skia.Paint.Style, color: Color | skia.Shader,
                   opacity: float) -> skia.Paint:
    """Returns a new paint object with the given *style*, *color*, and *opacity* applied to the original
    paint.

    :param orig_paint: The original paint.
    :param style: The new fill or stroke style.
    :param color: The new color.
    :param opacity: The new opacity.
    """
    paint = skia.Paint(orig_paint)
    paint.setStyle(style)
    if not isinstance(color, skia.Shader):
        color = skia.Shaders.Color(skia.Color4f(color))
    paint.setShader(color)
    paint.setAlphaf(opacity)
    return paint


class GradientBuilder:
    """Utility class for building different gradients."""

    class GradientType(enum.Enum):
        """Enum for gradient types."""
        LINEAR = 1
        RADIAL = 2
        CONIC = 3

    type: GradientType
    params: Dict[str, Any]
    color_stops: Dict[float, skia.Color4f]

    def __init__(self):
        self.color_stops = {}

    @classmethod
    def Linear(cls, x0: float, y0: float, x1: float, y1: float) -> GradientBuilder:
        """Create a linear gradient builder. This builds a linear gradient from (*x0*, *y0*) to (*x1*, *y1*).

        :param x0: The x coordinate of the start point.
        :param y0: The y coordinate of the start point.
        :param x1: The x coordinate of the end point.
        :param y1: The y coordinate of the end point.
        """
        gradient = cls()
        gradient.type = cls.GradientType.LINEAR
        gradient.params = {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1}
        return gradient

    @classmethod
    def Radial(cls, x0: float, y0: float, r0: float, x1: float | None = None, y1: float | None = None,
               r1: float | None = None) -> GradientBuilder:
        """Create a radial gradient builder. This builds a radial gradient from a circle centered at (*x0*,
        *y0*) with radius *r0* to a circle centered at (*x1*, *y1*) with radius *r1*. If *x1*, *y1*, and *r1* are not
        specified, the gradient will start at (*x0*, *y0*) and end at the circumference of the circle with radius *r0*.

        :param x0: The x coordinate of the start point.
        :param y0: The y coordinate of the start point.
        :param r0: The radius of the start point.
        :param x1: The x coordinate of the end point.
        :param y1: The y coordinate of the end point.
        :param r1: The radius of the end point.
        """
        gradient = cls()
        gradient.type = cls.GradientType.RADIAL
        if x1 is None:
            x1, y1, r1 = x0, y0, r0
            x0 = y0 = r0 = 0
        gradient.params = {'x0': x0, 'y0': y0, 'r0': r0, 'x1': x1, 'y1': y1, 'r1': r1}
        return gradient

    @classmethod
    def Conic(cls, start_angle: float, x: float, y: float) -> GradientBuilder:
        """Create a conic gradient builder. This builds a conic gradient centered at (*x*, *y*) and rotated to start
        from *start_angle*.

        :param start_angle: The start angle of the gradient.
        :param x: The x coordinate of the center.
        :param y: The y coordinate of the center.
        """
        gradient = cls()
        gradient.type = cls.GradientType.CONIC
        gradient.params = {'start_angle': start_angle, 'x': x, 'y': y}
        return gradient

    def add_color_stop(self, offset: float | Tuple[float, float],
                       clr: int | float | Iterable[float] | str | Color) -> GradientBuilder:
        """Add a color stop to the gradient. Later color stops take precedence over earlier ones.

        Specifying a single offset sets the color at that offset. Specifying a tuple of two offsets sets the color
        between those offsets.

        :param offset: The offset of the color stop. Should be between 0 and 1.
        :param clr: The color of the color stop.
        :return: Itself for chaining.
        """
        color4f = skia.Color4f(color(clr))
        if isinstance(offset, tuple):
            self.color_stops[numpy.nextafter(offset[0], 1, dtype=numpy.float32)] = color4f
            self.color_stops[numpy.nextafter(offset[1], 0, dtype=numpy.float32)] = color4f
        else:
            self.color_stops[offset] = color4f
        return self

    def build(self) -> skia.Shader:
        """Build the gradient."""
        color_offsets = sorted(self.color_stops.keys())
        if color_offsets[0] != 0:
            self.color_stops[0] = self.color_stops[color_offsets[0]]
            color_offsets.insert(0, 0)
        if color_offsets[-1] != 1:
            self.color_stops[1] = self.color_stops[color_offsets[-1]]
            color_offsets.append(1)

        if self.type == self.GradientType.LINEAR:
            return skia.GradientShader.MakeLinear(
                [(self.params['x0'], self.params['y0']), (self.params['x1'], self.params['y1'])],
                [self.color_stops[offset] for offset in color_offsets], color_offsets)

        if self.type == self.GradientType.RADIAL:
            return skia.GradientShader.MakeTwoPointConical((self.params['x0'], self.params['y0']), self.params['r0'],
                                                           (self.params['x1'], self.params['y1']), self.params['r1'],
                                                           [self.color_stops[offset] for offset in color_offsets],
                                                           color_offsets)

        if self.type == self.GradientType.CONIC:
            return skia.GradientShader.MakeSweep(self.params['x'], self.params['y'],
                                                 [self.color_stops[offset] for offset in color_offsets], color_offsets,
                                                 localMatrix=skia.Matrix.RotateDeg(self.params['start_angle']))
