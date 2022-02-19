"""The processing module allows for the use of Processing 3 like functions to draw on a scene. Only the 2D drawing
functions are implemented, that too with some changes. This is not intended to be a processing alternative. To write
Processing code in Python, check `Python Mode for Processing <https://py.processing.org/>`_. To keep things Pythonic
while supporting the style of Processing, several small changes have been made. Internally, this module uses ``cv2``
for displaying the scene and handling keyboard and mouse events. The sketch window is not resizeable.

In Processing, your code starts from ``void setup()``. Here, however, there's no setup function. Instead,
your code must start with :func:`size`, which will setup the internal scene and canvas. You must write the code you
want to execute repeatedly (animations) inside a function and pass that to :func:`draw`. All the enums, as used in
Processing, are also available. These include

====== ======= ====== =======
RADIUS CENTER  CORNER CORNERS
SQUARE PROJECT ROUND  MITER
BEVEL  RGB     HSB    PIE
OPEN   CHORD   LEFT   RIGHT
====== ======= ====== =======

Processing supports several global(-like) variables that can be used to access information like width and height.
Here, these variables can be accessed as the part of a special variable called ``pvars``. For example, to access the
width, do ``pvars.width``. This can also be used to set up different functions that are called during a keyboard or
mouse event. ``pvars`` contains the following variables:

  * **frameCount** (*default* ``1``): The number of frames already displayed.
  * **frameRate** (*default* ``10``): The moving average of the current frame rate.
  * **width**: Width of the current scene (sketch). Only available after :func:`size` is called.
  * **height**: Height of the current scene (sketch). Only available after :func:`size` is called.
  * **key** (*default* ``''``): The value of the last key pressed. This is basically ``chr(keyCode)``.
  * **keyCode** (*default* ``0``): The key code of the last key pressed. This is basically the 8 least significant bits
    of the key code returned by ``cv2.waitKey()``.
  * **keyPressed_** (*default* ``False``): This is True if any key is kept pressed. Note the underscore at the end.
  * **keyPressed** (*default* ``lambda: None``): This function is called every time a key is pressed. Note that, even if
    a single key is kept pressed, this function will be called once each frame.
  * **mouseButton** (*default* ``0``): The mouse button that is being pressed.
  * **mousePressed_** (*default* ``False``): This is True if any mouse button is kept pressed. Note the underscore at
    the end.
  * **mouseX** (*default* ``0``): The current horizontal position of the mouse inside the scene window.
  * **mouseY** (*default* ``0``): The current vertical position of the mouse inside the scene window.
  * **pmouseX** (*default* ``0``): The last horizontal position of the mouse inside the scene window. This is updated
    once per frame.
  * **pmouseY** (*default* ``0``): The last vertical position of the mouse inside the scene window. This is updated once
    per frame.
  * **mousePressed** (*default* ``lambda: None``): This function is called every time a mouse button is pressed.
  * **mouseReleased** (*default* ``lambda: None``): This function is called every time a mouse button is released.
  * **mouseClicked** (*default* ``lambda: None``): This function is called every time a mouse button is clicked.
  * **mouseWheel** (*default* ``lambda: None``): This function is called every time the mouse wheel or touchpad is
    scrolled.
  * **mouseMoved** (*default* ``lambda: None``): This function is called every time the mouse moves inside the window.
  * **mouseDragged** (*default* ``lambda: None``): This function is called every time the mouse is dragged inside the
    window.

Note that the ``keyPressed`` function is called only once per frame in the same thread in which the drawing loop is
running. This means that any heavy computations inside this function will drop the frame rate. However,
the mouse related functions are called in a separate thread, and possibly multiple times per frame. Do not assign any
of these variables except the functions. To disable an assigned function do not use None, instead use ``lambda: None``.

You may want to read the actual `Processing documentation <https://processing.org/reference/>`_ for more information
about the functions implemented here. Unless otherwise mentioned, the functions behave in the same way as implemented
in Processing.

**Example:** A sample program to draw the path the mouse pointer moves in is shown below.

.. code-block:: python

    from animator.processing import *

    size(500, 500)  # Set the size of the scene (sketch)
    def onMouseClick():
        print(pvars.mouseX, pvars.mouseY)
    def f():
        line(pvars.pmouseX, pvars.pmouseY, pvars.mouseX, pvars.mouseY)

    pvars.mouseClicked = onMouseClick  # Assign the mouse clicked callback
    draw(f)  # Note that draw must be called last

*The same program in Processing (Java mode) would be written as follows.*

.. code-block:: java

    void setup() {
        size(500, 500);
    }
    void draw() {
        line(pmouseX, pmouseY, mouseX, mouseY);
    }
    void mouseClicked() {
        println(mouseX, mouseY);
    }
"""
from __future__ import annotations

