from __future__ import annotations

from typing import TYPE_CHECKING, Any

from animator import skia
from animator._common_types import ColorLike
from animator.anim.anim import Anim
from animator.graphics import color as parse_color
from animator.graphics.style import Style

if TYPE_CHECKING:
    from animator.entity import Entity


class PaintColorAnim(Anim):
    """Animates the color of a paint."""

    def __init__(self, paint: skia.Paint, color: skia.Color4f, duration: float, **kwargs: Any) -> None:
        """
        :param paint: The paint to animate.
        :param color: The color to animate the paint to.
        :param duration: The duration of the animation.
        """
        super().__init__(duration, **kwargs)
        self.__paint: skia.Paint = paint
        self.__target_color: skia.Color4f = color
        self.__initial_color: skia.Color4f = None  # type: ignore lateinit
        self.__diff_color: skia.Color4f = None  # type: ignore lateinit

    def start(self) -> None:
        self.__initial_color = self.__paint.getColor4f()
        self.__diff_color = skia.Color4f(
            self.__target_color.fR - self.__initial_color.fR,
            self.__target_color.fG - self.__initial_color.fG,
            self.__target_color.fB - self.__initial_color.fB,
            self.__target_color.fA - self.__initial_color.fA,
        )

    def update(self, t: float) -> None:
        self.__paint.setColor4f(
            skia.Color4f(
                self.__initial_color.fR + self.__diff_color.fR * t,
                self.__initial_color.fG + self.__diff_color.fG * t,
                self.__initial_color.fB + self.__diff_color.fB * t,
                self.__initial_color.fA + self.__diff_color.fA * t,
            )
        )

    def end(self) -> None:
        self.__paint.setColor4f(self.__target_color)


_ColorOrShader = skia.Color4f | skia.Shader


class PaintShaderAnim(Anim):
    """Animates the shader of a paint."""

    _EFFECT: skia.RuntimeEffect = skia.RuntimeEffect.MakeForShader(
        'uniform shader s,d;uniform float t;half4 main(vec2 c){return mix(s.eval(c),d.eval(c),t);}'
    ).effect  # type: ignore if this is None, let the animation fail

    def __init__(self, paint: skia.Paint, shader: _ColorOrShader, duration: float, **kwargs: Any) -> None:
        """
        :param paint: The paint to animate.
        :param shader: The shader to animate the paint to. May be a color too.
        :param duration: The duration of the animation.
        """
        super().__init__(duration, **kwargs)
        self.__paint: skia.Paint = paint
        if isinstance(shader, skia.Shader):
            self.__target_color: skia.Color4f | None = None
            self.__target_shader: skia.Shader = shader
        else:
            self.__target_color: skia.Color4f | None = shader
            self.__target_shader: skia.Shader = skia.Shader.Color(self.__target_color)
        self.__initial_shader: skia.Shader = None  # type: ignore lateinit
        self.__builder: skia.RuntimeShaderBuilder = None  # type: ignore lateinit

    def start(self) -> None:
        self.__initial_shader = self.__paint.refShader()
        if self.__initial_shader is None:  # no shader means color, upgrade to shader
            self.__initial_shader = skia.Shader.Color(self.__paint.getColor4f())
            self.__paint.setShader(self.__initial_shader)
            self.__paint.setAlphaf(1)
        self.__builder = skia.RuntimeShaderBuilder(PaintShaderAnim._EFFECT)
        self.__builder.child('s').set(self.__initial_shader)
        self.__builder.child('d').set(self.__target_shader)

    def update(self, t: float) -> None:
        self.__builder.uniform('t').set(t)
        self.__paint.setShader(self.__builder.makeShader())

    def end(self) -> None:
        if self.__target_color is None:
            self.__paint.setShader(self.__target_shader)
        else:
            self.__paint.setShader(None)
            self.__paint.setColor4f(self.__target_color)


__ColorLikeOrShader = ColorLike | skia.Shader


def parse_if_color(c: __ColorLikeOrShader | None) -> _ColorOrShader | None:
    if c is None:
        return None
    if isinstance(c, skia.Shader):
        return c
    return parse_color(c)


class ColorAnim(Anim):
    """Animate the color (or shader) of an entity."""

    def __init__(
        self,
        entity: Entity,
        duration: float,
        fill_color: __ColorLikeOrShader | None = None,
        stroke_color: __ColorLikeOrShader | None = None,
        **kwargs: Any,
    ) -> None:
        """
        :param entity: The entity to animate.
        :param duration: The duration of the animation.
        :param fill_color: The new fill color or shader. If ``None``, the fill color will not be animated.
        :param stroke_color: The new stroke color or shader. If ``None``, the stroke color will not be animated.
        """
        super().__init__(duration, **kwargs)
        self._entity: Entity = entity
        self.__target_fill_color: _ColorOrShader | None = parse_if_color(fill_color)
        self.__target_stroke_color: _ColorOrShader | None = parse_if_color(stroke_color)
        self.__anims: set[Anim] = set()

    def _add_anim(self, paint: skia.Paint, color: _ColorOrShader | None) -> None:
        if color is None:
            return
        if isinstance(color, skia.Shader) or paint.getShader() is not None:  # either initial or target is a shader
            self.__anims.add(PaintShaderAnim(paint, color, self._duration, ease=self.ease_func))
        else:  # both initial and target are colors
            self.__anims.add(PaintColorAnim(paint, color, self._duration, ease=self.ease_func))

    def start(self) -> None:
        self._add_anim(self._entity.style.fill_paint, self.__target_fill_color)
        self._add_anim(self._entity.style.stroke_paint, self.__target_stroke_color)
        for anim in self.__anims:
            anim.start()

    def update(self, t: float) -> None:
        for anim in self.__anims:
            anim.update(t)

    def end(self) -> None:
        for anim in self.__anims:
            anim.end()


def _get_color_from_paint(paint: skia.Paint) -> _ColorOrShader:
    shader = paint.getShader()
    if shader is not None:
        return shader
    return paint.getColor4f()


class StyleAnim(ColorAnim):
    """Animate the style of an entity. Only animates the fill and stroke color/shader and stroke width."""

    def __init__(self, entity: Entity, style: Style, duration: float, **kwargs: Any) -> None:
        super().__init__(
            entity,
            duration,
            _get_color_from_paint(style.fill_paint),
            _get_color_from_paint(style.stroke_paint),
            **kwargs,
        )
        self.__target_style: Style = style
        self.__initial_stroke_width: float = None  # type: ignore
        self.__diff_stroke_width: float = None  # type: ignore lateinit
        self.__target_stroke_width: float = (
            0 if style.paint_style == Style.PaintStyle.FILL_ONLY else style.stroke_width
        )  # TODO: use opacity instead

    def start(self) -> None:
        super().start()
        initial_style = self._entity.style
        if initial_style.paint_style == Style.PaintStyle.FILL_ONLY:
            initial_style.paint_style = self.__target_style.paint_style
            self.__initial_stroke_width = 0
        else:
            self.__initial_stroke_width = initial_style.stroke_width
        self.__diff_stroke_width = self.__target_stroke_width - self.__initial_stroke_width

    def update(self, t: float) -> None:
        super().update(t)
        self._entity.style.stroke_width = self.__initial_stroke_width + self.__diff_stroke_width * t

    def end(self) -> None:
        super().end()
        self._entity.style.stroke_width = self.__target_stroke_width
