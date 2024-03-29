from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Tuple

from animator import skia


@dataclass
class Affine:
    originX: float = 0
    originY: float = 0
    translateX: float = 0
    translateY: float = 0
    scaleX: float = 1
    scaleY: float = 1
    rotation: float = 0
    skewX: float = 0
    skewY: float = 0


AFFINE_FIELDS = set(Affine.__dataclass_fields__.keys())


class Transformation(Affine):
    """A convenience class for holding the affine parts of a transformation matrix. This binds to an entity's
    transformation matrix and controls it. These values does not update when the matrix updates (to manually update,
    call :meth:`set_from_mat`), however changing these values updates the matrix.

    :ivar originX: The x-coordinate of the origin along which the transformations are applied.
    :ivar originY: The y-coordinate of the origin along which the transformations are applied.
    :ivar translateX: The x-translation of the transformation.
    :ivar translateY: The y-translation of the transformation.
    :ivar scaleX: The x-scale of the transformation.
    :ivar scaleY: The y-scale of the transformation.
    :ivar rotation: The angle of the rotation of the transformation in degrees.
    :ivar skewX: The angle of the x-skew of the transformation in degrees.
    :ivar skewY: The angle of the y-skew of the transformation in degrees.
    """

    def __init__(self, mat: skia.Matrix) -> None:
        self._mat: skia.Matrix = mat
        self.__do_update: bool = True

    @property
    def scale(self) -> float:
        """
        The uniform scale of the transformation. If :attr:`scaleX` and :attr:`scaleY` are different, this is the
        geometric mean of the two and might cause strange results.
        """
        return math.sqrt(self.scaleX * self.scaleY)

    @scale.setter
    def scale(self, value: float) -> None:
        self.__do_update = False
        self.scaleX = self.scaleY = value
        self._update_mat()
        self.__do_update = True

    def set_from_kwargs(self, **kwargs: Any) -> None:
        """Set the transformation from arguments. Supported arguments are the same as the attributes of this class."""
        self.__do_update = False
        has_updated = False
        for key, value in kwargs.items():
            if hasattr(self, key) and not callable(getattr(self, key)) and not key.startswith("_"):
                setattr(self, key, value)
                has_updated = True
        if has_updated:
            self._update_mat()
        self.__do_update = True

    @staticmethod
    def decompose_mat(
        scale_x: float,
        skew_x: float,
        translate_x: float,
        skew_y: float,
        scale_y: float,
        translate_y: float,
    ) -> Tuple[float, float, float, float, float, float]:
        """Decompose the transformation matrix into its affine parts and returns them. Angles are in degrees.

        :return: A tuple containing (scale, rotation, skewX, skewY, translateX, translateY).
        """
        s = scale_x - scale_y
        c = skew_x + skew_y
        v1 = skew_x * scale_y + scale_x * skew_y
        v2 = skew_x * skew_y - scale_x * scale_y
        if s == c == 0:  # if this is true then v1 == 0 and v2 <= 0
            scale = math.sqrt(-v2)
            rotation = math.atan2(skew_y, scale_x)
        else:
            scale = v1 / math.sqrt(c * c + s * s)
            rotation = math.atan2(s, c)
        return (
            scale,
            math.degrees(rotation),
            math.degrees(math.atan2(scale_x * scale_x + skew_x * skew_x + v2, v1)),  # skewX
            math.degrees(math.atan2(skew_y * skew_y + scale_y * scale_y + v2, v1)),  # skewY
            (translate_y * skew_x - translate_x * scale_y) / v2,  # translateX
            (translate_x * skew_y - translate_y * scale_x) / v2,  # translateY
        )

    def set_from_mat(self) -> None:
        """Set the affine parts of this transformation from the transformation matrix of the entity."""
        self.originX = self.originY = 0
        (
            self.scaleX,
            self.rotation,
            self.skewX,
            self.skewY,
            self.translateX,
            self.translateY,
        ) = Transformation.decompose_mat(*self._mat.get9()[:6])
        self.scaleY = self.scaleX

    def _update_mat(self) -> None:
        """Update the transformation matrix of the entity."""
        # origin -> translate -> rotation -> skew -> scale
        rad = math.radians(self.rotation)
        cr = math.cos(rad)
        sr = math.sin(rad)
        kx = math.tan(math.radians(self.skewX))
        ky = math.tan(math.radians(self.skewY))

        mat = self._mat
        mat[0] = xx = cr * self.scaleX + kx * self.scaleY * sr
        mat[3] = yx = cr * self.scaleX * ky + self.scaleY * sr
        mat[1] = xy = cr * self.scaleY * kx - self.scaleX * sr
        mat[4] = yy = cr * self.scaleY - ky * self.scaleX * sr
        mat[2] = self.originX * (1 - xx) - self.originY * xy + self.translateX * xx + self.translateY * xy
        mat[5] = self.originY * (1 - yy) - self.originX * yx + self.translateX * yx + self.translateY * yy
        mat.dirtyMatrixTypeCache()

    def __setattr__(self, name: str, value: Any) -> None:
        old_value = getattr(self, name, None)
        super().__setattr__(name, value)
        if name in AFFINE_FIELDS and self.__do_update and value != old_value:
            self._update_mat()

    def __str__(self) -> str:
        return (
            f'Transformation(origin=({self.originX}, {self.originY}), '
            f'translate=({self.translateX}, {self.translateY}), scale=({self.scaleX}, {self.scaleY}), '
            f'rotation={self.rotation}, skew=({self.skewX}, {self.skewY}))'
        )
