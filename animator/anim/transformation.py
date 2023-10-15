from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

import numpy as np

from animator import skia
from animator.anim.anim import Anim
from animator.entity.transformation import Transformation

if TYPE_CHECKING:
    from animator.entity import Entity

    T6 = tuple[float, float, float, float, float, float]


def _recompose_mat(
    rotation: float, skewX: float, scaleX: float, scaleY: float, translateX: float, translateY: float
) -> T6:
    cr = math.cos(rotation)
    sr = math.sin(rotation)
    kx = math.tan(skewX)
    yx = sr * scaleY
    yy = cr * scaleY

    return (
        xx := kx * yx + cr * scaleX,
        xy := kx * yy - sr * scaleX,
        translateX * xx + translateY * xy,
        yx,
        yy,
        translateX * yx + translateY * yy,
    )


class Transform(Anim):
    """
    Animate the transformation of an entity. This is done by decomposing the transformation matrix into its components
    and animating each component individually.
    """

    def __init__(self, entity: Entity, mat: skia.Matrix, duration: float, **kwargs: Any):
        """
        :param entity: The entity to animate the transformation of.
        :param mat: The target transformation matrix.
        """
        super().__init__(duration, **kwargs)
        self._entity: Entity = entity

        self._initial_affine: T6 = None  # type: ignore lateinit
        self._initial_p0: float = None  # type: ignore lateinit
        self._initial_p1: float = None  # type: ignore lateinit

        mat.normalizePerspective()
        self._target_mat = mat
        target_comp = mat.get9()
        self._target_affine: T6 = Transformation.decompose_mat(*target_comp[:6])
        self._target_p0: float = target_comp[6]
        self._target_p1: float = target_comp[7]

        self._diff_affine: T6 = None  # type: ignore lateinit
        self._diff_p0: float = None  # type: ignore lateinit
        self._diff_p1: float = None  # type: ignore lateinit

    def start(self) -> None:
        initial_mat = self._entity.mat
        initial_mat.normalizePerspective()
        initial_comp = initial_mat.get9()
        self._initial_affine = Transformation.decompose_mat(*initial_comp[:6])
        self._initial_p0 = initial_comp[6]
        self._initial_p1 = initial_comp[7]

        self._diff_affine = tuple(t - i for t, i in zip(self._target_affine, self._initial_affine))
        self._diff_p0 = self._target_p0 - self._initial_p0
        self._diff_p1 = self._target_p1 - self._initial_p1

    def update(self, t: float) -> None:
        self._entity.mat.setAll(
            *_recompose_mat(*(i + d * t for i, d in zip(self._initial_affine, self._diff_affine))),
            self._initial_p0 + self._diff_p0 * t,
            self._initial_p1 + self._diff_p1 * t,
            1,
        )

    def end(self) -> None:
        self._entity.mat.setFromMatrix(self._target_mat)


try:
    from scipy.linalg import fractional_matrix_power
except ImportError:
    pass


class Transform_Pow(Anim):
    """
    Animate the transformation of an entity. This is done by using the formula: :math:`R_t = (R_1(R_0)^{-1})^tR_0`. This
    requires the ``scipy`` package.
    """

    def __init__(self, entity: Entity, mat: skia.Matrix, duration: float, **kwargs: Any):
        """
        :param entity: The entity to animate the transformation of.
        :param mat: The target transformation matrix.
        """
        super().__init__(duration, **kwargs)
        self._entity: Entity = entity

        self._initial_array: np.ndarray = None  # type: ignore lateinit
        self._target_mat: skia.Matrix = mat
        self._pow_array: np.ndarray = None  # type: ignore lateinit

    def start(self) -> None:
        self._initial_array = np.array(self._entity.mat.get9()).reshape((3, 3))
        self._pow_array = np.array(self._target_mat.get9()).reshape((3, 3)) @ np.linalg.inv(self._initial_array)

    def update(self, t: float) -> None:
        self._entity.mat.set9((fractional_matrix_power(self._pow_array, t) @ self._initial_array).flatten().real)  # type: ignore array is sequence
        # TODO: Figure out how to properly handle complex matrices

    def end(self) -> None:
        self._entity.mat.setFromMatrix(self._target_mat)
