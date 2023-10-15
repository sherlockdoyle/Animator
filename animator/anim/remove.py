"""Remove an entity from the scene. These are the opposite of the creation animations."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from animator import skia
from animator.anim.anim import Anim
from animator.anim.create import _add_path_effect
from animator.entity import relpos
from animator.entity.relpos import RelativePosition

if TYPE_CHECKING:
    from animator.entity import Entity


class FadeOut(Anim):
    """Fades out an entity. Effects ``style.opacity``."""

    def __init__(self, entity: Entity, duration: float, **kwargs: Any) -> None:
        super().__init__(duration, **kwargs)
        self.__entity: Entity = entity
        self.__initial_opacity: float = None  # type: ignore lateinit

    def start(self) -> None:
        self.__initial_opacity = self.__entity.style.opacity

    def update(self, t: float) -> None:
        self.__entity.style.opacity = self.__initial_opacity * (1 - t)

    def end(self) -> None:
        self.__entity._remove()


class SlideOut(Anim):
    """Slides out an entity from the scene. Effects ``pos``."""

    def __init__(
        self, entity: Entity, duration: float, dir: RelativePosition = relpos.RIGHT, padding: float = 25, **kwargs: Any
    ) -> None:
        """
        :param entity: The entity to slide out.
        :param duration: Duration of the animation.
        :param dir: Relative direction to slide out to. +-1 represents the extreme, just outside the scene. Other values
            will scale this distance.
        :param padding: Extra padding to add around the scene.
        """
        super().__init__(duration, **kwargs)
        self.__entity: Entity = entity
        self.__dir: RelativePosition = dir
        self.__padding: float = padding
        self.__initial_pos: skia.Point = None  # type: ignore lateinit
        self.__diff_pos: skia.Point = None  # type: ignore lateinit

    def start(self) -> None:
        self.__initial_pos = skia.Point(*self.__entity.pos)
        bounds = self.__entity.get_bounds(True)
        dx = (
            self.__initial_pos.fX + bounds.right()
            if self.__dir[0] < 0
            else self._scene.width - self.__initial_pos.fX - bounds.left()
        )
        dy = (
            self.__initial_pos.fY + bounds.bottom()
            if self.__dir[1] < 0
            else self._scene.height - self.__initial_pos.fY - bounds.top()
        )
        self.__diff_pos = skia.Point(self.__dir[0] * (dx + self.__padding), self.__dir[1] * (dy + self.__padding))

    def update(self, t: float) -> None:
        self.__entity.pos.set(*(self.__initial_pos + self.__diff_pos * t))

    def end(self) -> None:
        self.__entity._remove()


class ScaleOut(Anim):
    """Scales out an entity. Effects ``transformation.scaleX`` and ``transformation.scaleY``."""

    def __init__(self, entity: Entity, duration: float, **kwargs: Any) -> None:
        super().__init__(duration, **kwargs)
        self.__entity: Entity = entity
        self.__initial_scaleX: float = None  # type: ignore lateinit
        self.__initial_scaleY: float = None  # type: ignore lateinit

    def start(self) -> None:
        self.__initial_scaleX = self.__entity.transformation.scaleX
        self.__initial_scaleY = self.__entity.transformation.scaleY

    def update(self, t: float) -> None:
        t = 1 - t
        self.__entity.transformation.scaleX = self.__initial_scaleX * t
        self.__entity.transformation.scaleY = self.__initial_scaleY * t

    def end(self) -> None:
        self.__entity._remove()


class DrawOut(Anim):
    """Draws out an entity (preferably a :class:`PathEntity`). Effects the entity's fill and stroke path effect."""

    def __init__(self, entity: Entity, duration: float, **kwargs: Any) -> None:
        super().__init__(duration, **kwargs)
        self.__entity: Entity = entity
        self.__initial_fill_path_effect: skia.PathEffect | None = None
        self.__initial_stroke_path_effect: skia.PathEffect | None = None

    def start(self) -> None:
        self.__initial_fill_path_effect = self.__entity.style.fill_paint.refPathEffect()
        self.__initial_stroke_path_effect = self.__entity.style.stroke_paint.refPathEffect()

    def update(self, t: float) -> None:
        trim_path_effect = skia.TrimPathEffect.Make(t, 1)
        _add_path_effect(self.__entity.style.fill_paint, self.__initial_fill_path_effect, trim_path_effect)
        _add_path_effect(self.__entity.style.stroke_paint, self.__initial_stroke_path_effect, trim_path_effect)

    def end(self) -> None:
        self.__entity._remove()
