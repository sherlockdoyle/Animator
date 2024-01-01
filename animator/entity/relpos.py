"""Contains relative positioning used by entities."""
from typing import Final

import numpy

RelativePosition = Final[numpy.ndarray]

# Relative positions
LEFT: RelativePosition = numpy.array([-1, 0])
RIGHT: RelativePosition = numpy.array([1, 0])
TOP: RelativePosition = numpy.array([0, -1])
BOTTOM: RelativePosition = numpy.array([0, 1])
CENTER: RelativePosition = numpy.array([0, 0])
TL: RelativePosition = TOP + LEFT
TR: RelativePosition = TOP + RIGHT
BL: RelativePosition = BOTTOM + LEFT
BR: RelativePosition = BOTTOM + RIGHT

LEFT.flags.writeable = False
RIGHT.flags.writeable = False
TOP.flags.writeable = False
BOTTOM.flags.writeable = False
CENTER.flags.writeable = False
TL.flags.writeable = False
TR.flags.writeable = False
BL.flags.writeable = False
BR.flags.writeable = False


def rp(x: float, y: float) -> RelativePosition:
    """Returns a relative position with the given *x* and *y* values."""
    rp = numpy.array([x, y])
    rp.flags.writeable = False
    return rp
