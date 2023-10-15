"""Create or insert an entity into the scene. The entity will be added to the scene once the animation starts."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from animator import skia
from animator.anim.anim import Anim
from animator.entity import relpos
from animator.entity.relpos import RelativePosition

if TYPE_CHECKING:
    from animator.entity import Entity


class FadeIn(Anim):
    """Fades in an entity. Effects ``style.opacity``."""

    def __init__(self, entity: Entity, duration: float, **kwargs: Any) -> None:
        super().__init__(duration, **kwargs)
        self.__entity: Entity = entity
        self.__target_opacity: float = None  # type: ignore lateinit

    def start(self) -> None:
        self._scene.add(self.__entity)
        self.__target_opacity = self.__entity.style.opacity
        self.__entity.style.opacity = 0

    def update(self, t: float) -> None:
        self.__entity.style.opacity = self.__target_opacity * t

    def end(self) -> None:
        self.__entity.style.opacity = self.__target_opacity


class SlideIn(Anim):
    """Slides in an entity from outside the scene. Effects ``pos``."""

    def __init__(
        self, entity: Entity, duration: float, dir: RelativePosition = relpos.LEFT, padding: float = 25, **kwargs: Any
    ) -> None:
        """
        :param entity: The entity to slide in.
        :param duration: Duration of the animation.
        :param dir: Relative direction to slide in from. +-1 represents the extreme, just outside the scene. Other
            values will scale this distance.
        :param padding: Extra padding to add around the scene.
        """
        super().__init__(duration, **kwargs)
        self.__entity: Entity = entity
        self.__dir: RelativePosition = dir
        self.__padding: float = padding
        self.__initial_pos: skia.Point = None  # type: ignore lateinit
        self.__target_pos: skia.Point = None  # type: ignore lateinit
        self.__diff_pos: skia.Point = None  # type: ignore lateinit

    def start(self) -> None:
        self._scene.add(self.__entity)
        self.__target_pos = skia.Point(*self.__entity.pos)

        bounds = self.__entity.get_bounds(True)
        dx = (
            self.__target_pos.fX + bounds.right()
            if self.__dir[0] < 0
            else self._scene.width - self.__target_pos.fX - bounds.left()
        )
        dy = (
            self.__target_pos.fY + bounds.bottom()
            if self.__dir[1] < 0
            else self._scene.height - self.__target_pos.fY - bounds.top()
        )
        self.__diff_pos = skia.Point(-self.__dir[0] * (dx + self.__padding), -self.__dir[1] * (dy + self.__padding))

        self.__initial_pos = self.__target_pos - self.__diff_pos
        self.__entity.pos.set(*self.__initial_pos)

    def update(self, t: float) -> None:
        self.__entity.pos.set(*(self.__initial_pos + self.__diff_pos * t))

    def end(self) -> None:
        self.__entity.pos.set(*self.__target_pos)


class ScaleIn(Anim):
    """Scale up an entity. Effects ``transformation.scaleX`` and ``transformation.scaleY``."""

    def __init__(self, entity: Entity, duration: float, **kwargs: Any) -> None:
        super().__init__(duration, **kwargs)
        self.__entity: Entity = entity
        self.__target_scaleX: float = None  # type: ignore lateinit
        self.__target_scaleY: float = None  # type: ignore lateinit

    def start(self) -> None:
        self._scene.add(self.__entity)
        self.__target_scaleX = self.__entity.transformation.scaleX
        self.__target_scaleY = self.__entity.transformation.scaleY
        self.__entity.transformation.scaleX = self.__entity.transformation.scaleY = 0

    def update(self, t: float) -> None:
        self.__entity.transformation.scaleX = self.__target_scaleX * t
        self.__entity.transformation.scaleY = self.__target_scaleY * t

    def end(self) -> None:
        self.__entity.transformation.scaleX = self.__target_scaleX
        self.__entity.transformation.scaleY = self.__target_scaleY


def _add_path_effect(
    paint: skia.Paint, initial_path_effect: skia.PathEffect | None, new_path_effect: skia.PathEffect
) -> None:
    paint.setPathEffect(
        new_path_effect
        if initial_path_effect is None
        else skia.PathEffect.MakeCompose(new_path_effect, initial_path_effect)
    )


class DrawIn(Anim):
    """
    Draws an entity (preferably a :class:`PathEntity`) into the scene. Effects the entity's fill and stroke path effect.
    """

    def __init__(self, entity: Entity, duration: float, **kwargs: Any) -> None:
        super().__init__(duration, **kwargs)
        self.__entity: Entity = entity
        self.__initial_fill_path_effect: skia.PathEffect | None = None
        self.__initial_stroke_path_effect: skia.PathEffect | None = None

    def start(self) -> None:
        self._scene.add(self.__entity)
        self.__initial_fill_path_effect = self.__entity.style.fill_paint.refPathEffect()
        self.__initial_stroke_path_effect = self.__entity.style.stroke_paint.refPathEffect()
        trim_path_effect = skia.TrimPathEffect.Make(0, 0)
        self.__entity.style.fill_paint.setPathEffect(trim_path_effect)
        self.__entity.style.stroke_paint.setPathEffect(trim_path_effect)

    def update(self, t: float) -> None:
        trim_path_effect = skia.TrimPathEffect.Make(0, t)
        _add_path_effect(self.__entity.style.fill_paint, self.__initial_fill_path_effect, trim_path_effect)
        _add_path_effect(self.__entity.style.stroke_paint, self.__initial_stroke_path_effect, trim_path_effect)

    def end(self) -> None:
        self.__entity.style.fill_paint.setPathEffect(self.__initial_fill_path_effect)
        self.__entity.style.stroke_paint.setPathEffect(self.__initial_stroke_path_effect)
