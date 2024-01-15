from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, TypeVar

from animator import skia
from animator._common_types import PointLike
from animator.anim.anim import Anim
from animator.entity import Entity
from animator.entity.relpos import RelativePosition

if TYPE_CHECKING:
    from animator.entity import Entity

    CT = TypeVar('CT', bound='Move')


class Move(Anim):
    """Animates the position of an entity."""

    def __init__(
        self,
        entity: Entity,
        duration: float,
        to: PointLike | None = None,
        by: PointLike | None = None,
        rel_to: Entity | None = None,
        rel_pos: RelativePosition | None = None,
        rel_anchor: RelativePosition | None = None,
        rel_padding: float = 25,
        **kwargs: Any,
    ) -> None:
        """
        Moves an entity from its current position to a new position. Exactly one of *to*, *by* or all of *rel_to*,
        *rel_pos* and *rel_anchor* must be specified.

        :param entity: The entity to move.
        :param duration: The duration of the animation.
        :param to: The destination of the entity.
        :param by: The offset to move the entity by.
        :param rel_to: The entity to move relative to.
        :param rel_pos: The position of the entity relative to *rel_to*, a 2 element numpy array [x, y]. The coordinates
            are between -1 and 1, where -1 is the left/top of the entity and 1 is the right/bottom of the entity.
        :param rel_anchor: The anchor point of the entity in relative coordinates, which will be positioned at
            *rel_pos*. If ``None``, it'll be same as -*rel_pos*.
        :param rel_padding: The extra space around the entity, in pixels.
        """
        super().__init__(duration, **kwargs)
        self._entity: Entity = entity

        to_None = to is None
        by_None = by is None
        rel_None = rel_to is None or rel_pos is None
        if to_None + by_None + rel_None != 2:
            raise ValueError('Exactly one of to, by, or all of rel_to, rel_pos, and rel_anchor must be defined.')

        self.__to: PointLike | None = to
        self.__by: PointLike | None = by
        self.__rel_to: Entity | None = rel_to
        self.__rel_pos: RelativePosition | None = rel_pos
        self.__rel_anchor: RelativePosition | None = rel_anchor
        self.__rel_padding: float = rel_padding

        self._initial_pos: skia.Point = None  # type: ignore lateinit
        self.__target_pos: skia.Point = None  # type: ignore lateinit
        self._diff_pos: skia.Point = None  # type: ignore lateinit

    @classmethod
    def to(cls: type[CT], entity: Entity, to: PointLike, duration: float, **kwargs: Any) -> CT:
        """Move an *entity* *to* a new position."""
        return cls(entity, duration, to=to, **kwargs)

    @classmethod
    def by(cls: type[CT], entity: Entity, by: PointLike, duration: float, **kwargs: Any) -> CT:
        """Move an *entity* *by* some offset."""
        return cls(entity, duration, by=by, **kwargs)

    @classmethod
    def relative_to(
        cls: type[CT],
        entity: Entity,
        relative_to: Entity,
        pos: RelativePosition,
        duration: float,
        anchor: RelativePosition | None = None,
        padding: float = 25,
        **kwargs: Any,
    ) -> CT:
        """
        Move an *entity* relative to another entity (*relative_to*) and position it at *pos* by *anchor*, with some
        optional *padding*.
        """
        return cls(entity, duration, rel_to=relative_to, rel_pos=pos, rel_anchor=anchor, rel_padding=padding, **kwargs)

    def start(self) -> None:
        self._initial_pos = skia.Point(*self._entity.pos)
        if self.__to is not None:
            self.__target_pos = skia.Point(*self.__to)
        elif self.__by is not None:
            self.__target_pos = self._initial_pos + skia.Point(*self.__by)
        else:
            self.__target_pos = self._entity.get_pos_relative_to_entity(
                self.__rel_to, self.__rel_pos, self.__rel_anchor, self.__rel_padding  # type: ignore already checked for None
            )
        self._diff_pos = self.__target_pos - self._initial_pos

    def update(self, t: float) -> None:
        self._entity.pos.set(*(self._initial_pos + self._diff_pos * t))

    def end(self) -> None:
        self._entity.pos.set(*self.__target_pos)


SQRT2 = math.sqrt(2)


class ArcMove(Move):
    def update(self, t: float) -> None:
        dx, dy = self._diff_pos
        a = math.atan2(dy, dx)
        cos_a = math.cos(a)
        sin_a = math.sin(a)
        z = math.sqrt(1 - (t - 1) ** 2)  # height of a quarter circle
        x = (t + z) / 2
        y = (t - z) / SQRT2
        r = math.hypot(dx, dy)
        self._entity.pos.set(
            self._initial_pos.fX + (cos_a * x + sin_a * y) * r, self._initial_pos.fY + (sin_a * x - cos_a * y) * r
        )
