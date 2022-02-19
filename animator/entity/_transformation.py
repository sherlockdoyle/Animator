from __future__ import annotations

import math
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from .entity import Entity


class Transformation:
    """A convenience class for holding the affine parts of a transformation matrix. This binds to an *entity* and
    controls its transformation matrix. These values does not update when the entity's matrix updates (to manually
    update, call :meth:`set_from_mat`), however changing these values updates the matrix.

    :ivar originX: The x-coordinate of the origin along which the transformations are applied.
    :ivar originY: The y-coordinate of the origin along which the transformations are applied.
    :ivar translateX: The x-translation of the transformation.
    :ivar translateY: The y-translation of the transformation.
    :ivar scale: The uniform scale of the transformation.
    :ivar scaleX: The x-scale of the transformation.
    :ivar scaleY: The y-scale of the transformation.
    :ivar rotation: The angle of the rotation of the transformation in degrees.
    :ivar skewX: The angle of the x-skew of the transformation in degrees.
    :ivar skewY: The angle of the y-skew of the transformation in degrees.
    """

    def __init__(self, entity: Entity) -> None:
        self.__update = False
        self._entity: Entity = entity
        self.originX: float = 0
        self.originY: float = 0
        self.translateX: float = 0
        self.translateY: float = 0
        self.scaleX: float = 1
        self.scaleY: float = 1
        self.rotation: float = 0
        self.skewX: float = 0
        self.skewY: float = 0
        self.__update = True

    @staticmethod
    def decompose_mat(scale_x: float, skew_x: float, translate_x: float, skew_y: float, scale_y: float,
                      translate_y: float) -> Tuple[float, float, float, float, float, float]:
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
        return (scale, math.degrees(rotation),
                math.degrees(math.atan2(scale_x * scale_x + skew_x * skew_x + v2, v1)),  # skewX
                math.degrees(math.atan2(skew_y * skew_y + scale_y * scale_y + v2, v1)),  # skewY
                (translate_y * skew_x - translate_x * scale_y) / v2,  # translateX
                (translate_x * skew_y - translate_y * scale_x) / v2)  # translateY

    def set_from_mat(self) -> None:
        """Set the affine parts of this transformation from the transformation matrix of the entity."""
        self.__update = False
        self.originX = self.originY = 0
        self.scaleX, self.rotation, self.skewX, self.skewY, self.translateX, self.translateY = Transformation.decompose_mat(
            *self._entity.mat.get9()[:6])
        self.scaleY = self.scaleX
        self.__update = True

    def __setattr__(self, key: str, value: float) -> None:
        """Set an affine part of this transformation and update the transformation matrix of the entity."""
        if key == 'scale':
            self.__update = False
            super().__setattr__('scaleX', value)
            super().__setattr__('scaleY', value)
            self.__update = True
        elif key == 'rotation':
            super().__setattr__('rotation', value % 360)
        else:
            super().__setattr__(key, value)

        if self.__update:  # origin -> translate -> rotation -> skew -> scale
            cr = math.cos(math.radians(self.rotation))
            sr = math.sin(math.radians(self.rotation))
            kx = math.tan(math.radians(self.skewX))
            ky = math.tan(math.radians(self.skewY))

            mat = self._entity.mat
            mat[0] = xx = cr * self.scaleX + kx * self.scaleY * sr
            mat[3] = yx = cr * self.scaleX * ky + self.scaleY * sr
            mat[1] = xy = cr * self.scaleY * kx - self.scaleX * sr
            mat[4] = yy = cr * self.scaleY - ky * self.scaleX * sr
            mat[2] = self.originX * (1 - xx) - self.originY * xy + self.translateX * xx + self.translateY * xy
            mat[5] = self.originY * (1 - yy) - self.originX * yx + self.translateX * yx + self.translateY * yy
            mat.dirtyMatrixTypeCache()

    def __str__(self) -> str:
        return f'Transformation(origin=({self.originX}, {self.originY}), ' \
               f'translate=({self.translateX}, {self.translateY}), scale=({self.scaleX}, {self.scaleY}), ' \
               f'rotation={self.rotation}, skew=({self.skewX}, {self.skewY}))'
