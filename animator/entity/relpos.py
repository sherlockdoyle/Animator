"""Contains relative positioning used by entities."""
__all__ = 'LEFT', 'RIGHT', 'TOP', 'BOTTOM', 'CENTER', 'TL', 'TR', 'BL', 'BR'

import numpy

# Relative positions
LEFT = numpy.array([-1, 0])
RIGHT = numpy.array([1, 0])
TOP = numpy.array([0, -1])
BOTTOM = numpy.array([0, 1])
CENTER = numpy.array([0, 0])
TL = TOP + LEFT
TR = TOP + RIGHT
BL = BOTTOM + LEFT
BR = BOTTOM + RIGHT

LEFT.flags.writeable = False
RIGHT.flags.writeable = False
TOP.flags.writeable = False
BOTTOM.flags.writeable = False
CENTER.flags.writeable = False
TL.flags.writeable = False
TR.flags.writeable = False
BL.flags.writeable = False
BR.flags.writeable = False
