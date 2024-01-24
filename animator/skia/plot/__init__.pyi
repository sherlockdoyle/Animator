"""
This module provides alternate to functions that allows buufers to be used. Class methods of the form ``Class.method``
have alternate implementations as ``Class_method`` that take a buffer as some of it's arguments.
"""
from __future__ import annotations

import numpy

import animator.skia

__all__ = ['Canvas_drawPoints', 'Point_Polygon']

def Canvas_drawPoints(
    canvas: animator.skia.Canvas,
    mode: animator.skia.Canvas.PointMode,
    pts: numpy.ndarray,
    matrix: animator.skia.Matrix,
    paint: animator.skia.Paint,
) -> None:
    """
    Draw points, *pts*, with the specified *mode* and *paint* after transforming by *matrix*.
    """

def Point_Polygon(
    points: numpy.ndarray,
    isClosed: bool,
    ft: animator.skia.PathFillType = animator.skia.PathFillType.kWinding,
    isVolatile: bool = False,
) -> animator.skia.Path: ...
