"""More types of path based entities."""
import math
from typing import Any

from animator import skia
from animator._common_types import PointLike
from animator.entity.path import PathEntity


class Ring(PathEntity):
    _observed_attrs = {'r0', 'r1'}

    def __init__(self, r0: float, r1: float, **kwargs: Any) -> None:
        """
        :param r0: Outer radius of the ring.
        :param r1: Inner radius of the ring.
        """
        super().__init__(**kwargs)
        self.r0 = r0
        self.r1 = r1

    def on_build_path(self) -> None:
        self.path.addCircle(0, 0, self.r0, skia.PathDirection.kCW)
        self.path.addCircle(0, 0, self.r1, skia.PathDirection.kCCW)


class Arrow(PathEntity):
    _observed_attrs = {'to', 'from_', 'arrow_head_size'}

    def __init__(
        self,
        to: PointLike,
        from_: PointLike = (0, 0),
        arrow_head_size: float | None = None,
        pos: PointLike = (0, 0),
        **kwargs: Any
    ) -> None:
        """
        :param to: The point to draw the arrow to.
        :param from_: The point to draw the arrow from.
        :param arrow_head_size: The size of the arrow head. If ``None``, it'll be set from the ``stroke_width``.
        """
        super().__init__(pos=pos, **kwargs)
        self.to: skia.Point = skia.Point(*to)
        self.from_: skia.Point = skia.Point(*from_)
        self.arrow_head_size: float = self.style.stroke_width * 2 if arrow_head_size is None else arrow_head_size

    def on_build_path(self) -> None:
        self.path.moveTo(self.from_)
        self.path.lineTo(self.to)

        angle = math.atan2(self.to.fY - self.from_.fY, self.to.fX - self.from_.fX)
        sa = math.sin(angle)
        ca = math.cos(angle)
        dx = -self.arrow_head_size * (ca + sa)
        dy = self.arrow_head_size * (ca - sa)
        self.path.rMoveTo(dx, dy)
        self.path.lineTo(self.to)
        self.path.rLineTo(-dy, dx)
