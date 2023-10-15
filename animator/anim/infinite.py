from __future__ import annotations

from typing import TYPE_CHECKING

from animator.anim.anim import Anim

if TYPE_CHECKING:
    from animator.entity import Entity


class Rotating(Anim):
    """Rotates an entity at a constant rate forever."""

    def __init__(self, entity: Entity, rate: float) -> None:
        """
        :param entity: The entity to rotate.
        :param rate: The rate of rotation in degrees per second.
        """
        super().__init__(Anim.Duration.INFINITE)
        self._entity: Entity = entity
        self._rate: float = rate

    def start(self) -> None:
        self._rate /= self._scene.fps

    def update(self, t: float) -> None:
        self._entity.transformation.rotation += self._rate


class Scaling(Anim):
    """Scales an entity at a constant rate forever."""

    def __init__(self, entity: Entity, rateX: float, rateY: float | None = None) -> None:
        """
        :param entity: The entity to scale.
        :param rateX: The rate of scaling in the x direction.
        :param rateY: The rate of scaling in the y direction. If None, defaults to rateX.
        """
        super().__init__(Anim.Duration.INFINITE)
        self._entity: Entity = entity
        self._rateX: float = rateX
        self._rateY: float = rateX if rateY is None else rateY

    def start(self) -> None:
        self._rateX /= self._scene.fps
        self._rateY /= self._scene.fps

    def update(self, t: float) -> None:
        self._entity.transformation._do_update = False
        self._entity.transformation.scaleX += self._rateX
        self._entity.transformation.scaleY += self._rateY
        self._entity.transformation._update_mat()
        self._entity.transformation._do_update = True


class Skewing(Anim):
    """Skews an entity at a constant rate forever."""

    def __init__(self, entity: Entity, rateX: float, rateY: float) -> None:
        """
        :param entity: The entity to skew.
        :param rateX: The rate of skewing in the x direction in degrees per second.
        :param rateY: The rate of skewing in the y direction in degrees per second.
        """
        super().__init__(Anim.Duration.INFINITE)
        self._entity: Entity = entity
        self._rateX: float = rateX
        self._rateY: float = rateY

    def start(self) -> None:
        self._rateX /= self._scene.fps
        self._rateY /= self._scene.fps

    def update(self, t: float) -> None:
        self._entity.transformation._do_update = False
        self._entity.transformation.skewX += self._rateX
        self._entity.transformation.skewY += self._rateY
        self._entity.transformation._update_mat()
        self._entity.transformation._do_update = True


class Translating(Anim):
    """Translates an entity at a constant rate forever."""

    def __init__(self, entity: Entity, rateX: float, rateY: float) -> None:
        """
        :param entity: The entity to translate.
        :param rateX: The rate of translation in the x direction.
        :param rateY: The rate of translation in the y direction.
        """
        super().__init__(Anim.Duration.INFINITE)
        self._entity: Entity = entity
        self._rateX: float = rateX
        self._rateY: float = rateY

    def start(self) -> None:
        self._rateX /= self._scene.fps
        self._rateY /= self._scene.fps

    def update(self, t: float) -> None:
        self._entity.transformation._do_update = False
        self._entity.transformation.translateX += self._rateX
        self._entity.transformation.translateY += self._rateY
        self._entity.transformation._update_mat()
        self._entity.transformation._do_update = True


class Moving(Anim):
    """Keeps an entity moving at a constant rate forever."""

    def __init__(self, entity: Entity, rateX: float, rateY: float) -> None:
        """
        :param entity: The entity to move.
        :param rateX: The rate of movement in the x direction.
        :param rateY: The rate of movement in the y direction.
        """
        super().__init__(Anim.Duration.INFINITE)
        self._entity: Entity = entity
        self._rateX: float = rateX
        self._rateY: float = rateY

    def start(self) -> None:
        self._rateX /= self._scene.fps
        self._rateY /= self._scene.fps

    def update(self, t: float) -> None:
        self._entity.pos.offset(self._rateX, self._rateY)


class Bouncing(Anim):
    """Keeps an entity bouncing to the edge of the scene forever."""

    def __init__(self, entity: Entity, rateX: float, rateY: float) -> None:
        """
        :param entity: The entity to bounce.
        :param rateX: The rate of movement in the x direction.
        :param rateY: The rate of movement in the y direction.
        """
        super().__init__(Anim.Duration.INFINITE)
        self._entity: Entity = entity
        self._rateX: float = rateX
        self._rateY: float = rateY

    def start(self) -> None:
        self._rateX /= self._scene.fps
        self._rateY /= self._scene.fps

    def update(self, t: float) -> None:
        self._entity.pos.offset(self._rateX, self._rateY)
        bounds = self._entity.get_bounds(True)
        bounds.offset(self._entity.pos)
        if bounds.fLeft < 0:
            self._rateX = abs(self._rateX)
        elif bounds.fRight > self._scene.width:
            self._rateX = -abs(self._rateX)
        if bounds.fTop < 0:
            self._rateY = abs(self._rateY)
        elif bounds.fBottom > self._scene.height:
            self._rateY = -abs(self._rateY)
