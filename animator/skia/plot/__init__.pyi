"""
This module provides alternate to functions that allows numpy arrays to be used for the plot related entities. Class
methods of the form ``Class.method`` have alternate implementations as ``Class_method`` that take a numpy array as some
of it's arguments.
"""

from __future__ import annotations

import numpy

import animator.skia

__all__ = ['Canvas_drawPoints', 'Path_Polygon', 'Vertices__init__']

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

def Path_Polygon(
    points: numpy.ndarray,
    isClosed: bool,
    ft: animator.skia.PathFillType = animator.skia.PathFillType.kWinding,
    isVolatile: bool = False,
) -> animator.skia.Path: ...
def Vertices__init__(positions: numpy.ndarray, colors: numpy.ndarray) -> animator.skia.Vertices:
    """
    Constructs a vertices with the specified *positions* and *colors* (array of Color4f).
    """
