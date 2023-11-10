"""Class and functions to manage the style of an entity."""
from __future__ import annotations

import re
from enum import Enum
from typing import Literal

from animator import skia
from animator._common_types import ClipLike, ColorLike
from animator.graphics.color import color as parse_color
from animator.graphics.shader import _BlenderLike, _to_blender

__ALPHA_RE = re.compile(br'[A-Za-z]+')
__stroke = {
    'SkPath1DPathEffect',
    'SkDashImpl',
    'SkStrokePE',
    'SkPath2DPathEffect',
    'SkCornerPathEffect',
    'SkDiscretePathEffect',
    'SkMatrixPE',
    'SkTrimPE',
}
__fill = {
    'SkPath2DPathEffect',
    'SkCornerPathEffect',
    'SkDiscretePathEffect',
    'SkMatrixPE',
    'SkTrimPE',
    'SkLine2DPathEffect',
    'SkStrokeAndFillPE',
}
__recursive = {'SkOpPE', 'SkComposePathEffect', 'SkSumPathEffect'}


def _calculate_path_effect_needs(effect: skia.PathEffect) -> tuple[bool, bool]:
    """Returns a tuple of whether the effect needs to be applied to the (stroke, fill)."""
    type_ = effect.getTypeName()
    types = {t.decode() for t in __ALPHA_RE.findall(effect.serialize().bytes())} if type_ in __recursive else {type_}
    return bool(types & __stroke), bool(types & __fill)