__all__ = ('pvars', 'HALF_PI', 'PI', 'QUARTER_PI', 'TAU', 'TWO_PI', 'RADIUS', 'CENTER', 'CORNER', 'CORNERS', 'SQUARE',
           'PROJECT', 'ROUND', 'MITER', 'BEVEL', 'RGB', 'HSB', 'PIE', 'OPEN', 'CHORD', 'LEFT', 'RIGHT', 'size', 'draw',
           'draw_parallel', 'arc', 'circle', 'ellipse', 'line', 'point', 'quad', 'rect', 'square', 'triangle', 'bezier',
           'bezierPoint', 'bezierTangent', 'curve', 'curvePoint', 'curveTangent', 'curveTightness', 'loop', 'noLoop',
           'push', 'pop', 'setTitle', 'delay', 'frameRate', 'smooth', 'noSmooth', 'ellipseMode', 'rectMode',
           'imageMode', 'strokeCap', 'strokeJoin', 'strokeWeight', 'save', 'saveFrame', 'color', 'background',
           'colorMode', 'fill', 'noFill', 'stroke', 'noStroke', 'alpha', 'red', 'green', 'blue', 'hue', 'saturation',
           'brightness', 'lerpColor', 'image', 'imageMode', 'loadImage', 'noTint', 'tint', 'rotate', 'scale',
           'translate', 'constrain', 'dist', 'lerp', 'mag', 'map_', 'norm', 'random', 'noise')

import colorsys
import math
import random as rnd
import time
import types
from typing import Callable, overload, Sequence, Tuple

import cv2

from . import skia
from ._common_types import Color
from .scene import Scene
from .scene.Context2d import Context2d
from .util.env import get_path

__scene: Scene = None
__canvas: skia.Canvas = None
__paint: skia.Paint = skia.Paint(
    StrokeWidth=1,
    StrokeCap=skia.Paint.Cap.kRound_Cap,
    StrokeJoin=skia.Paint.Join.kMiter_Join,
    AntiAlias=True
)
__stroke_color: Color = (0, 0, 0, 1)
__fill_color: Color = (1, 1, 1, 1)
__title: str = 'processing_scene'
__looping: bool = True
__draw_func: Callable[[], None] = None
__frame_wait: int = 14
__last_event = None


class ProcessingVariables(types.SimpleNamespace):
    """A namespace to hold the processing global variables."""
    frameCount: int
    frameRate: float
    width: int
    height: int
    key: str
    keyCode: int
    keyPressed_: bool
    keyPressed: Callable[[], None]
    mouseButton: int
    mousePressed_: bool
    mouseX: float
    mouseY: float
    pmouseX: float
    pmouseY: float
    mousePressed: Callable[[], None]
    mouseReleased: Callable[[], None]
    mouseClicked: Callable[[], None]
    mouseWheel: Callable[[], None]
    mouseMoved: Callable[[], None]
    mouseDragged: Callable[[], None]


pvars = ProcessingVariables(
    frameCount=1,
    frameRate=10,
    key='',
    keyCode=0,
    keyPressed_=False,
    keyPressed=lambda: None,
    mouseButton=0,
    mousePressed_=False,
    mouseX=0,
    mouseY=0,
    pmouseX=0,
    pmouseY=0,
    mousePressed=lambda: None,
    mouseReleased=lambda: None,
    mouseClicked=lambda: None,
    mouseWheel=lambda: None,
    mouseMoved=lambda: None,
    mouseDragged=lambda: None
)
HALF_PI = math.pi / 2
PI = math.pi
QUARTER_PI = math.pi / 4
TAU = 2 * math.pi
TWO_PI = math.pi * 2

RADIUS = 0
CENTER = 1
CORNER = 2
CORNERS = 3
SQUARE = 4
PROJECT = 5
ROUND = 6
MITER = 7
BEVEL = 8
RGB = 9
HSB = 10
PIE = 11
OPEN = 12
CHORD = 13
LEFT = 14
RIGHT = 15

