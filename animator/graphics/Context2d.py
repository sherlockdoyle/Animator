"""**Context2d** adds more drawing functions to the :class:`skia.Canvas`. This is a convenience wrapper around
:class:`skia.Canvas` that adds *HTML CanvasRenderingContext2D* like drawing methods. Most of the *Context2D* methods are
available, although they might behave differently."""
from __future__ import annotations

import math
from contextlib import AbstractContextManager
from typing import IO, Any, Literal, NamedTuple, Sequence, overload

import numpy as np

from animator import skia

Point = tuple[float, float]
Color = skia.Color4f | tuple[float, float, float, float]


class TextMetrics(NamedTuple):
    width: float
    actualBoundingBoxLeft: float
    actualBoundingBoxRight: float
    actualBoundingBoxAscent: float
    actualBoundingBoxDescent: float


CompositeOperation = Literal[
    'source-over',
    'source-in',
    'source-out',
    'source-atop',
    'destination-over',
    'destination-in',
    'destination-out',
    'destination-atop',
    'lighter',
    'copy',
    'xor',
    'multiply',
    'screen',
    'overlay',
    'darken',
    'lighten',
    'color-dodge',
    'color-burn',
    'hard-light',
    'soft-light',
    'difference',
    'exclusion',
    'hue',
    'saturation',
    'color',
    'luminosity',
]
_composite_operation: dict[CompositeOperation, skia.BlendMode] = {
    'source-over': skia.BlendMode.kSrcOver,
    'source-in': skia.BlendMode.kSrcIn,
    'source-out': skia.BlendMode.kSrcOut,
    'source-atop': skia.BlendMode.kSrcATop,
    'destination-over': skia.BlendMode.kDstOver,
    'destination-in': skia.BlendMode.kDstIn,
    'destination-out': skia.BlendMode.kDstOut,
    'destination-atop': skia.BlendMode.kDstATop,
    'lighter': skia.BlendMode.kPlus,
    'copy': skia.BlendMode.kSrc,
    'xor': skia.BlendMode.kXor,
    'multiply': skia.BlendMode.kMultiply,
    'screen': skia.BlendMode.kScreen,
    'overlay': skia.BlendMode.kOverlay,
    'darken': skia.BlendMode.kDarken,
    'lighten': skia.BlendMode.kLighten,
    'color-dodge': skia.BlendMode.kColorDodge,
    'color-burn': skia.BlendMode.kColorBurn,
    'hard-light': skia.BlendMode.kHardLight,
    'soft-light': skia.BlendMode.kSoftLight,
    'difference': skia.BlendMode.kDifference,
    'exclusion': skia.BlendMode.kExclusion,
    'hue': skia.BlendMode.kHue,
    'saturation': skia.BlendMode.kSaturation,
    'color': skia.BlendMode.kColor,
    'luminosity': skia.BlendMode.kLuminosity,
}
_composite_operation_inverse: dict[skia.BlendMode, CompositeOperation] = {v: k for k, v in _composite_operation.items()}


def create_styled_paint(orig_paint: skia.Paint, style: skia.Paint.Style, color: Color | skia.Shader) -> skia.Paint:
    """Returns a new paint object with the given *color* and *style* and the same properties as the original paint.

    :param orig_paint: The original paint.
    :param color: The new color.
    :param style: The new fill or stroke style.
    """
    paint = skia.Paint(orig_paint)
    if not isinstance(color, skia.Shader):
        color = skia.Shader.Color(skia.Color4f(color))
    paint.setShader(color)
    paint.setStyle(style)
    return paint


def calculate_sweep_angle(start_angle: float, end_angle: float, counterclockwise: bool) -> float:
    """Calculates the sweep angle for a given *start_angle* and *end_angle*, in degrees and *counterclockwise* flag."""
    sweep_angle = end_angle - start_angle
    if abs(sweep_angle) >= 360:
        return -359.999969482421875 if counterclockwise else 359.999969482421875
    else:
        sweep_angle %= 360
        if counterclockwise:
            sweep_angle -= 360
        return sweep_angle