class Style:
    """
    The style of an entity. This class initializes with the default style values, which can be changed.

    :ivar clip: The clip to be applied to the entity. The clip is applied after transformations.
    :ivar paint_style: Paint style for the entity; if the entity is filled, stroked, or both.
    :ivar optimization: Optimization to apply for the final paint since applying the final paint can be expensive.
    """

    STROKE_WIDTH: float = 5
    STROKE_CAP: skia.Paint.Cap = skia.Paint.Cap.kRound_Cap
    STROKE_JOIN: skia.Paint.Join = skia.Paint.Join.kRound_Join
    STROKE_MITER: float = 10
    FILL_COLOR: skia.Color4f | skia.Shader = skia.Color4f(0.9686274509803922, 0.7333333333333333, 0, 1)
    STROKE_COLOR: skia.Color4f | skia.Shader = skia.Color4f(0, 0.47058823529411764, 0.8431372549019608, 1)
    OPACITY: float = 1

    class PaintStyle(Enum):
        STROKE_ONLY = 0  #: Only stroke the entity.
        FILL_ONLY = 1  #: Only fill the entity.
        FILL_THEN_STROKE = 2  #: Fill the entity, then stroke it. This is the most common style.
        STROKE_THEN_FILL = 3  #: Stroke the entity, then fill it.

        @classmethod
        def from_style_str(cls, style: Literal['stroke', 'fill', 'fill-stroke', 'stroke-fill']) -> Style.PaintStyle:
            if style == 'stroke':
                return cls.STROKE_ONLY
            elif style == 'fill':
                return cls.FILL_ONLY
            elif style == 'fill-stroke':
                return cls.FILL_THEN_STROKE
            elif style == 'stroke-fill':
                return cls.STROKE_THEN_FILL
            else:
                raise ValueError(f'Invalid style string: {style}')

    class FinalPaintOptimization(Enum):
        NONE = 0  #: Do not apply any properties from the final paint.
        OPACITY_ONLY = 1  #: Only apply opacity from the final paint if present.
        ALL = 2  #: Apply all properties from the final paint if present.
        ALWAYS = 3  #: Always apply all properties from the final paint.

    def __init__(self):
        self.__fill_paint = skia.Paint(
            antiAlias=True,
            strokeWidth=Style.STROKE_WIDTH,
            strokeCap=Style.STROKE_CAP,
            strokeJoin=Style.STROKE_JOIN,
            strokeMiter=Style.STROKE_MITER,
        )
        self.__stroke_paint = skia.Paint(self.__fill_paint)
        self.__final_paint = skia.Paint(antiAlias=True, alphaf=Style.OPACITY)

        self.__fill_paint.setStyle(skia.Paint.Style.kFill_Style)
        if isinstance(Style.FILL_COLOR, skia.Color4f):
            self.__fill_paint.setColor4f(skia.Color4f(Style.FILL_COLOR))
        else:
            self.__fill_paint.setShader(Style.FILL_COLOR)

        self.__stroke_paint.setStyle(skia.Paint.Style.kStroke_Style)
        if isinstance(Style.STROKE_COLOR, skia.Color4f):
            self.__stroke_paint.setColor4f(skia.Color4f(Style.STROKE_COLOR))
        else:
            self.__stroke_paint.setShader(Style.STROKE_COLOR)

        self.clip: ClipLike | None = None

        self.paint_style: Style.PaintStyle = Style.PaintStyle.FILL_THEN_STROKE
        self.optimization: Style.FinalPaintOptimization = Style.FinalPaintOptimization.OPACITY_ONLY

    @property
    def fill_paint(self) -> skia.Paint:
        """The paint used to fill the entity."""
        return self.__fill_paint

    @property
    def stroke_paint(self) -> skia.Paint:
        """The paint used to stroke the entity."""
        return self.__stroke_paint

    @property
    def final_paint(self) -> skia.Paint:
        """The final paint used to draw the entity."""
        return self.__final_paint

    @property
    def anti_alias(self) -> bool:
        """Whether the entity is anti-aliased."""
        return self.__stroke_paint.isAntiAlias()

    @anti_alias.setter
    def anti_alias(self, value: bool) -> None:
        """:note: Setter modifies all three paints."""
        self.__stroke_paint.setAntiAlias(value)
        self.__fill_paint.setAntiAlias(value)
        self.__final_paint.setAntiAlias(value)

    @property
    def stroke_width(self) -> float:
        """The width of the stroke."""
        return self.__stroke_paint.getStrokeWidth()

    @stroke_width.setter
    def stroke_width(self, value: float) -> None:
        """:note: Setter modifies ``stroke_paint`` and ``fill_paint``."""
        self.__stroke_paint.setStrokeWidth(value)
        self.__fill_paint.setStrokeWidth(value)

    @property
    def stroke_cap(self) -> skia.Paint.Cap:
        """The cap of the stroke."""
        return self.__stroke_paint.getStrokeCap()

    @stroke_cap.setter
    def stroke_cap(self, value: skia.Paint.Cap) -> None:
        """:note: Setter modifies ``stroke_paint`` and ``fill_paint``."""
        self.__stroke_paint.setStrokeCap(value)
        self.__fill_paint.setStrokeCap(value)

    @property
    def stroke_join(self) -> skia.Paint.Join:
        """The join of the stroke."""
        return self.__stroke_paint.getStrokeJoin()

    @stroke_join.setter
    def stroke_join(self, value: skia.Paint.Join) -> None:
        """:note: Setter modifies ``stroke_paint`` and ``fill_paint``."""
        self.__stroke_paint.setStrokeJoin(value)
        self.__fill_paint.setStrokeJoin(value)

    @property
    def stroke_miter(self) -> float:
        """The miter of the stroke."""
        return self.__stroke_paint.getStrokeMiter()

    @stroke_miter.setter
    def stroke_miter(self, value: float) -> None:
        """:note: Setter modifies ``stroke_paint`` and ``fill_paint``."""
        self.__stroke_paint.setStrokeMiter(value)
        self.__fill_paint.setStrokeMiter(value)

    @property
    def opacity(self) -> float:
        """The opacity of the entity."""
        return self.__final_paint.getAlphaf()

    @opacity.setter
    def opacity(self, value: float) -> None:
        """:note: Setter modifies ``final_paint``."""
        self.__final_paint.setAlphaf(value)

    def get_dash(self) -> skia.PathEffect.DashInfo | None:
        """Get the dash of the stroke."""
        path_effect = self.__stroke_paint.getPathEffect()
        if path_effect is None:
            return None
        return path_effect.asADash()

    def set_dash(self, intervals: list[float], phase: float = 0) -> None:
        """Set the dash of the stroke.

        :note: Modifies ``stroke_paint``.
        """
        if intervals is None:
            self.__stroke_paint.setPathEffect(None)
        self.__stroke_paint.setPathEffect(skia.DashPathEffect.Make(intervals, phase))

    def set_trim(self, start: float | None = 0, stop: float = 1) -> None:
        """Set the trim of the stroke.

        :note: Modifies ``stroke_paint``.
        """
        if start is None:
            self.__stroke_paint.setPathEffect(None)
        else:
            self.__stroke_paint.setPathEffect(skia.TrimPathEffect.Make(start, stop))

    def set_shadow(
        self,
        dx: float,
        dy: float,
        sx: float = 0,
        sy: float = 0,
        color: ColorLike | None = None,
        shadow_only: bool = False,
    ) -> None:
        """Set the shadow of the entity.

        :param dx: The x offset of the shadow.
        :param dy: The y offset of the shadow.
        :param sx: The sigma x of the shadow.
        :param sy: The sigma y of the shadow.
        :param color: The color of the shadow. If ``None``, a translucent fill color will be used.
        :param shadow_only: Whether the shadow should be the only thing drawn.

        :note: Modifies ``final_paint``.
        """
        if color is None:
            color4f = self.__fill_paint.getColor4f()
            color4f.fA = 0.3
        else:
            color4f = skia.Color4f(parse_color(color))
        self.__final_paint.setImageFilter(
            (skia.ImageFilters.DropShadowOnly if shadow_only else skia.ImageFilters.DropShadow)(dx, dy, sx, sy, color4f)
        )
        self.optimization = Style.FinalPaintOptimization.ALL

    def set_glow(self, sigma: float, color: ColorLike | None = None, glow_only: bool = False) -> None:
        """Set a glow emmiting from behind the entity.

        :param sigma: The sigma of the glow.
        :param color: The color of the glow. If ``None``, a translucent fill color will be used.
        :param glow_only: Whether the glow should be the only thing drawn.

        :note: Modifies ``final_paint``.
        """
        self.set_shadow(0, 0, sigma, sigma, color, glow_only)

    def set_fill_color(self, c: ColorLike, *args, **kwargs) -> None:
        """Set the fill color of the entity. This takes the same arguments as :func:`animator.color`.

        :note: Modifies ``fill_paint``.
        """
        self.__fill_paint.setColor4f(parse_color(c, *args, **kwargs))

    def set_stroke_color(self, c: ColorLike, *args, **kwargs) -> None:
        """Set the stroke color of the entity. This takes the same arguments as :func:`animator.color`.

        :note: Modifies ``stroke_paint``.
        """
        self.__stroke_paint.setColor4f(parse_color(c, *args, **kwargs))

    def set_fill_shader(self, shader: skia.Shader) -> None:
        """Set the fill shader of the entity.

        :note: Modifies ``fill_paint``.
        """
        self.__fill_paint.setShader(shader)

    def set_stroke_shader(self, shader: skia.Shader) -> None:
        """Set the stroke shader of the entity.

        :note: Modifies ``stroke_paint``.
        """
        self.__stroke_paint.setShader(shader)

    def set_fill_color_or_shader(self, c: ColorLike | skia.Shader, *args, **kwargs) -> None:
        """Set the fill color or shader of the entity.

        :note: Modifies ``fill_paint``.
        """
        if isinstance(c, skia.Shader):
            self.set_fill_shader(c)
        else:
            self.set_fill_color(c, *args, **kwargs)

    def set_stroke_color_or_shader(self, c: ColorLike | skia.Shader, *args, **kwargs) -> None:
        """Set the stroke color or shader of the entity.

        :note: Modifies ``stroke_paint``.
        """
        if isinstance(c, skia.Shader):
            self.set_stroke_shader(c)
        else:
            self.set_stroke_color(c, *args, **kwargs)

    def set_image_filter(
        self, filter: skia.ImageFilter | skia.ColorFilter | skia.Image | skia.Picture | skia.Shader | None
    ) -> None:
        """Set the image filter in the ``final_paint``.

        :note: Modifies ``final_paint``.
        """
        if isinstance(filter, skia.ColorFilter):
            filter = skia.ImageFilters.ColorFilter(filter)
        elif isinstance(filter, skia.Image):
            filter = skia.ImageFilters.Image(filter)
        elif isinstance(filter, skia.Picture):
            filter = skia.ImageFilters.Picture(filter)
        elif isinstance(filter, skia.Shader):
            filter = skia.ImageFilters.Shader(filter)
        self.__final_paint.setImageFilter(filter)
        if filter is not None:
            self.optimization = Style.FinalPaintOptimization.ALL

    def set_blend_mode(self, mode: _BlenderLike | None) -> None:
        """Set the blend mode of the entity.

        :note: Modifies ``final_paint``.
        """
        self.__final_paint.setBlender(mode if mode is None else _to_blender(mode))
        if mode is not None:
            self.optimization = Style.FinalPaintOptimization.ALL

    def set_mask_filter(self, filter: skia.MaskFilter | skia.Shader | None) -> None:
        """Set the mask filter of the entity.

        :note: Modifies ``fill_paint``.
        """
        if isinstance(filter, skia.Shader):
            filter = skia.ShaderMaskFilter.Make(filter)
        self.__fill_paint.setMaskFilter(filter)

    def set_color_filter(self, filter: skia.ColorFilter | skia.ColorMatrix | skia.ColorTable | None) -> None:
        """Set the color filter of the entity.

        :note: Modifies ``final_paint``.
        """
        if isinstance(filter, skia.ColorMatrix):
            filter = skia.ColorFilters.Matrix(filter)
        elif isinstance(filter, skia.ColorTable):
            filter = skia.ColorFilters.Table(filter)
        self.__final_paint.setColorFilter(filter)
        if filter is not None:
            self.optimization = Style.FinalPaintOptimization.ALL

    def set_path_effect(self, effect: skia.PathEffect | None) -> None:
        """
        Set the path effect of the entity. The effect is intelligently applied to the ``stroke_paint`` or ``fill_paint``
        depending on its type. It'd make more sense to apply the effect manually to the paint you want to apply it to
        using ``style.stroke_paint.setPathEffect(effect)`` or ``style.fill_paint.setPathEffect(effect)``.

        :note: Modifies ``stroke_paint``, ``fill_paint`` or both.
        """
        if effect is None:
            self.__fill_paint.setPathEffect(None)
            self.__stroke_paint.setPathEffect(None)
        else:
            needs_stroke, needs_fill = _calculate_path_effect_needs(effect)
            if needs_stroke:
                self.__stroke_paint.setPathEffect(effect)
            if needs_fill:
                self.__fill_paint.setPathEffect(effect)

    def set_from_kwargs(self, **kwargs) -> None:
        """
        Set the style from arguments. Supported arguments are the same as the attributes of this class and

            - ``fill_color``: The fill color or shader of the entity. Takes all the arguments of :func:`animator.color`.
            - ``stroke_color``: The stroke color or shader of the entity. Takes all the arguments of
              :func:`animator.color`.
            - ``image_filter``: The image filter of the entity. Can be a :class:`skia.ImageFilter`, a
              :class:`skia.ColorFilter`, a :class:`skia.Image`, a :class:`skia.Picture` or a :class:`skia.Shader`.
            - ``blend_mode``: The blend mode of the entity.
            - ``mask_filter``: The mask filter of the entity. Can be a :class:`skia.MaskFilter` or a
              :class:`skia.Shader`.
            - ``color_filter``: The color filter of the entity. Can be a :class:`skia.ColorFilter`, a
              :class:`skia.ColorMatrix` or a :class:`skia.ColorTable`.
            - ``path_effect``: The path effect to apply to the entity's path, intelligently applied to the
              ``stroke_paint`` or ``fill_paint``.
            - ``dash``: The dash of the stroke. Can be ``None`` or a list of floats.
            - ``trim``: The trim of the stroke. Can be ``None`` or a tuple of ``(start, end)``.
            - ``style``: The style of the paint. Can be ``'fill'``, ``'stroke'``, ``'fill-stroke'`` (default) or
              ``'stroke-fill'``.
        """
        for key, value in kwargs.items():
            if key == 'fill_color':
                self.set_fill_color_or_shader(value)
            elif key == 'stroke_color':
                self.set_stroke_color_or_shader(value)
            elif key == 'image_filter':
                self.set_image_filter(value)
            elif key == 'blend_mode':
                self.set_blend_mode(value)
            elif key == 'mask_filter':
                self.set_mask_filter(value)
            elif key == 'color_filter':
                self.set_color_filter(value)
            elif key == 'path_effect':
                self.set_path_effect(value)
            elif key == 'dash':
                self.set_dash(value)
            elif key == 'trim':
                if value is None:
                    self.set_trim(None)
                else:
                    self.set_trim(*value)
            elif key == 'style':
                self.paint_style = Style.PaintStyle.from_style_str(value)
            elif hasattr(self, key) and not callable(getattr(self, key)) and not key.startswith("_"):
                setattr(self, key, value)

    def __copy__(self) -> Style:
        """Return a copy of the style."""
        style: Style = object.__new__(type(self))
        style.__fill_paint = skia.Paint(self.__fill_paint)
        style.__stroke_paint = skia.Paint(self.__stroke_paint)
        style.__final_paint = skia.Paint(self.__final_paint)
        style.clip = (
            self.clip.__class__(*self.clip)  # type: ignore union type matches
            if isinstance(self.clip, (skia.IRect, skia.Rect))
            else self.clip.__class__(self.clip)  # type: ignore union type matches
            if isinstance(self.clip, (skia.Path, skia.RRect, skia.Region))
            else self.clip
        )
        style.paint_style = self.paint_style
        style.optimization = self.optimization
        return style

    def nothing_to_draw(self) -> bool:
        """Returns ``True`` if the style has nothing to draw. However, even if this returns ``False``, the style may not
        draw anything."""
        if self.optimization == Style.FinalPaintOptimization.NONE:
            return False
        if self.optimization == Style.FinalPaintOptimization.OPACITY_ONLY:
            return self.__final_paint.getAlpha() == 0
        return self.__final_paint.nothingToDraw()

    def apply_clip(self, canvas: skia.Canvas) -> None:
        """Apply the clip to the canvas."""
        if self.clip is None:
            return
        if isinstance(self.clip, skia.IRect):
            canvas.clipIRect(self.clip)
        elif isinstance(self.clip, skia.Path):
            canvas.clipPath(self.clip, doAntiAlias=True)
        elif isinstance(self.clip, skia.RRect):
            canvas.clipRRect(self.clip, doAntiAlias=True)
        elif isinstance(self.clip, skia.Rect):
            canvas.clipRect(self.clip, doAntiAlias=True)
        elif isinstance(self.clip, skia.Region):
            canvas.clipRegion(self.clip)
        elif isinstance(self.clip, skia.Shader):
            canvas.clipShader(self.clip)
        else:  # tuple, which is a rect
            for i in self.clip:
                if i != int(i):  # found a float
                    canvas.clipRect(self.clip, doAntiAlias=True)
                    break
            else:  # all ints
                canvas.clipIRect(tuple(int(i) for i in self.clip))  # type: ignore tuple has correct number of elements

    def apply_final_paint(self, canvas: skia.Canvas) -> None:
        """Apply the final paint to the canvas."""
        if self.optimization == Style.FinalPaintOptimization.OPACITY_ONLY and self.__final_paint.getAlpha() < 255:
            canvas.saveLayerAlphaf(None, self.__final_paint.getAlphaf())
        elif (
            self.optimization == Style.FinalPaintOptimization.ALL and not self.__final_paint.nothingToDraw()
        ) or self.optimization == Style.FinalPaintOptimization.ALWAYS:
            canvas.saveLayer(None, self.__final_paint)