__mouseButton = {cv2.EVENT_LBUTTONDOWN: LEFT, cv2.EVENT_RBUTTONDOWN: RIGHT, cv2.EVENT_MBUTTONDOWN: CENTER}
__stroke_caps = {SQUARE: skia.Paint.Cap.kButt_Cap, PROJECT: skia.Paint.Cap.kSquare_Cap,
                 ROUND: skia.Paint.Cap.kRound_Cap}
__stroke_joins = {MITER: skia.Paint.Join.kMiter_Join, BEVEL: skia.Paint.Join.kBevel_Join,
                  ROUND: skia.Paint.Join.kRound_Join}
__ellipse_mode: int = CENTER
__rect_mode: int = CORNER
__image_mode: int = CORNER
__color_mode: int = RGB
__color_max: Tuple[float, float, float, float] = (255, 255, 255, 255)
__tint: skia.ColorFilter | None = None
__curve_tension: float = 1
__perlin_octave: int = 4
__perlin_amp_falloff: float = 0.5


@overload
def size(scene: Scene) -> None:
    """Initialize the internal scene (it'll be cleared) and set the size of the window."""


@overload
def size(width: int, height: int) -> None:
    """Set the size of the window and initialize the internal scene."""


def size(w: int | Scene = 100, h: int | None = 100) -> None:
    global __scene, __canvas
    __scene = w if isinstance(w, Scene) else Scene(w, h)
    pvars.width = __scene.width
    pvars.height = __scene.height
    __canvas = __scene.canvas
    background(204, 204, 204, 255)


def __onMouse(event, x, y, flags, param):
    global __last_event
    pvars.mouseX, pvars.mouseY = x, y
    pvars.mouseButton = 0
    if event in {cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN, cv2.EVENT_MBUTTONDOWN}:
        pvars.mousePressed_ = True
        pvars.mouseButton = __mouseButton[event]
        pvars.mousePressed()
    elif event in {cv2.EVENT_LBUTTONUP, cv2.EVENT_RBUTTONUP, cv2.EVENT_MBUTTONUP}:
        pvars.mousePressed_ = False
        pvars.mouseReleased()
        if __last_event in {cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN, cv2.EVENT_MBUTTONDOWN}:
            pvars.mouseClicked()
    elif event in {cv2.EVENT_MOUSEWHEEL, cv2.EVENT_MOUSEHWHEEL}:
        pvars.mouseWheel()
    elif event == cv2.EVENT_MOUSEMOVE:
        if pvars.mousePressed_:
            pvars.mouseDragged()
        else:
            pvars.mouseMoved()
    __last_event = event


def __fill_paint() -> skia.Paint:
    p = skia.Paint(__paint)
    p.setColor(skia.Color4f(__fill_color))
    p.setStyle(skia.Paint.kFill_Style)
    return p


def __stroke_paint() -> skia.Paint:
    p = skia.Paint(__paint)
    p.setColor(skia.Color4f(__stroke_color))
    p.setStyle(skia.Paint.kStroke_Style)
    return p


def draw(f: Callable[[], bool | None]) -> None:
    """Continuously calls *f* and updates the scene. f can optionally return True to stop the drawing loop."""
    global __draw_func
    __draw_func = f
    cv2.namedWindow(__title)
    cv2.setMouseCallback(__title, __onMouse)
    start_time = time.time()
    while not f() and __looping:
        pvars.pmouseX, pvars.pmouseY = pvars.mouseX, pvars.mouseY
        cv2.imshow(__title, cv2.cvtColor(__scene.frame, cv2.COLOR_RGBA2BGR))
        key_code = cv2.waitKey(__frame_wait) & 0xff
        pvars.keyPressed_ = key_code != 0xff
        pvars.keyCode, pvars.key = key_code, chr(key_code)
        if key_code != 0xff:
            pvars.keyPressed()
        if key_code == 27 or cv2.getWindowProperty(__title, cv2.WND_PROP_AUTOSIZE) < 0:
            break
        pvars.frameCount += 1
        # Exponential moving average (https://github.com/processing/processing/blob/8e86389c7e017d0e4d61f81fb942c25e3ed348c7/core/src/processing/core/PApplet.java#L2460-L2470)
        pvars.frameRate /= 0.95 + 0.05 * (time.time() - start_time) * pvars.frameRate
        start_time = time.time()
    try:
        cv2.destroyWindow(__title)
    except cv2.error:
        pass
    __draw_func = None


