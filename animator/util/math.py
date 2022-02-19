"""Mathematical functions."""
from __future__ import annotations

from typing import TYPE_CHECKING

import math
from .. import skia

if TYPE_CHECKING:
    from .._common_types import Point


def rotate_x(degrees: float, perspective: float = 0.0009765625) -> skia.Matrix:
    """Create a perspective matrix that simulates a rotation around the X axis.

    :param degrees: The angle of rotation in degrees.
    :param perspective: Amount of perspective of the rotation.
    :return: The rotation matrix.
    """
    radians = math.radians(degrees)
    return skia.Matrix().setAll(1, 0, 0, 0, math.cos(radians), 0, 0, -math.sin(radians) * perspective, 1)


def rotate_y(degrees: float, perspective: float = 0.0009765625) -> skia.Matrix:
    """Create a perspective matrix that simulates a rotation around the Y axis.

    :param degrees: The angle of rotation in degrees.
    :param perspective: Amount of perspective of the rotation.
    :return: The rotation matrix.
    """
    radians = math.radians(degrees)
    return skia.Matrix().setAll(math.cos(radians), 0, 0, 0, 1, 0, math.sin(radians) * perspective, 0, 1)


def rotate_3d(degrees: float, vector: Point | skia.Point, perspective: float = 0.0009765625) -> skia.Matrix:
    """Create a perspective matrix that simulates a rotation around a vector lying in the XY plane.

    :param degrees: The angle of rotation in degrees.
    :param vector: The vector to rotate around.
    :param perspective: Amount of perspective of the rotation.
    :return: The rotation matrix.
    """
    vector: skia.Point = skia.Point(*vector)
    vector.normalize()
    cv, sv = vector
    cv2, sv2 = cv * cv, sv * sv
    radians = math.radians(degrees)
    sr = math.sin(radians) * perspective
    cr = math.cos(radians)
    return skia.Matrix().setAll(
        cv2 + cr * sv2, cv * sv * (1 - cr), 0,
        cv * sv * (1 - cr), sv2 + cr * cv2, 0,
        sr * sv, -cv * sr, 1
    )