class Context2d(AbstractContextManager):
    """*Context2d* provides additional functionality on top of the :class:`skia.Canvas` class."""

    LINE_CAP_SQUARE = skia.Paint.Cap.kSquare_Cap
    LINE_CAP_ROUND = skia.Paint.Cap.kRound_Cap
    LINE_CAP_BUTT = skia.Paint.Cap.kButt_Cap

    LINE_JOIN_BEVEL = skia.Paint.Join.kBevel_Join
    LINE_JOIN_ROUND = skia.Paint.Join.kRound_Join
    LINE_JOIN_MITER = skia.Paint.Join.kMiter_Join

    def __init__(self, canvas: skia.Canvas):
        """Initializes the :class:`Context2d` with a ``skia`` *canvas*.

        :param canvas: The `skia.Canvas` to wrap around.
        """
        self.fillStyle: Color | skia.Shader = (1, 1, 1, 1)
        self.strokeStyle: Color | skia.Shader = (0, 0, 0, 1)

        self._canvas: skia.Canvas = canvas
        self._path: skia.Path = skia.Path()
        self._paint: skia.Paint = skia.Paint(antiAlias=True)
        self._font: skia.Font = skia.Font()

        self.__paths: list[skia.Path] = []

    def clearRect(self, x: float, y: float, width: float, height: float) -> None:
        """Sets the rectangular area from (*x*, *y*) with *width* and *height* to transparent black.

        :param x: The x coordinate of the rectangle.
        :param y: The y coordinate of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        """
        paint = skia.Paint(blendMode=skia.BlendMode.kClear)
        self._canvas.drawRect(skia.Rect.MakeXYWH(x, y, width, height), paint)

    def fillRect(self, x: float, y: float, width: float, height: float) -> None:
        """Draws a rectangle from (*x*, *y*) with *width* and *height* that is filled.

        :param x: The x coordinate of the rectangle.
        :param y: The y coordinate of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        """
        self._canvas.drawRect(
            skia.Rect.MakeXYWH(x, y, width, height),
            create_styled_paint(self._paint, skia.Paint.Style.kFill_Style, self.fillStyle),
        )

    def strokeRect(self, x: float, y: float, width: float, height: float) -> None:
        """Draws a rectangle from (*x*, *y*) with *width* and *height* that is stroked (outlined).

        :param x: The x coordinate of the rectangle.
        :param y: The y coordinate of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        """
        self._canvas.drawRect(
            skia.Rect.MakeXYWH(x, y, width, height),
            create_styled_paint(self._paint, skia.Paint.Style.kStroke_Style, self.strokeStyle),
        )

    def fillText(self, text: str, x: float, y: float) -> None:
        """Draws a filled *text* at (x, y).

        :param text: The text to draw.
        :param x: The x coordinate of the text.
        :param y: The y coordinate of the text.
        """
        self._canvas.drawString(
            text, x, y, self._font, create_styled_paint(self._paint, skia.Paint.Style.kFill_Style, self.fillStyle)
        )

    def strokeText(self, text: str, x: float, y: float) -> None:
        """Draws a stroked *text* at (x, y).

        :param text: The text to draw.
        :param x: The x coordinate of the text.
        :param y: The y coordinate of the text.
        """
        self._canvas.drawString(
            text, x, y, self._font, create_styled_paint(self._paint, skia.Paint.Style.kStroke_Style, self.strokeStyle)
        )

    def measureText(self, text: str) -> TextMetrics:
        """Measures the *text* and returns information like width, etc.

        :param text: The text to measure.
        :return: A :class:`TextMetrics` object with information about the text.
        """
        width, bound = self._font.measureText(text, paint=self._paint)
        return TextMetrics(width, bound.left(), bound.right(), bound.top(), bound.bottom())

    @property
    def lineWidth(self) -> float:
        """Line width used for stroking."""
        return self._paint.getStrokeWidth()

    @lineWidth.setter
    def lineWidth(self, width: float) -> None:
        self._paint.setStrokeWidth(width)

    @property
    def lineCap(self) -> skia.Paint.Cap:
        """Line cap used for stroking."""
        return self._paint.getStrokeCap()

    @lineCap.setter
    def lineCap(self, cap: skia.Paint.Cap) -> None:
        self._paint.setStrokeCap(cap)

    @property
    def lineJoin(self) -> skia.Paint.Join:
        """Line join used for stroking."""
        return self._paint.getStrokeJoin()

    @lineJoin.setter
    def lineJoin(self, join: skia.Paint.Join) -> None:
        self._paint.setStrokeJoin(join)

    @property
    def miterLimit(self) -> float:
        """Miter limit for miter join."""
        return self._paint.getStrokeMiter()

    @miterLimit.setter
    def miterLimit(self, limit: float) -> None:
        self._paint.setStrokeMiter(limit)

    def getLineDash(self) -> list[float]:
        """Returns the line dash pattern used when stroking lines."""
        return self._paint.getPathEffect().asADash().fIntervals

    def setLineDash(self, segments: list[float] | None, offset: float = 0) -> None:
        """Sets the line dash pattern and offset used when stroking lines. Pass empty list or ``None`` to remove the set
        line dash."""
        if not segments:
            self._paint.setPathEffect(None)
        else:
            if len(segments) & 1:
                segments += segments
            self._paint.setPathEffect(skia.DashPathEffect.Make(segments, offset))

    @property
    def lineDashOffset(self) -> float:
        """Offset for the line dash pattern."""
        return self._paint.getPathEffect().asADash().fPhase

    @lineDashOffset.setter
    def lineDashOffset(self, offset: float) -> None:
        self._paint.setPathEffect(skia.DashPathEffect.Make(self._paint.getPathEffect().asADash().fIntervals, offset))

    @property
    def font(self) -> str:
        """The current set font, in <[[style-weight ]size'px' ]family> format."""
        parts: list[str] = []
        typeface: skia.Typeface = self._font.getTypefaceOrDefault()
        if typeface.isItalic():
            parts.append('italic')
        if typeface.isBold():
            parts.append('bold')
        parts.append(f'{self._font.getSize():g}px')
        parts.append(f'"{typeface.getFamilyName()}"')
        return ' '.join(parts)

    @font.setter
    def font(self, font: str) -> None:
        parts = font.lower().split()
        l = len(parts)
        style_weight, size, family = [], None, None
        if l == 1:  # family
            family = parts[0]
        elif l == 2:  # size family
            size, family = parts
        else:  # style-weight size family
            *style_weight, size, family = parts

        style = skia.FontStyle.Normal()
        if style_weight:
            if 'bold' in style_weight:
                if 'italic' in style_weight:
                    style = skia.FontStyle.BoldItalic()
                else:
                    style = skia.FontStyle.Bold()
            elif 'italic' in style_weight:
                style = skia.FontStyle.Italic()
        self._font.setTypeface(skia.Typeface(family, style))
        if size is not None:
            if size.endswith('px'):
                size = size[:-2]
            self._font.setSize(float(size))

    @staticmethod
    def createConicGradient(
        start_angle: float, x: float, y: float, colors: list[Color], pos: list[float] | None = None
    ) -> skia.Shader:
        """Creates a conical gradient around (*x*, *y*) starting from *start_angle* in radians.

        :param start_angle: The start angle in radians.
        :param x: The x coordinate of the center of the gradient.
        :param y: The y coordinate of the center of the gradient.
        :param colors: The colors of the gradient.
        :param pos: The position of the colors in the gradient.
        :return: A :class:`skia.Shader` object representing the conical gradient.
        """
        return skia.GradientShader.MakeSweep(
            x, y, list(map(lambda c: skia.Color4f(c), colors)), pos, localMatrix=skia.Matrix.RotateRad(start_angle)
        )

    @staticmethod
    def createLinearGradient(
        x0: float, y0: float, x1: float, y1: float, colors: list[Color], pos: list[float] | None = None
    ) -> skia.Shader:
        """Creates a linear gradient along the line joining (*x0*, *y0*) to (*x1*, *y1*).

        :param x0: The x coordinate of the start of the gradient.
        :param y0: The y coordinate of the start of the gradient.
        :param x1: The x coordinate of the end of the gradient.
        :param y1: The y coordinate of the end of the gradient.
        :param colors: The colors of the gradient.
        :param pos: The position of the colors in the gradient.
        :return: A :class:`skia.Shader` object representing the linear gradient.
        """
        return skia.GradientShader.MakeLinear([(x0, y0), (x1, y1)], list(map(lambda c: skia.Color4f(c), colors)), pos)

    @staticmethod
    def createRadialGradient(
        x0: float,
        y0: float,
        r0: float,
        x1: float,
        y1: float,
        r1: float,
        colors: list[Color],
        pos: list[float] | None = None,
    ) -> skia.Shader:
        """Creates a radial gradient using the radius and coordinates of two circles.

        :param x0: The x coordinate of the center of the inner circle.
        :param y0: The y coordinate of the center of the inner circle.
        :param r0: The radius of the inner circle.
        :param x1: The x coordinate of the center of the outer circle.
        :param y1: The y coordinate of the center of the outer circle.
        :param r1: The radius of the outer circle.
        :param colors: The colors of the gradient.
        :param pos: The position of the colors in the gradient.
        :return: A :class:`skia.Shader` object representing the radial gradient.
        """
        return skia.GradientShader.MakeTwoPointConical(
            (x0, y0), r0, (x1, y1), r1, list(map(lambda c: skia.Color4f(c), colors)), pos
        )

    @staticmethod
    def createPattern(
        image: str | IO[bytes] | skia.Image,
        repetition: Literal['repeat', 'repeat-x', 'repeat-y', 'no-repeat'] = 'repeat',
    ) -> skia.Shader:
        """Creates a pattern using the *image* or path to the image.

        :param image: The image to use as a pattern.
        :param repetition: The repetition of the pattern. Should be one of ``'repeat'``, ``'repeat-x'``, ``'repeat-y'``,
            or ``'no-repeat'``.
        :return: A :class:`skia.Shader` object representing the pattern.
        """
        if not isinstance(image, skia.Image):
            image = skia.Image.open(image)
        tmx = skia.TileMode.kRepeat if repetition in {'repeat', 'repeat-x'} else skia.TileMode.kDecal
        tmy = skia.TileMode.kRepeat if repetition in {'repeat', 'repeat-y'} else skia.TileMode.kDecal
        return image.makeShader(tmx, tmy)

    def beginPath(self) -> None:
        """Starts a new path by emptying the current path."""
        self._path.rewind()

    def closePath(self) -> None:
        """Closes the current path."""
        self._path.close()

    def moveTo(self, x: float, y: float) -> None:
        """Starts a new path at (x, y).

        :param x: The x coordinate of the new path.
        :param y: The y coordinate of the new path.
        """
        self._path.moveTo(x, y)

    def lineTo(self, x: float, y: float) -> None:
        """Adds a straight line to the current path by connecting the last point to (x, y).

        :param x: The x coordinate of the new path.
        :param y: The y coordinate of the new path.
        """
        self._path.lineTo(x, y)

    def bezierCurveTo(self, cp1x: float, cp1y: float, cp2x: float, cp2y: float, x: float, y: float) -> None:
        """Adds a cubic bezier curve to the current path.

        :param cp1x: The x coordinate of the first control point.
        :param cp1y: The y coordinate of the first control point.
        :param cp2x: The x coordinate of the second control point.
        :param cp2y: The y coordinate of the second control point.
        :param x: The x coordinate of the end of the curve.
        :param y: The y coordinate of the end of the curve.
        """
        self._path.cubicTo(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadraticCurveTo(self, cpx: float, cpy: float, x: float, y: float) -> None:
        """Adds a quadratic bezier curve to the current path.

        :param cpx: The x coordinate of the control point.
        :param cpy: The y coordinate of the control point.
        :param x: The x coordinate of the end of the curve.
        :param y: The y coordinate of the end of the curve.
        """
        self._path.quadTo(cpx, cpy, x, y)

    def arc(
        self,
        x: float,
        y: float,
        r: float,
        start_angle: float = 0,
        end_angle: float = 2 * math.pi,
        counterclockwise: bool = False,
        move_to: bool = False,
    ) -> None:
        """Creates a circular arc centered at (x, y) with radius *r*. The path starts at start_angle and ends
        at end_angle. Pass only the first 3 arguments to draw a complete circle.

        :param x: The x-axis (horizontal) coordinate of the arc's center.
        :param y: The y-axis (vertical) coordinate of the arc's center.
        :param r: The arc's radius.
        :param start_angle: The angle at which the arc starts, measured clockwise from the positive x-axis and
            expressed in radians.
        :param end_angle: The angle at which the arc ends, measured clockwise from the positive x-axis and expressed
            in radians.
        :param counterclockwise: If ``True``, draws the ellipse anticlockwise (counter-clockwise).
        :param move_to: If ``True``, moves the starting point on the ellipse. This removes the line joining the current
            point to the start of the ellipse.
        """
        start_angle = math.degrees(start_angle)
        self._path.arcTo(
            skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r),
            start_angle % 360,
            calculate_sweep_angle(start_angle, math.degrees(end_angle), counterclockwise),
            move_to,
        )

    def arcTo(self, x1: float, y1: float, x2: float, y2: float, r: float) -> None:
        """Creates a circular arc to the current path, using the given control points and radius *r*.

        :param x1: The x-axis coordinate of the first control point.
        :param y1: The y-axis coordinate of the first control point.
        :param x2: The x-axis coordinate of the second control point.
        :param y2: The y-axis coordinate of the second control point.
        :param r: The arc's radius.
        """
        self._path.arcTo(x1, y1, x2, y2, r)

    def ellipse(
        self,
        x: float,
        y: float,
        rx: float,
        ry: float | None = None,
        rotation: float = 0,
        start_angle: float = 0,
        end_angle: float = 2 * math.pi,
        counterclockwise: bool = False,
        move_to: bool = False,
    ) -> None:
        """Creates an elliptical arc centered at (x, y) with the radii rx and ry. The path starts at start_angle and
        ends at end_angle. Pass only the first 3 or 4 arguments to draw a complete ellipse.

        :param x: The x-axis (horizontal) coordinate of the ellipse's center.
        :param y: The y-axis (vertical) coordinate of the ellipse's center.
        :param rx: The ellipse's major-axis radius.
        :param ry: The ellipse's minor-axis radius. If omitted, rx is used.
        :param rotation: The rotation of the ellipse, expressed in radians.
        :param start_angle: The angle at which the ellipse starts, measured clockwise from the positive x-axis and
            expressed in radians.
        :param end_angle: The angle at which the ellipse ends, measured clockwise from the positive x-axis and expressed
            in radians.
        :param counterclockwise: If true, draws the ellipse anticlockwise (counter-clockwise).
        :param move_to: If ``True``, moves the starting point on the ellipse. This removes the line joining the current
            point to the start of the ellipse.
        """
        if ry is None:
            ry = rx
        start_angle = math.degrees(start_angle)

        path = skia.Path()
        if rx == 0 and ry == 0:
            if not move_to:
                path.lineTo(x, y)
        else:
            if rx == 0:
                rx = 0.0001  # add a small radius to draw a line for 0 radius
            elif ry == 0:
                ry = 0.0001
            path.addArc(
                skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry),
                start_angle % 360,
                calculate_sweep_angle(start_angle, math.degrees(end_angle), counterclockwise),
            )
        self._path.addPath(
            path,
            skia.Matrix.RotateDeg(math.degrees(rotation), (x, y)),
            skia.Path.AddPathMode.kAppend_AddPathMode if move_to else skia.Path.AddPathMode.kExtend_AddPathMode,
        )

    def rect(self, x: float, y: float, width: float, height: float) -> None:
        """Draws a rectangle from (x, y) with *width* and *height*.

        :param x: The x-axis coordinate of the rectangle's top-left corner.
        :param y: The y-axis coordinate of the rectangle's top-left corner.
        :param width: The rectangle's width.
        :param height: The rectangle's height.
        """
        self._path.addRect(x, y, x + width, y + height)

    def fill(self, clear_path: bool = False) -> None:
        """Fills the current path.

        :param clear_path: If *True*, the current path is cleared after filling.
        """
        self._canvas.drawPath(
            self._path, create_styled_paint(self._paint, skia.Paint.Style.kFill_Style, self.fillStyle)
        )
        if clear_path:
            self._path.rewind()

    def stroke(self, clear_path: bool = False) -> None:
        """Strokes the current path.

        :param clear_path: If *True*, the current path is cleared after stroking.
        """
        self._canvas.drawPath(
            self._path, create_styled_paint(self._paint, skia.Paint.Style.kStroke_Style, self.strokeStyle)
        )
        if clear_path:
            self._path.rewind()

    def fill_stroke(self, clear_path: bool = True) -> None:
        """Convenience method to first fill then stroke the current path.

        :param clear_path: If *True*, the current path is cleared from the context after filling and stroking. **Note**
            that the default argument is *True*; this is so cause :meth:`fill_stroke` is supposed to be the most used
            method which will be followed by a clearing of the path.
        """
        self.fill(False)
        self.stroke(clear_path)

    def stroke_fill(self, clear_path: bool = False) -> None:
        """Convenience method to first stroke then fill the current path. This modifies the context's source.

        :param clear_path: If *True*, the current path is cleared from the context after stroking and filling.
        """
        self.stroke(False)
        self.fill(clear_path)

    def clip(self, path: skia.Path | None = None, fill_rule: Literal['nonzero', 'evenodd'] = 'nonzero') -> None:
        """Turns the current or given *path* into the current clipping region.

        :param path: The path to clip. If ``None``, the current path is used.
        :param fill_rule: The fill rule to use when clipping. Should be either ``'nonzero'`` or ``'evenodd'``.
        """
        if path is None:
            path = skia.Path(self._path)
        path.setFillType(skia.PathFillType.kEvenOdd if fill_rule == 'evenodd' else skia.PathFillType.kWinding)
        self._canvas.clipPath(path, doAntiAlias=True)

    def isPointInPath(self, x: float, y: float) -> bool:
        """Returns ``True`` if the point (x, y) is in the current path when filled.

        :param x: The x-axis coordinate of the point.
        :param y: The y-axis coordinate of the point.
        :return: ``True`` if the point is in the current path when filled.
        """
        return self._path.contains(x, y)

    def get_fill_for_stroke(self) -> skia.Path:
        """Returns a path, which when filled, will look like the current path stroked."""
        paint = skia.Paint(self._paint)
        paint.setStyle(skia.Paint.Style.kStroke_Style)
        fill_path, _ = self._path.fillPathWithPaint(paint)
        return fill_path

    def isPointInStroke(self, x: float, y: float) -> bool:
        """Returns if the point (x, y) is in the current path when stroked.

        :param x: The x-axis coordinate of the point.
        :param y: The y-axis coordinate of the point.
        :return: ``True`` if the point is in the current path when stroked.
        """
        return self.get_fill_for_stroke().contains(x, y)

    def getTransform(self) -> skia.Matrix:
        """Returns the current transformation matrix."""
        return self._canvas.getTotalMatrix()

    def rotate(self, angle: float) -> None:
        """Rotates the current transformation matrix by *angle* radians.

        :param angle: The angle to rotate by.
        """
        self._canvas.rotate(math.degrees(angle))

    def scale(self, sx: float, sy: float | None = None) -> None:
        """Scales the current transformation matrix by *sx*, *sy*. *sy* defaults to *sx*.

        :param sx: The x-axis scaling factor.
        :param sy: The y-axis scaling factor.
        """
        if sy is None:
            sy = sx
        self._canvas.scale(sx, sy)

    def translate(self, tx: float, ty: float) -> None:
        """Translates the current transformation matrix by *tx*, *ty*.

        :param tx: The x-axis translation.
        :param ty: The y-axis translation.
        """
        self._canvas.translate(tx, ty)

    def transform(self, a: float, b: float, c: float, d: float, e: float, f: float) -> None:
        """Applies the given transformation matrix to the current transformation matrix.

        :param a: Horizontal scaling.
        :param b: Vertical shearing.
        :param c: Horizontal skewing.
        :param d: Vertical scaling.
        :param e: Horizontal translation.
        :param f: Vertical translation.
        """
        self._canvas.concat(skia.Matrix.MakeAll(a, c, e, b, d, f, 0, 0, 1))

    @overload
    def setTransform(self, a: float, b: float, c: float, d: float, e: float, f: float) -> None:
        """Sets the current transformation matrix to the given matrix.

        :param a: Horizontal scaling.
        :param b: Vertical shearing.
        :param c: Horizontal skewing.
        :param d: Vertical scaling.
        :param e: Horizontal translation.
        :param f: Vertical translation.
        """

    @overload
    def setTransform(self, m: skia.Matrix) -> None:
        """Sets the current transformation matrix to *m*.

        :param m: The matrix to set.
        """

    def setTransform(
        self,
        a: skia.Matrix | float,
        b: float | None = None,
        c: float | None = None,
        d: float | None = None,
        e: float | None = None,
        f: float | None = None,
    ) -> None:
        if isinstance(a, skia.Matrix):
            self._canvas.setMatrix(a)
        else:
            self._canvas.setMatrix(skia.Matrix.MakeAll(a, c, e, b, d, f, 0, 0, 1))

    def resetTransform(self) -> None:
        """Resets the current transformation matrix to the identity matrix."""
        self._canvas.resetMatrix()

    @property
    def globalAlpha(self) -> float:
        """Alpha value to use for drawing."""
        return self._paint.getAlphaf()

    @globalAlpha.setter
    def globalAlpha(self, alpha: float) -> None:
        self._paint.setAlphaf(alpha)

    @property
    def globalCompositeOperation(self) -> CompositeOperation | None:
        """Composite operation to use for drawing."""
        blend_mode = self._paint.asBlendMode()
        if blend_mode is None:
            return None
        return _composite_operation_inverse[blend_mode]

    @globalCompositeOperation.setter
    def globalCompositeOperation(self, operation: CompositeOperation) -> None:
        self._paint.setBlendMode(_composite_operation[operation])

    @overload
    def drawImage(self, img: str | IO[bytes] | skia.Image, x: float, y: float) -> None:
        """Draws an image at (*x*, *y*).

        :param img: The filepath, a file like object or a ``skia.Image`` representing the image.
        :param x: The x-axis coordinate to draw the image at.
        :param y: The y-axis coordinate to draw the image at.
        """

    @overload
    def drawImage(self, img: str | IO[bytes] | skia.Image, x: float, y: float, width: float, height: float) -> None:
        """Draws an image at (*x*, *y*) with the given *width* and *height*.

        :param img: The filepath, a file like object or a ``skia.Image`` representing the image.
        :param x: The x-axis coordinate to draw the image at.
        :param y: The y-axis coordinate to draw the image at.
        :param width: The width of the image to draw.
        :param height: The height of the image to draw.
        """

    @overload
    def drawImage(
        self,
        img: str | IO[bytes] | skia.Image,
        sx: float,
        sy: float,
        sw: float,
        sh: float,
        dx: float,
        dy: float,
        dw: float,
        dh: float,
    ) -> None:
        """Draws a part of an image from (*sx*, *sy*) with width *sw* and height *sh* at (*dx*, *dy*) with the given
        width *dw* and height *dh*.

        :param img: The filepath, a file like object or a ``skia.Image`` representing the image.
        :param sx: The x-axis coordinate of the source image to draw.
        :param sy: The y-axis coordinate of the source image to draw.
        :param sw: The width of the source image to draw.
        :param sh: The height of the source image to draw.
        :param dx: The x-axis coordinate to draw the image at.
        :param dy: The y-axis coordinate to draw the image at.
        :param dw: The width of the image to draw.
        :param dh: The height of the image to draw.
        """

    def drawImage(
        self,
        img: str | IO[bytes] | skia.Image,
        sx: float = 0,
        sy: float = 0,
        sw: float | None = None,
        sh: float | None = None,
        dx: float | None = None,
        dy: float | None = None,
        dw: float | None = None,
        dh: float | None = None,
    ) -> None:
        if not isinstance(img, skia.Image):
            img = skia.Image.open(img)
        if sw is None:  # drawImage(img, x, y)
            self._canvas.drawImage(img, sx, sy, paint=self._paint)
        elif dx is None:  # drawImage(img, x, y, width, height)
            self._canvas.drawImageRect(img, skia.Rect.MakeXYWH(sx, sy, sw, sh), paint=self._paint)
        else:  # drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh)
            self._canvas.drawImageRect(
                img, src=skia.Rect.MakeXYWH(sx, sy, sw, sh), dst=skia.Rect.MakeXYWH(dx, dy, dw, dh), paint=self._paint
            )

    @staticmethod
    def createImageData(width: int, height: int) -> np.ndarray:
        """Creates an image data object with the given *width* and *height*.

        :param width: The width of the image data.
        :param height: The height of the image data.
        :return: A numpy array representing the image data.
        """
        return np.zeros((height, width, 4), dtype=np.uint8)

    def getImageData(self, sx: int, sy: int, sw: int, sh: int) -> np.ndarray:
        """Gets the image data from the given rectangle from (*sx*, *sy*) with width *sw* and height *sh*.

        :param sx: The x-axis coordinate in the canvas to get the image data from.
        :param sy: The y-axis coordinate in the canvas to get the image data from.
        :param sw: The width of the image data to get.
        :param sh: The height of the image data to get.
        """
        array = np.empty((sh, sw, 4), dtype=np.uint8)
        if not self._canvas.readPixels(skia.Pixmap(array), sx, sy):
            raise RuntimeError('Failed to read pixels')
        return array

    def putImageData(
        self,
        image_data: np.ndarray,
        dx: int = 0,
        dy: int = 0,
        dirty_x: int | None = None,
        dirty_y: int | None = None,
        dirty_width: int | None = None,
        dirty_height: int | None = None,
    ) -> None:
        """Puts the given image data at (*dx*, *dy*) that's inside the given rectangle from (*dirty_x*, *dirty_y*)
        with *dirty_width* and *dirty_height*.

        :param image_data: The image data to put.
        :param dx: The x-axis coordinate to put the image data at.
        :param dy: The y-axis coordinate to put the image data at.
        :param dirty_x: The x-axis coordinate of the rectangle in the image data to put.
        :param dirty_y: The y-axis coordinate of the rectangle in the image data to put.
        :param dirty_width: The width of the rectangle in the image data to put.
        :param dirty_height: The height of the rectangle in the image data to put.
        """
        img_rect: skia.IRect = skia.IRect.MakeXYWH(0, 0, image_data.shape[1], image_data.shape[0])
        if dirty_x is None or img_rect.intersect(skia.IRect.MakeXYWH(dirty_x, dirty_y, dirty_width, dirty_height)):
            l, t = img_rect.left(), img_rect.top()
            self._canvas.writePixels(
                skia.ImageInfo.Make(
                    img_rect.width(),
                    img_rect.height(),
                    skia.ColorType.kRGBA_8888_ColorType,
                    skia.AlphaType.kUnpremul_AlphaType,
                ),
                image_data if l == 0 and t == 0 else image_data[t:, l:],
                x=dx + l,
                y=dy + t,
            )

    @property
    def imageSmoothingEnabled(self) -> bool:
        """Whether image smoothing is enabled."""
        return self._paint.isAntiAlias()

    @imageSmoothingEnabled.setter
    def imageSmoothingEnabled(self, value: bool) -> None:
        self._paint.setAntiAlias(value)

    def save(self) -> None:
        """Saves the current state."""
        self._canvas.save()

    def restore(self) -> None:
        """Restores the last saved state."""
        self._canvas.restore()

    def __enter__(self) -> None:
        """Enters the context, saving the current state."""
        self._canvas.save()

    def __exit__(self, __exc_type: Any, __exc_value: Any, __traceback: Any) -> None:
        """Exits the context, restoring the last saved state."""
        self._canvas.restore()

    def point(self, x: float, y: float) -> None:
        """Draws a point at (*x*, *y*). The point is either a square (``LINE_CAP_SQUARE``), circle (``LINE_CAP_ROUND``)
        or invisible (``LINE_CAP_BUTT``) depending on the canvas's ``lineCap``. The point must be stroked/filled to
        make it visible.

        :param x: The x-axis coordinate of the point.
        :param y: The y-axis coordinate of the point.
        """
        self._path.moveTo(x, y).close()

    def circle(self, x: float, y: float, r: float) -> None:
        """Draws a circle centered at (*x*, *y*) with radius *r*.

        :param x: The x-axis coordinate of the circle's center.
        :param y: The y-axis coordinate of the circle's center.
        :param r: The radius of the circle.
        """
        self._path.addCircle(x, y, r)

    def square(self, x: float, y: float, w: float) -> None:
        """Draws a square from (*x*, *y*) with width and height *w*.

        :param x: The x-axis coordinate of the square's top-left corner.
        :param y: The y-axis coordinate of the square's top-left corner.
        :param w: The width of the square.
        """
        self._path.addRect(x, y, x + w, y + w)

    @staticmethod
    def parse_RR_radius(r: float | Sequence[float]) -> tuple[float, ...]:
        """Parses round rect radius from different formats.

        .. seealso:: :meth:`roundedRect`
        """
        if isinstance(r, (int, float)):
            return (r,) * 8
        else:
            l = len(r)
            if l == 1:  # Just a number
                return (r[0],) * 8
            elif l < 4:  # Two number, rx and ry
                return (r[0], r[1]) * 4
            elif l < 8:  # Corner radius, rx == ry
                return r[0], r[0], r[1], r[1], r[2], r[2], r[3], r[3]
            else:  # All different radius
                return r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]

    def roundedRect(self, x: float, y: float, w: float, h: float | None = None, r: float | Sequence[float] = 0) -> None:
        """Draws a rounded rectangle from (*x*, *y*) with width *w*, height *h* (defaults to *w*) and radius *r*. *r*
        is in clockwise direction starting from the top left corner and can either be

          * a number or a tuple with a single element: The radius for every corner.
          * a tuple with two elements: The x and y radius for every corner.
          * a tuple with four elements: The radius of each corner.
          * a tuple with eight elements: The x and y radius of each corner.

        :param x: The x-axis coordinate of the rectangle's top-left corner.
        :param y: The y-axis coordinate of the rectangle's top-left corner.
        :param w: The width of the rectangle.
        :param h: The height of the rectangle. Defaults to *w*.
        :param r: The radius of the rectangle in a format as described above.
        """
        if h is None:
            h = w
        self._path.addRoundRect(skia.Rect.MakeXYWH(x, y, w, h), Context2d.parse_RR_radius(r))

    def line(self, x0: float, y0: float, x1: float, y1: float) -> None:
        """Draws a line from (*x0*, *y0*) to (*x1*, *y1*).

        :param x0: The x-axis coordinate of the start point.
        :param y0: The y-axis coordinate of the start point.
        :param x1: The x-axis coordinate of the end point.
        :param y1: The y-axis coordinate of the end point.
        """
        self._path.moveTo(x0, y0).lineTo(x1, y1)

    def bezier_curve(
        self,
        x0: float,
        y0: float,  # Point
        x1: float | None = None,
        y1: float | None = None,  # Line
        x2: float | None = None,
        y2: float | None = None,  # Quadratic bezier
        x3: float | None = None,
        y3: float | None = None,  # Cubic bezier
    ) -> None:
        """Generic method to draw curves. With a single point (x0, y0), a point is drawn. With two sets of points (
        x1, y1), a line is drawn. With three sets of points (x2, y2), a quadratic bezier is drawn. With four sets of
        points (x3, y3), a cubic bezier curve is drawn.

        :param x0: The x-axis coordinate of the start point.
        :param y0: The y-axis coordinate of the start point.
        :param x1: The x-axis coordinate of the first control point.
        :param y1: The y-axis coordinate of the first control point.
        :param x2: The x-axis coordinate of the second control point.
        :param y2: The y-axis coordinate of the second control point.
        :param x3: The x-axis coordinate of the end point.
        :param y3: The y-axis coordinate of the end point.
        """
        self._path.moveTo(x0, y0)
        if x1 is None:  # Point
            self._path.close()
        elif x2 is None:  # Line
            self._path.lineTo(x1, y1)
        elif x3 is None:  # Quadratic bezier
            self._path.quadTo(x1, y1, x2, y2)
        else:  # Cubic bezier
            self._path.cubicTo(x1, y1, x2, y2, x3, y3)

    @staticmethod
    def catmullrom_to_bezier(
        p0: float, p1: float, p2: float, p3: float, t: float = 1
    ) -> tuple[float, float, float, float]:
        """Transforms a four point Catmull-Rom curve with tension *t* to a four point bezier curve. The points returned
        can be used to draw the curve with :meth:`bezier_curve`.

        Call this method twice with the x and y coordinates of the Catmull-Rom curve separately. You can also use numpy
        array of two elements to do the transformation at once.

        >>> x0, y0, x1, y1, x2, y2, x3, y3 = 10, 20, 30, 40, 50, 60, 70, 80
        >>> bx0, bx1, bx2, bx3 = Context2d.catmullrom_to_bezier(x0, x1, x2, x3)
        >>> by0, by1, by2, by3 = Context2d.catmullrom_to_bezier(y0, y1, y2, y3)
        >>> context2d.bezier_curve(bx0, by0, bx1, by1, bx2, by2, bx3, by3)

        :param p0: The start point.
        :param p1: The first control point.
        :param p2: The second control point.
        :param p3: The end point.
        :param t: The tension of the curve.
        :return: A tuple with four points describing the corresponding bezier curve.
        """
        t *= 6  # https://pomax.github.io/bezierinfo/#catmullconv
        return p1, p1 + (p2 - p0) / t, p2 - (p3 - p1) / t, p2

    def catmullRom(
        self, x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, t: float
    ) -> None:
        """Draws a four point Catmull-Rom curve from (x1, y1) to (x2, y2) with control points (x0, y0) and (x3, y3).

        :param x0: The x-axis coordinate of the start point.
        :param y0: The y-axis coordinate of the start point.
        :param x1: The x-axis coordinate of the first control point.
        :param y1: The y-axis coordinate of the first control point.
        :param x2: The x-axis coordinate of the second control point.
        :param y2: The y-axis coordinate of the second control point.
        :param x3: The x-axis coordinate of the end point.
        :param y3: The y-axis coordinate of the end point.
        :param t: The tension of the curve.
        """
        x0, x1, x2, x3 = Context2d.catmullrom_to_bezier(x0, x1, x2, x3, t)
        y0, y1, y2, y3 = Context2d.catmullrom_to_bezier(y0, y1, y2, y3, t)
        self._path.moveTo(x0, y0).cubicTo(x1, y1, x2, y2, x3, y3)

    @staticmethod
    def __get_control_points(
        x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, t: float = 0.5
    ) -> tuple[Point, Point]:  # http://scaledinnovation.com/analytics/splines/aboutSplines.html
        d01 = math.hypot(x1 - x0, y1 - y0)
        d12 = math.hypot(x2 - x1, y2 - y1)
        fa = t * d01 / (d01 + d12)
        fb = t * d12 / (d01 + d12)
        return (x1 - fa * (x2 - x0), y1 - fa * (y2 - y0)), (x1 + fb * (x2 - x0), y1 + fb * (y2 - y0))

    def spline(self, points: Sequence[Point], tension: float = 0.5, closed: bool = False) -> None:
        """Draws a spline passing through all the points (at least 3) with given tension. If closed is `True`, the curve
        is closed smoothly.

        :param points: A list of points.
        :param tension: The tension of the curve.
        :param closed: Whether the curve is closed.

        :note: To get a smoothly closed curve, the first and last points must be different.
        """
        if closed:
            points = [points[-1], *points, points[0], points[1]]
        cps: list[Point] = []
        for i in range(len(points) - 2):
            cps.extend(Context2d.__get_control_points(*points[i], *points[i + 1], *points[i + 2], tension))

        if closed:
            self._path.moveTo(*points[1])
        else:
            self._path.moveTo(*points[0]).quadTo(*cps[0], *points[1])
        for i in range(1, len(points) - 2):
            self._path.cubicTo(*cps[2 * i - 1], *cps[2 * i], *points[i + 1])
        if closed:
            self._path.close()
        else:
            self._path.quadTo(*cps[-1], *points[-1])

    def add_path(self, path: skia.Path, move_to: bool = False) -> None:
        """Adds a *path* to the current path. If *move_to* is ``True``, moves the starting point on the path. This
        removes the line joining the current point to the start of the path.

        :param path: The path to add.
        :param move_to: Whether to move to the start of the path.
        """
        self._path.addPath(
            path, skia.Path.AddPathMode.kAppend_AddPathMode if move_to else skia.Path.AddPathMode.kExtend_AddPathMode
        )

    @property
    def path(self) -> skia.Path:
        """Returns the internal path object. All drawings are appended to this object."""
        return self._path

    def save_path(self, new_path: bool = True) -> int:
        """Pushes the current path on an internal stack and returns the size of the stack. Restore the path with
        :meth:`restore_path`. A new path is created if *new_path* is ``True``, else the old path is extended.

        :param new_path: Whether to create a new path.
        :return: The size of the stack.
        """
        self.__paths.append(self._path)
        if new_path:
            self._path = skia.Path()
        else:
            self._path = skia.Path(self._path)
        return len(self.__paths)

    def restore_path(self) -> None:
        """Restores the last saved path, if available, as the current path."""
        if self.__paths:
            self._path = self.__paths.pop()