def draw_parallel(f: Callable[[], bool | None]) -> None:
    """Similar to :func:`draw`, but the drawing operations are performed on a separate thread. This is useful in Jupyter
    notebooks where you can update the drawing in real-time.

    :warning: In case of exceptions in Jupyter the kernel will crash.
    """
    import threading
    threading.Thread(target=draw, args=(f,)).start()


def __parse_bound_params(a: float, b: float, c: float, d: float, mode: int) -> skia.Rect:
    if mode == CORNER:
        return skia.Rect.MakeXYWH(a, b, c, d)
    elif mode == CORNERS:
        return skia.Rect.MakeLTRB(a, b, c, d)
    if mode == CENTER:
        return skia.Rect.MakeXYWH(a - c / 2, b - d / 2, c, d)
    if mode == RADIUS:
        return skia.Rect.MakeLTRB(a - c, b - d, a + c, b + d)


def arc(a: float, b: float, c: float, d: float, start: float, stop: float,
        mode: int | Tuple[int, int] = (PIE, OPEN)) -> None:
    """Draws an arc which is part of the :func:`ellipse` defined by a, b, c, d starting from start to stop. mode is a
    tuple of two elements containing the fill and stroke styles respectively. If mode is a single value, that is used
    for both the fill and stroke styles."""
    if not isinstance(mode, tuple):
        mode = (mode, mode)
    bound = __parse_bound_params(a, b, c, d, __ellipse_mode)
    x, y = bound.centerX(), bound.centerY()
    rx, ry = bound.width() / 2, bound.height() / 2
    start = math.degrees(start)
    stop = math.degrees(stop) % 360
    sweep = stop - start

    path = skia.Path().addArc(bound, start, sweep)
    if mode[0] != OPEN:
        if mode[0] == PIE:
            path.lineTo(x, y)
        path.lineTo(x + rx * math.cos(start), y + ry * math.sin(start))
    __canvas.drawPath(path, __fill_paint())
    if mode[0] != mode[1]:
        path.rewind()
        path.addArc(bound, start, sweep)
        if mode[1] == PIE:
            path.lineTo(x, y)
            path.lineTo(x + rx * math.cos(start), y + ry * math.sin(stop))
    __canvas.drawPath(path, __stroke_paint())


def ellipse(a: float, b: float, c: float, d: float) -> None:
    """Draws an ellipse centered (or cornered, depending on :func:`ellipseMode`) at (a, b) and radius (or width and
    height) of c and d."""
    bound = __parse_bound_params(a, b, c, d, __ellipse_mode)
    __canvas.drawOval(bound, __fill_paint())
    __canvas.drawOval(bound, __stroke_paint())


def circle(x: float, y: float, extent: float) -> None:
    """Draws a circle centered (or cornered, depending on :func:`ellipseMode`) at (x, y) and radius (or width/height) of
    extent."""
    ellipse(x, y, extent, extent)


def line(x1: float, y1: float, x2: float, y2: float) -> None:
    """Draws a line from (x1, y1) to (x2, y2)."""
    __canvas.drawLine(x1, y1, x2, y2, __stroke_paint())


def point(x: float, y: float) -> None:
    """Draws a point at (x, y)."""
    __canvas.drawPath(skia.Path().moveTo(x, y).close(), __stroke_paint())


def quad(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float) -> None:
    """Draws a quadrilateral with points (x1, y1), (x2, y2), (x3, y3), (x4, y4)."""
    path = skia.Path().moveTo(x1, y1).lineTo(x2, y2).lineTo(x3, y3).lineTo(x4, y4).close()
    __canvas.drawPath(path, __fill_paint())
    __canvas.drawPath(path, __stroke_paint())


def rect(a: float, b: float, c: float, d: float, tl: float = 0, tr: float | None = None, br: float | None = None,
         bl: float | None = None) -> None:
    """Draws a rectangle centered (or cornered, depending on :func:`rectMode`) at (a, b) and radius (or width and
    height) of c and d. The rectangle can have one or four optional corner radius."""
    if tr is None:
        tr = br = bl = tl
    rrect = skia.RRect()
    rrect.setRectRadii(__parse_bound_params(a, b, c, d, __rect_mode), [(tl, tl), (tr, tr), (br, br), (bl, bl)])
    __canvas.drawRRect(rrect, __fill_paint())
    __canvas.drawRRect(rrect, __stroke_paint())


