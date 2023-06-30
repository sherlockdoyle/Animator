from __future__ import annotations

from abc import abstractmethod
from typing import Literal

import numpy

from animator import skia
from animator._common_types import ColorLike
from animator.graphics.color import color as parse_color

TileMode = Literal['clamp', 'repeat', 'mirror', 'decal']
_tile_mode: dict[TileMode, skia.TileMode] = {
    'clamp': skia.TileMode.kClamp,
    'repeat': skia.TileMode.kRepeat,
    'mirror': skia.TileMode.kMirror,
    'decal': skia.TileMode.kDecal,
}


class Gradient:
    """Utility class for building different gradients."""

    def __init__(self):
        self.__color_stops: dict[float, skia.Color4f] = {}
        self.__colors: list[skia.Color4f] | None = None
        self._tile_mode: skia.TileMode = skia.TileMode.kClamp

    @classmethod
    def Linear(cls, x0: float, y0: float, x1: float, y1: float, /) -> Gradient:
        """Create a linear gradient from (*x0*, *y0*) to (*x1*, *y1*)."""
        return _Linear(x0, y0, x1, y1)

    @classmethod
    def Radial(
        cls,
        x0: float,
        y0: float,
        r0: float,
        x1: float | None = None,
        y1: float | None = None,
        r1: float | None = None,
        /,
    ) -> Gradient:
        """
        Create a radial gradient from (*x0*, *y0*) with radius *r0* to (*x1*, *y1*) with radius *r1*. If *x1*, *y1*, and
        *r1* is ``None``, the gradient will be a circle.
        """
        if x1 is None:
            return _Radial(x0, y0, r0)
        return _RadialTwoPoint(x0, y0, r0, x1, y1, r1)  # type: ignore y1 and r1 are not None

    @classmethod
    def Conical(cls, x0: float, y0: float, start_angle: float = 0, /) -> Gradient:
        """Create a conical gradient from (*x0*, *y0*) with the given *start_angle* (in degrees)."""
        return _Conical(x0, y0, start_angle)

    def add_colors(self, *colors: ColorLike) -> Gradient:
        """Add *colors* evenly spaced between 0 and 1."""
        self.__colors = [skia.Color4f(parse_color(color)) for color in colors]
        return self

    def add_color_stop(self, offset: float | tuple[float, float], color: ColorLike) -> Gradient:
        """
        Add a color stop at *offset* (between 0 and 1) with the given *color*. If *offset* is a tuple, the color will be
        added between the two points.
        """
        self.__colors = None
        color4f = skia.Color4f(parse_color(color))
        if isinstance(offset, tuple):
            self.__color_stops[numpy.nextafter(offset[0], 1, dtype=numpy.float32)] = color4f
            self.__color_stops[numpy.nextafter(offset[1], 0, dtype=numpy.float32)] = color4f
        else:
            self.__color_stops[offset] = color4f
        return self

    def __setitem__(self, offset: float | tuple[float, float], color: ColorLike) -> None:
        self.add_color_stop(offset, color)

    def _get_color_stops(self) -> tuple[list[float] | None, list[skia.Color4f]]:
        """Get the color stops sorted by offset."""
        if self.__colors is not None:
            return None, self.__colors
        offsets = sorted(self.__color_stops.keys())
        if offsets[0] != 0:
            self.__color_stops[0] = self.__color_stops[offsets[0]]
            offsets.insert(0, 0)
        if offsets[-1] != 1:
            self.__color_stops[1] = self.__color_stops[offsets[-1]]
            offsets.append(1)
        return offsets, [self.__color_stops[offset] for offset in offsets]

    def set_tile_mode(self, mode: skia.TileMode | TileMode) -> Gradient:
        """Set the tile mode."""
        self._tile_mode = _tile_mode[mode] if isinstance(mode, str) else mode
        return self

    @abstractmethod
    def build(self) -> skia.Shader:
        """Build the gradient. Must be implemented by subclasses."""
        pass


class _Linear(Gradient):
    def __init__(self, x0: float, y0: float, x1: float, y1: float, /):
        super().__init__()
        self.__pts = [(x0, y0), (x1, y1)]

    def build(self) -> skia.Shader:
        offsets, colors = self._get_color_stops()
        return skia.GradientShader.MakeLinear(pts=self.__pts, colors=colors, pos=offsets, mode=self._tile_mode)


class _Radial(Gradient):
    def __init__(self, x0: float, y0: float, r0: float, /):
        super().__init__()
        self.__p0 = (x0, y0)
        self.__r0 = r0

    def build(self) -> skia.Shader:
        offsets, colors = self._get_color_stops()
        return skia.GradientShader.MakeRadial(
            center=self.__p0, radius=self.__r0, colors=colors, pos=offsets, mode=self._tile_mode
        )


class _RadialTwoPoint(Gradient):
    def __init__(self, x0: float, y0: float, r0: float, x1: float, y1: float, r1: float, /):
        super().__init__()
        self.__p0 = (x0, y0)
        self.__r0 = r0
        self.__p1 = (x1, y1)
        self.__r1 = r1

    def build(self) -> skia.Shader:
        offsets, colors = self._get_color_stops()
        return skia.GradientShader.MakeTwoPointConical(
            start=self.__p0,
            startRadius=self.__r0,
            end=self.__p1,
            endRadius=self.__r1,
            colors=colors,
            pos=offsets,
            mode=self._tile_mode,
        )


class _Conical(Gradient):
    def __init__(self, x: float, y: float, start_angle: float, /):
        super().__init__()
        self.__cx = x
        self.__cy = y
        self.__start_angle = start_angle

    def build(self) -> skia.Shader:
        offsets, colors = self._get_color_stops()
        return skia.GradientShader.MakeSweep(
            cx=self.__cx,
            cy=self.__cy,
            colors=colors,
            pos=offsets,
            mode=self._tile_mode,
            localMatrix=skia.Matrix.RotateDeg(self.__start_angle),
        )