def square(x: float, y: float, extent: float) -> None:
    """Draws a square centered (or cornered, depending on :func:`rectMode`) at (x, y) and radius (or width/height) of
    extent."""
    rect(x, y, extent, extent)


def triangle(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> None:
    """Draws a triangle with points (x1, y1), (x2, y2), (x3, y3)."""
    path = skia.Path().moveTo(x1, y1).lineTo(x2, y2).lineTo(x3, y3).close()
    __canvas.drawPath(path, __fill_paint())
    __canvas.drawPath(path, __stroke_paint())


def bezier(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float) -> None:
    """Draws a bezier curve from (x1, y1) to (x4, y4) with control points (x2, y2) and (x3, y3)."""
    path = skia.Path().moveTo(x1, y1).cubicTo(x2, y2, x3, y3, x4, y4)
    __canvas.drawPath(path, __fill_paint())
    __canvas.drawPath(path, __stroke_paint())


def bezierPoint(a: float, b: float, c: float, d: float, t: float) -> float:
    """Return the value of the bezier curve at point t for points a, b, c, d. Call this function twice with the x and y
    coordinates separately, or once with both coordinates in a numpy array."""
    u = 1 - t
    return u ** 3 * a + 3 * u * t * (u * b + t * c) + t ** 3 * d


def bezierTangent(a: float, b: float, c: float, d: float, t: float) -> float:
    """Return the value of the tangent of the bezier curve at point t for points a, b, c, d. Call this function twice
    with the x and y coordinates separately, or once with both coordinates in a numpy array."""
    u = 1 - t
    return -3 * (a * u ** 2 + b * u * (3 * t - 1) + c * t * (3 * t - 2) - d * t ** 2)


def curve(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float) -> None:
    """Draws a Catmull-Rom spline from (x2, y2) to (x3, y3) with control points (x1, y1) and (x4, y4)."""
    x1, x2, x3, x4 = Context2d.catmullrom_to_bezier(x1, x2, x3, x4, __curve_tension)
    y1, y2, y3, y4 = Context2d.catmullrom_to_bezier(y1, y2, y3, y4, __curve_tension)
    bezier(x1, y1, x2, y2, x3, y3, x4, y4)


def curvePoint(a: float, b: float, c: float, d: float, t: float) -> float:
    """Return the value of a curve at point t for points a, b, c, d. Call this function twice with the x and y
    coordinates separately, or once with both coordinates in a numpy array."""
    a, b, c, d = Context2d.catmullrom_to_bezier(a, b, c, d, __curve_tension)
    return bezierPoint(a, b, c, d, t)


def curveTangent(a: float, b: float, c: float, d: float, t: float) -> float:
    """Return the value of the tangent of a curve at point t for points a, b, c, d. Call this function twice with the x
    and y coordinates separately, or once with both coordinates in a numpy array."""
    a, b, c, d = Context2d.catmullrom_to_bezier(a, b, c, d, __curve_tension)
    return bezierTangent(a, b, c, d, t)


def curveTightness(tightness: float) -> None:
    """Sets the tightness of the curve. tightness determines how the curve fits to the vertices."""
    global __curve_tension
    __curve_tension = math.inf if tightness == 1 else 1 / (1 - tightness)


def loop() -> None:
    """Restarts the drawing loop. However, this function is useless since once the drawing loop pauses, it can't be
    interacted with. This might change in future."""
    global __looping
    if not __looping:
        __looping = True
        draw(__draw_func)


def noLoop() -> None:
    """Pauses the drawing loop. The loop cannot be resumed since once the drawing loop pauses, it can't be interacted
    with."""
    global __looping
    __looping = False


def push() -> None:
    """Pushes the current context state onto an internal stack."""
    __canvas.save()


def pop() -> None:
    """Pops a previously pushed context state."""
    __canvas.restore()


def setTitle(title: str) -> None:
    """Sets the title of the scene window."""
    global __title
    __title = title


def delay(ms: int) -> None:
    """Pauses the drawing loop for ms milliseconds."""
    time.sleep(ms / 1000)


def frameRate(fps: int) -> None:
    """Specifies the frame rate to be used. The actual frame rate might be slightly lower because of calculation
    overheads."""
    global __frame_wait
    __frame_wait = 1000 // fps


def smooth(antialias: bool = True) -> None:
    """Turns on antialiasing."""
    __paint.setAntiAlias(antialias)


def noSmooth() -> None:
    """Turns off antialiasing."""
    __paint.setAntiAlias(False)


def ellipseMode(mode: int) -> None:
    """Sets the ellipse mode to be used while drawing ellipses, circles and arcs. Check the `Processing ellipseMode
    documentation <https://processing.org/reference/ellipseMode_.html>`_ for details."""
    global __ellipse_mode
    __ellipse_mode = mode


def rectMode(mode: int) -> None:
    """Sets the rect mode to be used while drawing rectangles and squares. Check the `Processing rectMode documentation
    <https://processing.org/reference/rectMode_.html>`_ for details."""
    global __rect_mode
    __rect_mode = mode


def strokeCap(cap: int) -> None:
    """Sets the style for rendering line endings. Check the `Processing strokeCap documentation
    <https://processing.org/reference/strokeCap_.html>`_ for details."""
    __paint.setStrokeCap(__stroke_caps[cap])


def strokeJoin(join: int) -> None:
    """Sets the style of the joints which connect line segments. Check the `Processing strokeJoin documentation
    <https://processing.org/reference/strokeJoin_.html>`_ for details."""
    __paint.setStrokeJoin(__stroke_joins[join])


def strokeWeight(weight: float) -> None:
    """Sets the line width used for drawing lines and points."""
    __paint.setStrokeWidth(weight)


def save(path: str) -> None:
    """Save the current frame to a *path*."""
    __scene.save_frame(path)


def saveFrame(path: str = 'screen-####.png') -> None:
    """Saves the current frame to *path* (defaults to 'screen-####.png'). The hash symbol (#) will be replaced with
    the current frame number. The number of digits is determined by the number of hashes in the path string."""
    first, last = path.find('#'), path.rfind('#')
    if first != -1:
        path = path[:first] + str(pvars.frameCount).zfill(last - first + 1) + path[last + 1:]
    __scene.save_frame(path)


def color(r: float | Sequence[float], g: float | None = None, b: float | None = None, a: float | None = None) -> Color:
    """In the processing module colors are 4-tuples of (R, G, B, A) each in range 0-1. This function returns a color
    from another color, from a shade of gray or from color components based on the current ``colorMode`` and color max
    value.

    **Syntax:**

    - ``color((r, g, b, a))``: Creates a copy of another color.
    - ``color(gray)``
    - ``color(gray, alpha)``
    - ``color(c1, c2, c3)``: Creates a color from three of its components based on ``colorMode``.
    - ``color(c1, c2, c3, alpha)``: Same as above, with alpha.
    """
    if isinstance(r, Sequence):
        if len(r) != 4:
            raise ValueError('A color must be a tuple of 4 elements.')
        return r[0], r[1], r[2], r[3]
    is_hsb = __color_mode == HSB
    if g is None:
        a = __color_max[3]
        g = b = r
        is_hsb = False
    elif b is None:
        a = g
        g = b = r
        is_hsb = False
    elif a is None:
        a = __color_max[3]
    r /= __color_max[0]
    g /= __color_max[1]
    b /= __color_max[2]
    if is_hsb:
        r, g, b = colorsys.hsv_to_rgb(r, g, b)
    return r, g, b, a / __color_max[3]


def background(r: float | Sequence[float] | skia.Image, g: float | None = None, b: float | None = None,
               a: float | None = None) -> None:
    """Clears and set the background of the scene. Parameters are same as :func:`color` or an image."""
    if isinstance(r, skia.Image):
        __canvas.drawImage(r, 0, 0)
    else:  # as fast as possible
        __canvas.clear(skia.Color4f(color(r, g, b, a)))


def colorMode(mode: int, max1: float = None, max2: float = None, max3: float = None, maxA: float = None) -> None:
    """Sets the color mode (RGB or HSB) for future drawings and maximum values for each color components."""
    global __color_mode, __color_max
    __color_mode = mode
    if max1 is not None:
        if max2 is None:
            max2 = max3 = maxA = max1
        elif maxA is None:
            maxA = __color_max[3]
        __color_max = (max1, max2, max3, maxA)


def fill(r: float | Sequence[float], g: float | None = None, b: float | None = None, a: float | None = None) -> None:
    """Sets the fill color for future drawings. Parameters are same as :func:`color`."""
    global __fill_color
    __fill_color = color(r, g, b, a)


def noFill() -> None:
    """Turns off filling for future drawings. This simply sets the fill color to transparent."""
    global __fill_color
    __fill_color = (0, 0, 0, 0)


def stroke(r: float | Sequence[float], g: float | None = None, b: float | None = None, a: float | None = None) -> None:
    """Sets the stroke color for future drawings. Parameters are same as :func:`color`."""
    global __stroke_color
    __stroke_color = color(r, g, b, a)


def noStroke() -> None:
    """Turns off drawing the stroke for future drawings. This simply sets the stroke color to transparent."""
    global __stroke_color
    __stroke_color = (0, 0, 0, 0)


def alpha(rgb: int) -> float:
    """Returns the alpha value for a 32-bit packed ARGB color scaled to the current alpha max."""
    return (rgb >> 24) / 255 * __color_max[3]


def red(rgb: int) -> float:
    """Returns the red value for a 32-bit packed ARGB color scaled to the current red max."""
    return (rgb >> 16 & 0xff) / 255 * __color_max[0]


def green(rgb: int) -> float:
    """Returns the green value for a 32-bit packed ARGB color scaled to the current green max."""
    return (rgb >> 8 & 0xff) / 255 * __color_max[1]


def blue(rgb: int) -> float:
    """Returns the blue value for a 32-bit packed ARGB color scaled to the current blue max."""
    return (rgb & 0xff) / 255 * __color_max[2]


def hue(rgb: int) -> float:
    """Returns the hue value for a 32-bit packed ARGB color scaled to the current hue max."""
    return colorsys.rgb_to_hsv((rgb >> 16 & 0xff) / 255, (rgb >> 8 & 0xff) / 255, (rgb & 0xff) / 255)[0] * __color_max[
        0]


def saturation(rgb: int) -> float:
    """Returns the saturation value for a 32-bit packed ARGB color scaled to the current saturation max."""
    return colorsys.rgb_to_hsv((rgb >> 16 & 0xff) / 255, (rgb >> 8 & 0xff) / 255, (rgb & 0xff) / 255)[1] * __color_max[
        1]


def brightness(rgb: int) -> float:
    """Returns the brightness value for a 32-bit packed ARGB color scaled to the current brightness max."""
    return colorsys.rgb_to_hsv((rgb >> 16 & 0xff) / 255, (rgb >> 8 & 0xff) / 255, (rgb & 0xff) / 255)[2] * __color_max[
        2]


def lerpColor(c1: Color, c2: Color, amt: float) -> Color:
    """Interpolate between two colors (per components) by ``amt`` amount."""
    m = 1 - amt
    return m * c1[0] + amt * c2[0], m * c1[1] + amt * c2[1], m * c1[2] + amt * c2[2], m * c1[3] + amt * c2[3]


def image(img: skia.Image, a: float, b: float, c: float | None = None, d: float | None = None) -> None:
    """Draws an image at (a, b) depending on the current image mode. (c, d) is the optional width and height (depending
    on image mode), which defaults to original image dimensions."""
    c_is_none = c is None
    if c_is_none:
        c, d = img.width(), img.height()
    bound = skia.Rect.MakeXYWH(a, b, c, d)
    if __image_mode == CORNERS and not c_is_none:
        bound = skia.Rect.MakeLTRB(a, b, c, d)
    elif __image_mode == CENTER:
        bound = skia.Rect.MakeXYWH(a - c / 2, b - d / 2, c, d)

    __canvas.drawImageRect(img, bound, skia.Paint(ColorFilter=__tint))


def imageMode(mode: int) -> None:
    """Sets the image mode to be used while drawing images. Check the `Processing imageMode documentation
    <https://processing.org/reference/imageMode_.html>`_ for details."""
    global __image_mode
    __image_mode = mode


def loadImage(path: str) -> skia.Image:
    """Loads and returns an image from the ``path``. This only supports PNG images."""
    return skia.Image.open(get_path(path))


def noTint() -> None:
    """Turns off tinting for drawing future images."""
    global __tint
    __tint = None


def tint(r: float, g: float | None = None, b: float | None = None, a: float | None = None) -> None:
    """Sets the tint color for drawing future images. Parameters are same as :func:`color`."""
    global __tint
    r, g, b, a = color(r, g, b, a)
    __tint = skia.ColorFilters.Matrix([
        r, 0, 0, 0, 0,
        0, g, 0, 0, 0,
        0, 0, b, 0, 0,
        0, 0, 0, a, 0
    ])


def rotate(angle: float) -> None:
    """Rotate by *angle* radians."""
    __canvas.rotate(math.degrees(angle))


def scale(x: float, y: float | None = None) -> None:
    """Scale by (*x*, *y*). If *y* is not specified, it equals *x*."""
    if y is None:
        y = x
    __canvas.scale(x, y)


def translate(x: float, y: float) -> None:
    """Translate by (*x*, *y*)."""
    __canvas.translate(x, y)


def constrain(amt: float, low: float, high: float) -> float:
    """Constrain a value to not exceed *low* and *high*."""
    return low if amt < low else high if amt > high else amt


def dist(x1: float, y1: float, x2: float, y2: float) -> float:
    """Returns the distance between two points, (*x1*, *y1*) and (*x2*, *y2*)."""
    return math.hypot(x1 - x2, y1 - y2)


def lerp(start: float, stop: float, amt: float) -> float:
    """Interpolate between *start* and *stop* by *amt* amount."""
    return (1 - amt) * start + amt * stop


def mag(a: float, b: float) -> float:
    """Returns the magnitude of a vector (*a*, *b*)."""
    return math.hypot(a, b)


def map_(value: float, start1: float, stop1: float, start2: float, stop2: float) -> float:
    """Remap the *value* from the (*start1*, *stop1*) range to the (*start2*, *stop2*) range. Note the underscore at the
    end, this is to differentiate it from Python's builtin ``map`` function."""
    return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2


def norm(value: float, start: float, stop: float) -> float:
    """Normalize the *value* from the (*start*, *stop*) range to (0, 1)."""
    return (value - start) / (stop - start)


def random(a: float = 1, b: float | None = None) -> float:
    """Returns a random number between 0 and *a*. If *b* is specified, returns a random number between *a* and *b*."""
    if b is None:
        a, b = 0, a
    return rnd.random() * (b - a) + a


# This is the same algorithm as implemented in Processing with variables substituted with corresponding magic numbers :)
__perlin = tuple(rnd.random() for _ in range(4096))
__perlin_cos = tuple(0.5 * (1 - math.cos(i * 0.008726646259971648)) for i in range(360))


def noise(x: float, y: float = 0, z: float = 0) -> float:
    """Returns perlin noise at a point (*x*, *y*, *z*)."""
    x, y, z = abs(x), abs(y), abs(z)
    xi, yi, zi = int(x), int(y), int(z)
    xf, yf, zf = x - xi, y - yi, z - zi
    r, ampl = 0.0, 0.5
    for i in range(__perlin_octave):
        of = xi + (yi << 4) + (zi << 8)
        rxf, ryf = __perlin_cos[int(xf * 360)], __perlin_cos[int(yf * 360)]
        n1 = __perlin[of & 4095]
        n1 += rxf * (__perlin[(of + 1) & 4095] - n1)
        n2 = __perlin[(of + 16) & 4095]
        n2 += rxf * (__perlin[(of + 17) & 4095] - n2)
        n1 += ryf * (n2 - n1)
        of += 256
        n2 = __perlin[of & 4095]
        n2 += rxf * (__perlin[(of + 1) & 4095] - n2)
        n3 = __perlin[(of + 16) & 4095]
        n3 += rxf * (__perlin[(of + 17) & 4095] - n3)
        n2 += ryf * (n3 - n2)
        n1 += __perlin_cos[int(zf * 360)] * (n2 - n1)
        r += n1 * ampl
        ampl *= __perlin_amp_falloff
        xi <<= 1
        xf *= 2
        if xf >= 1:
            xi += 1
            xf -= 1
        yi <<= 1
        yf *= 2
        if yf >= 1:
            yi += 1
            yf -= 1
        zi <<= 1
        zf *= 2
        if zf >= 1:
            zi += 1
            zf -= 1
    return r


def _get_scene() -> Scene:
    """Returns the internal scene."""
    return __scene


def _get_canvas() -> skia.Canvas:
    """Returns the internal canvas."""
    return __canvas
