"""Colors make things look better. In animator, all colors are given by a tuple of four float values, each between 0
and 1. These are simple tuples and can not be operated on. Alternatively, the :class:`ColorSwatch` class can be used
for more functionality. Some basic colors can be accessed directly by name. These include

======= ====== ==== ===== ====== ===========
BLACK   BLUE   CYAN GRAY  GREEN  LIME
MAGENTA MAROON NAVY OLIVE ORANGE PURPLE
RED     SILVER TEAL WHITE YELLOW TRANSPARENT
======= ====== ==== ===== ====== ===========

**CSS colors:** The :func:`color` function can parse CSS color strings in several formats. It can parse all the
formats specified in `MDN <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#Color_keywords>`_ including a
few generalizations. All these formats are case-insensitive.

- ``'colorname'``: Using a simple name refers to one of the CSS colors.
- ``'#hexadecimal'``: Using hexadecimal, a hexadecimal color value can be specified. This can be of several formats
  depending on the number of hexadecimal digits.
    - 1 digit (G): A shade of gray.
    - 2 digits (GA): A shade of gray and alpha.
    - 3 digits (RGB): RGB values.
    - 4 digits (RGBA): RGB values with alpha.
    - 6 digits (RRGGBB): Double digit RGB values.
    - 8 digits (RRGGBBAA): Double digit RGB values with alpha.
- ``'rgba(r, g, b, a)'``
    - Functional notations can be used, but the 'a' (alpha) in the name of the function is optional. The alpha value
      is determined by the number of arguments, if 4 arguments are provided, the last argument is the alpha.
    - The function name can be one of rgb, rgba, hsb, hsba, hsv, hsva, hls or hlsa. Again, the 'a' is optional.
    - The arguments can be any string parsable by Python's ``float`` function, followed by an optional % sign.
    - The arguments can be separated by any set of characters which does not make a number.

Some example code and possible mistakes to look out for follows.

>>> color(127.5, 255, 0, 1)  # simplest use of color: R[0-255], G[0-255], B[0-255], A[0-1]
(0.5, 1.0, 0.0, 1.0)
>>> color(255.)  # a shade of gray with a single float argument
(1.0, 1.0, 1.0, 1.0)
>>> color(255)  # a single int argument is interpreted as a packed 32-bit ARGB color
(0.0, 0.0, 1.0, 0.0)
>>> ColorSwatch(255)  # ColorSwatch takes the exact same arguments as color
(0.0, 0.0, 1.0, 0.0)
>>> ColorSwatch.RED.shade50  # a Material color shade
(1.0, 0.9215686274509803, 0.9333333333333333, 1)
>>> ColorSwatch.BROWN[900]  # another Material color shade
(0.24313725490196078, 0.15294117647058825, 0.13725490196078433, 1)
>>> ColorSwatch.BROWN.shadeA200  # no accent for Material brown, this would have worked for RED (see next example)
KeyError
>>> ColorSwatch.RED[-200]  # accent colors have a negative index
(1.0, 0.3215686274509804, 0.3215686274509804, 1)
>>> ColorSwatch('MarOon').brighten(0.5)  # color names are case insensitive
(0.7509803921568627, 0.5, 0.5, 1)
>>> ColorSwatch(r'r G b ( 50% 0, 0.0\\0.5)').saturate(0.5)  # really strange version of CSS functional format
(0.3867022311449232, 0.13670223114492316, 0.13670223114492316, 0.5)
>>> color(420, 42, 3.14, max=(420, 42, 3.14), a=0.123)  # white, scaled with max, and some alpha
(1.0, 1.0, 1.0, 0.123)
"""
from __future__ import annotations

__all__ = ('color', 'lerp_color', 'ColorSwatch', 'BLACK', 'BLUE', 'CYAN', 'GRAY', 'GREEN', 'LIME', 'MAGENTA', 'MAROON',
           'NAVY', 'OLIVE', 'ORANGE', 'PURPLE', 'RED', 'SILVER', 'TEAL', 'WHITE', 'YELLOW', 'TRANSPARENT')

import colorsys
import re
from typing import Iterable, Tuple, Callable, Literal, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .._common_types import Color

def_max = {'rgb': (255, 255, 255, 1),  # alpha always 1
           'hsb': (360, 100, 100, 1),
           'hls': (360, 100, 100, 1)}
__css_colors = {
    'black': (0, 0, 0),
    'silver': (192, 192, 192),
    'gray': (128, 128, 128),
    'white': (255, 255, 255),
    'maroon': (128, 0, 0),
    'red': (255, 0, 0),
    'purple': (128, 0, 128),
    'fuchsia': (255, 0, 255),
    'green': (0, 128, 0),
    'lime': (0, 255, 0),
    'olive': (128, 128, 0),
    'yellow': (255, 255, 0),
    'navy': (0, 0, 128),
    'blue': (0, 0, 255),
    'teal': (0, 128, 128),
    'aqua': (0, 255, 255),
    'orange': (255, 165, 0),
    'aliceblue': (240, 248, 255),
    'antiquewhite': (250, 235, 215),
    'aquamarine': (127, 255, 212),
    'azure': (240, 255, 255),
    'beige': (245, 245, 220),
    'bisque': (255, 228, 196),
    'blanchedalmond': (255, 235, 205),
    'blueviolet': (138, 43, 226),
    'brown': (165, 42, 42),
    'burlywood': (222, 184, 135),
    'cadetblue': (95, 158, 160),
    'chartreuse': (127, 255, 0),
    'chocolate': (210, 105, 30),
    'coral': (255, 127, 80),
    'cornflowerblue': (100, 149, 237),
    'cornsilk': (255, 248, 220),
    'crimson': (220, 20, 60),
    'cyan': (0, 255, 255),
    'darkblue': (0, 0, 139),
    'darkcyan': (0, 139, 139),
    'darkgoldenrod': (184, 134, 11),
    'darkgray': (169, 169, 169),
    'darkgreen': (0, 100, 0),
    'darkgrey': (169, 169, 169),
    'darkkhaki': (189, 183, 107),
    'darkmagenta': (139, 0, 139),
    'darkolivegreen': (85, 107, 47),
    'darkorange': (255, 140, 0),
    'darkorchid': (153, 50, 204),
    'darkred': (139, 0, 0),
    'darksalmon': (233, 150, 122),
    'darkseagreen': (143, 188, 143),
    'darkslateblue': (72, 61, 139),
    'darkslategray': (47, 79, 79),
    'darkslategrey': (47, 79, 79),
    'darkturquoise': (0, 206, 209),
    'darkviolet': (148, 0, 211),
    'deeppink': (255, 20, 147),
    'deepskyblue': (0, 191, 255),
    'dimgray': (105, 105, 105),
    'dimgrey': (105, 105, 105),
    'dodgerblue': (30, 144, 255),
    'firebrick': (178, 34, 34),
    'floralwhite': (255, 250, 240),
    'forestgreen': (34, 139, 34),
    'gainsboro': (220, 220, 220),
    'ghostwhite': (248, 248, 255),
    'gold': (255, 215, 0),
    'goldenrod': (218, 165, 32),
    'greenyellow': (173, 255, 47),
    'grey': (128, 128, 128),
    'honeydew': (240, 255, 240),
    'hotpink': (255, 105, 180),
    'indianred': (205, 92, 92),
    'indigo': (75, 0, 130),
    'ivory': (255, 255, 240),
    'khaki': (240, 230, 140),
    'lavender': (230, 230, 250),
    'lavenderblush': (255, 240, 245),
    'lawngreen': (124, 252, 0),
    'lemonchiffon': (255, 250, 205),
    'lightblue': (173, 216, 230),
    'lightcoral': (240, 128, 128),
    'lightcyan': (224, 255, 255),
    'lightgoldenrodyellow': (250, 250, 210),
    'lightgray': (211, 211, 211),
    'lightgreen': (144, 238, 144),
    'lightgrey': (211, 211, 211),
    'lightpink': (255, 182, 193),
    'lightsalmon': (255, 160, 122),
    'lightseagreen': (32, 178, 170),
    'lightskyblue': (135, 206, 250),
    'lightslategray': (119, 136, 153),
    'lightslategrey': (119, 136, 153),
    'lightsteelblue': (176, 196, 222),
    'lightyellow': (255, 255, 224),
    'limegreen': (50, 205, 50),
    'linen': (250, 240, 230),
    'magenta': (255, 0, 255),
    'mediumaquamarine': (102, 205, 170),
    'mediumblue': (0, 0, 205),
    'mediumorchid': (186, 85, 211),
    'mediumpurple': (147, 112, 219),
    'mediumseagreen': (60, 179, 113),
    'mediumslateblue': (123, 104, 238),
    'mediumspringgreen': (0, 250, 154),
    'mediumturquoise': (72, 209, 204),
    'mediumvioletred': (199, 21, 133),
    'midnightblue': (25, 25, 112),
    'mintcream': (245, 255, 250),
    'mistyrose': (255, 228, 225),
    'moccasin': (255, 228, 181),
    'navajowhite': (255, 222, 173),
    'oldlace': (253, 245, 230),
    'olivedrab': (107, 142, 35),
    'orangered': (255, 69, 0),
    'orchid': (218, 112, 214),
    'palegoldenrod': (238, 232, 170),
    'palegreen': (152, 251, 152),
    'paleturquoise': (175, 238, 238),
    'palevioletred': (219, 112, 147),
    'papayawhip': (255, 239, 213),
    'peachpuff': (255, 218, 185),
    'peru': (205, 133, 63),
    'pink': (255, 192, 203),
    'plum': (221, 160, 221),
    'powderblue': (176, 224, 230),
    'rosybrown': (188, 143, 143),
    'royalblue': (65, 105, 225),
    'saddlebrown': (139, 69, 19),
    'salmon': (250, 128, 114),
    'sandybrown': (244, 164, 96),
    'seagreen': (46, 139, 87),
    'seashell': (255, 245, 238),
    'sienna': (160, 82, 45),
    'skyblue': (135, 206, 235),
    'slateblue': (106, 90, 205),
    'slategray': (112, 128, 144),
    'slategrey': (112, 128, 144),
    'snow': (255, 250, 250),
    'springgreen': (0, 255, 127),
    'steelblue': (70, 130, 180),
    'tan': (210, 180, 140),
    'thistle': (216, 191, 216),
    'tomato': (255, 99, 71),
    'turquoise': (64, 224, 208),
    'violet': (238, 130, 238),
    'wheat': (245, 222, 179),
    'whitesmoke': (245, 245, 245),
    'yellowgreen': (154, 205, 50),
    'rebeccapurple': (102, 51, 153)
}


def __parse_max(max: float | Iterable[float] | None, type: str) -> Tuple[float, float, float, float]:
    if max is None:
        return def_max[type]
    if isinstance(max, Iterable):
        max = list(max)
        l = len(max)
        if l == 1:  # gray
            return max[0], max[0], max[0], 1
        if l == 2:  # gray, alpha
            return max[0], max[0], max[0], max[1]
        if l == 3:  # rgb
            return max[0], max[1], max[2], 1
        return max[0], max[1], max[2], max[3]  # rgba
    else:  # not iterable, so for all
        return max, max, max, max


__h: float = 0.0


# TODO: How to make this return constant brightness colors?
def __unique_color() -> Color:
    global __h
    r, g, b, x = 0.0, 0.0, 0.0, 1 - abs(__h % 2 - 1)
    if __h < 1:
        r, g = 1.0, x
    elif __h < 2:
        r, g = x, 1.0
    elif __h < 3:
        g, b = 1.0, x
    elif __h < 4:
        g, b = x, 1.0
    elif __h < 5:
        r, b = x, 1.0
    else:
        r, b = 1.0, x
    __h = (__h + 3.708203932499369) % 6  # 6 * golden ratio
    return r, g, b, 1.


def __parse_num(n: str, max: float) -> float:
    if n[-1] == '%':
        return float(n[:-1]) / 100
    return float(n) / max


def __parse_css_color(c: str, a: float = 1, max: float | Iterable[float] | None = None) -> Color:
    col = c.strip().lower()
    c = re.sub(r'\s+', '', col)  # space-less version
    if c in __css_colors:  # a named color
        r, g, b = __css_colors[c]
        return r / 255.0, g / 255.0, b / 255.0, a

    if c[0] == '#':  # hexadecimal notation
        c = c[1:]
        l = len(c)
        if l == 1:  # gray
            g = int(c, 16) / 15
            return g, g, g, a
        if l == 2:  # gray-alpha
            g = int(c[0], 16) / 15
            a = int(c[1], 16) / 15
            return g, g, g, a
        if l == 3:  # rgb
            rgb = int(c, 16)
            return (rgb >> 8) / 15, ((rgb >> 4) & 0xf) / 15, (rgb & 0xf) / 15, a
        if l == 4:  # rgba
            rgba = int(c, 16)
            return (rgba >> 12) / 15, ((rgba >> 8) & 0xf) / 15, ((rgba >> 4) & 0xf) / 15, (rgba & 0xf) / 15
        if l == 6:  # rrggbb
            rrggbb = int(c, 16)
            return (rrggbb >> 16) / 255, ((rrggbb >> 8) & 0xff) / 255, (rrggbb & 0xff) / 255, a
        if l == 8:  # rrggbbaa
            rrggbbaa = int(c, 16)
            return (rrggbbaa >> 24) / 255, ((rrggbbaa >> 16) & 0xff) / 255, ((rrggbbaa >> 8) & 0xff) / 255, \
                   (rrggbbaa & 0xff) / 255

    left_par, right_par = col.find('('), col.find(')')  # function notation
    type = re.sub(r'\s+', '', col[:left_par])
    comp = [m.group() for m in re.finditer(r'[-+]?[0-9]+[.]?[0-9]*([eE][-+]?[0-9]+)?%?', col[left_par + 1:right_par])]
    if type in {'rgb', 'rgba'}:
        max = __parse_max(max, 'rgb')
        comp = [__parse_num(n, max[i]) for i, n in enumerate(comp)]
        if len(comp) == 3:
            comp.append(a / max[-1])
        return color(rgba=comp, max=(1, 1, 1, 1))
    if type in {'hsb', 'hsba', 'hsv', 'hsva'}:
        max = __parse_max(max, 'hsb')
        comp = [__parse_num(n, max[i]) for i, n in enumerate(comp)]
        if len(comp) == 3:
            comp.append(a / max[-1])
        return color(hsba=comp, max=(1, 1, 1, 1))
    if type in {'hls', 'hlsa'}:
        max = __parse_max(max, 'hls')
        comp = [__parse_num(n, max[i]) for i, n in enumerate(comp)]
        if len(comp) == 3:
            comp.append(a / max[-1])
        return color(hlsa=comp, max=(1, 1, 1, 1))
    return TRANSPARENT


# Quick colors
BLACK = (0., 0., 0., 1.)
BLUE = (0., 0., 1., 1.)
CYAN = (0., 1., 1., 1.)
GRAY = (.5, .5, .5, 1.)
GREEN = (0., .5, 0., 1.)
LIME = (0., 1., 0., 1.)
MAGENTA = (1., 0., 1., 1.)
MAROON = (.5, 0., 0., 1.)
NAVY = (0., 0., .5, 1.)
OLIVE = (.5, .5, 0., 1.)
ORANGE = (1., .65, 0., 1.)
PURPLE = (.5, 0., .5, 1.)
RED = (1., 0., 0., 1.)
SILVER = (.75, .75, .75, 1.)
TEAL = (0., .5, .5, 1.)
WHITE = (1., 1., 1., 1.)
YELLOW = (1., 1., 0., 1.)
TRANSPARENT = (0., 0., 0., 0.)


def color(r: int | float | Iterable[float] | str | None = None, g: float | None = None, b: float | None = None,
          a: float = 1, packed: int | None = None, argb: int | None = None,
          rgb: Tuple[float, float, float] | None = None, rgba: Tuple[float, float, float, float] | None = None,
          hsb: Tuple[float, float, float] | None = None, hsba: Tuple[float, float, float, float] | None = None,
          hsv: Tuple[float, float, float] | None = None, hsva: Tuple[float, float, float, float] | None = None,
          hls: Tuple[float, float, float] | None = None, hlsa: Tuple[float, float, float, float] | None = None,
          max: float | Iterable[float] | None = None) -> Color:
    """A all-in-one color function. This can be used in several ways. If multiple formats are specified, they are parsed
    in the order specified below. The function returns a tuple with (r, g, b, a), each between 0 and 1.

    :note: It is not guaranteed that the components will be in the range [0, 1], depending on what values you pass.

    This function also takes a *max* parameter, which specifies the maximum possible value of a parameter. This is used
    to scale the parameters between 0 and 1, although no checks are made to ensure that the parameters are within the
    range. *max* should generally consist of four components (R, G and B for RGB; H, S, B for HSB, etc. and A for
    alpha), but can be specified in several ways.

    - ``max=n``: If a single number is provided, the same is used for all the fields. (n, n, n, n)
    - ``max=[n]``: If an iterable with a single number is provided, it is used for the first three fields and alpha is
      set to 1. (n, n, n, 1)
    - ``max=[m, n]``: If an iterable with two numbers is provided, the first number is used for the first three
      fields and the second number is used for alpha. (m, m, m, n)
    - ``max=[m, n, o]``: If an iterable with three numbers is provided, they are used for the first three fields and
      alpha is set to 1. (m, n, o, 1)
    - ``max=[m, n, o, p, ...]``: If an iterable with four or more numbers is provided, the first four are used for the
      four fields.
    - ``max=None``: The maximum value is automatically determined if nothing is specified. It is (255, 255, 255, 1) for
      RGB and (360, 100, 100, 1) for HSB, HSV and HLS.

    **Color orders:** If multiple color formats are specified, they are parsed in the following order and whichever is
    found first is returned.

    - ``color(r, g, b)`` or ``color(r, g, b, a)``: Returns the RGB color with an optional alpha value.
    - ``color(g, a)``: Returns a shade of gray with value of g, and given alpha.
    - If a single value is given, there are multiple formats available.
        - ``color(g: float between 0 and max)``: Returns a shade of gray.
        - ``color(g: int)``: This is like calling with the *packed* or *argb* parameter, returns a color with ARGB
          values packed as a 32-bit integer.
        - ``color([r, g, b, a]: Iterable)``: When called with a iterable, returns the values as is parsed into the
          4-component RGBA values. In this case the values are not scaled by *max*.
        - ``color('color': str, a=a)``: If called with a string, it is parsed as one of the CSS color formats discussed
          above. In this format a optional alpha and max value can also be specified as a named argument.
    - ``color(packed=0xaarrggbb)`` or ``color(argb=0xaarrggbb)``: Returns a color with ARGB values packed as a 32-bit
      integer.
    - ``color(rgb=(r, g, b))``: Returns a color with RGB values as specified.
    - ``color(rgba=(r, g, b, a))``: Returns a color with RGB and alpha values as specified. Note that this is different
      from ``argb``.
    - ``color(hsb=(h, s, b))``: Returns a HSB color converted to RGB.
    - ``color(hsba=(h, s, b, a))``: Returns a HSB color converted to RGB and alpha.
    - ``color(hsv=(h, s, v))``: Returns a HSV color converted to RGB.
    - ``color(hsva=(h, s, v, a))``: Returns a HSV color converted to RGB and alpha.
    - ``color(hls=(h, l, s))``: Returns a HLS color converted to RGB.
    - ``color(hlsa=(h, l, s, a))``: Returns a HLS color converted to RGB and alpha.
    - ``color()``: Returns a unique color each time called without any parameters.
    """
    mr, mg, mb, ma = __parse_max(max, 'rgb')
    if b is not None:  # RGB
        return r / mr, g / mg, b / mb, a / ma
    if g is not None:  # gray-alpha
        r /= mr
        return r, r, r, g
    if r is not None:
        if isinstance(r, float):  # gray
            r /= mr
            return r, r, r, a / ma
        if isinstance(r, int):
            return color(packed=r)
        if isinstance(r, str):  # first check for string
            return __parse_css_color(r, a, max)
        if isinstance(r, Iterable):  # assumes len(r) == 4, otherwise general fallback
            return __parse_max(r, 'rgb')  # shortcut, because they use the same format

    if not (packed is None and argb is None):
        if argb is None:
            argb = packed
        a = argb >> 24
        r = (argb >> 16) & 0xff
        g = (argb >> 8) & 0xff
        b = argb & 0xff
        return r / 255, g / 255, b / 255, a / 255

    if not (rgb is None and rgba is None):
        if rgb is None:
            r, g, b, a = rgba
        else:
            r, g, b = rgb
        mr, mg, mb, ma = __parse_max(max, 'rgb')
        return r / mr, g / mg, b / mb, a / ma

    if not (hsb is None and hsba is None and hsv is None and hsva is None):
        if hsb is not None:
            h, s, b = hsb
        elif hsba is not None:
            h, s, b, a = hsba
        elif hsv is not None:
            h, s, b = hsv
        else:  # hsva
            h, s, b, a = hsva
        mh, ms, mb, ma = __parse_max(max, 'hsb')
        return (*colorsys.hsv_to_rgb(h / mh, s / ms, b / mb), a / ma)

    if not (hls is None or hlsa is None):
        if hls is None:
            h, l, s, a = hlsa
        else:
            h, l, s = hls
        mh, ml, ms, ma = __parse_max(max, 'hsb')
        return (*colorsys.hls_to_rgb(h / mh, l / ml, s / ms), a / ma)

    return __unique_color()  # nothing matched


def lerp_color(c1: Color, c2: Color, amt: float | None = None, mode: Literal['rgb', 'hsv', 'hsv_linear'] = 'rgb') \
        -> Color | Callable[[float], Color]:
    """Returns an interpolation between two colors, *c1* and *c2*. If *amt* is provided, this function returns the
    interpolated color. However for multiple calls to this function, call this function without the *amt* argument,
    which will return another function which can be called with the *amt* argument for the interpolation result. Several
    interpolation modes are available (alpha is interpolated linearly for all modes):

    - ``rgb``: The components are interpolated in the RGB color space.
    - ``hsv``: The components are interpolated in the HSV color space.
    - ``hsv_linear``: The components are interpolated in the HSV color space. Since HSV is a cylindrical system, the hue
      component is normally interpolated in the direction of the smaller angle. *hsv_linear* makes the interpolation
      linear instead.

    :param c1: The first color.
    :param c2: The second color.
    :param amt: Amount of interpolation, 0: first color, 1: second color. If absent, a function is returned which can be
        called with ``amt`` to get the interpolation.
    :param mode: Mode of interpolation to be used. Either ``'rgb'``, ``'hsv'``, or ``'hsv_linear'``.
    """
    if mode == 'rgb':
        def f(t: float) -> Color:
            m = 1 - t
            return m * c1[0] + t * c2[0], m * c1[1] + t * c2[1], m * c1[2] + t * c2[2], m * c1[3] + t * c2[3]
    else:  # hsv or hsv_linear
        c1, a1 = list(colorsys.rgb_to_hsv(c1[0], c1[1], c1[2])), c1[3]
        c2, a2 = list(colorsys.rgb_to_hsv(c2[0], c2[1], c2[2])), c2[3]
        if mode == 'hsv':
            if c1[0] < c2[0]:
                if 1 + c1[0] - c2[0] < c2[0] - c1[0]:
                    c1[0] += 1
            elif 1 + c2[0] - c1[0] < c1[0] - c2[0]:
                c2[0] += 1

        def f(t: float) -> Color:
            m = 1 - t
            return (*colorsys.hsv_to_rgb((m * c1[0] + t * c2[0]) % 1, m * c1[1] + t * c2[1], m * c1[2] + t * c2[2]),
                    m * a1 + t * a2)
    return f if amt is None else f(amt)


class ColorSwatch(Tuple[float]):
    """High functionality color class.

    It behaves like a 4-tuple of (r, g, b, a) values with added functionality and can be used anywhere instead of the
    normal :func:`color` function. This allows for adding, multiplying and dividing two colors, or a color by a
    float, changing brightness and saturation and material like multiple color shades. The constructor takes the same
    arguments as the :func:`color` function. Material color shades and accents can be accessed with the following
    properties:

    - **Shades:** ``shade50``, ``shade100``, ``shade200``, ``shade300``, ``shade400``, ``shade500``, ``shade600``,
      ``shade700``, ``shade800``, ``shade900``
    - **Accents:** ``shadeA100``, ``shadeA200``, ``shadeA400``, ``shadeA700`` (not available for ``BROWN``,
    ``GREY`` and ``BLUE_GREY``)

    :note: Material like color shades are only supported for inbuilt material colors.
    """

    def __new__(cls, *args: Any, **kwargs: Any):
        col = super().__new__(cls, color(*args, **kwargs))
        col.shades = {}
        return col

    @property
    def r(self) -> float:
        """Red component of the color."""
        return self[0]

    @property
    def g(self) -> float:
        """Green component of the color."""
        return self[1]

    @property
    def b(self) -> float:
        """Blue component of the color."""
        return self[2]

    @property
    def a(self) -> float:
        """Alpha component of the color."""
        return self[3]

    def __getitem__(self, item: int) -> float | ColorSwatch:
        """Allows for accessing the material color shades."""
        try:
            return super().__getitem__(item)
        except IndexError as e:
            if item == 500:
                return self
            return ColorSwatch(self.shades[item])

    def __getattr__(self, item: str) -> 'ColorSwatch':
        """Allows for accessing the material color shades."""
        item = item.lower()
        if item.startswith('shadea'):  # accent
            return ColorSwatch(self.shades[-int(item[6:])])
        item = int(item[5:])
        if item == 500:
            return self
        return ColorSwatch(self.shades[item])

    def __add__(self, other: ColorSwatch) -> ColorSwatch:
        """Add two colors per component."""
        return ColorSwatch((min(self.r + other.r, 1), min(self.g + other.g, 1),
                            min(self.b + other.b, 1), min(self.a + other.a, 1)))

    def __sub__(self, other: ColorSwatch) -> ColorSwatch:
        """Subtract two colors per component."""
        return ColorSwatch((max(0.0, self.r - other.r), max(0.0, self.g - other.g),
                            max(0.0, self.b - other.b), max(0.0, self.a - other.a)))

    def __mul__(self, other: ColorSwatch | int | float) -> ColorSwatch:
        """Multiply two colors per component or a single color (except alpha) with a factor."""
        if isinstance(other, (int, float)):
            return ColorSwatch((min(self.r * other, 1), min(self.g * other, 1), min(self.b * other, 1), self.a))
        return ColorSwatch((self.r * other.r, self.g * other.g, self.b * other.b, self.a * other.a))

    __rmul__ = __mul__

    def __truediv__(self, other: float) -> ColorSwatch:
        """Divide each component (except alpha) of the color with a factor."""
        return ColorSwatch((self.r / other, self.g / other, self.b / other, self.a))

    def brighten(self, brightness: float = 0.1) -> ColorSwatch:
        """Returns a brighter (or darker) version of the color. Alpha is not changed.

        :param brightness: The amount to brighten the color, can be negative for darker colors. 0: no change, 1: full
            brightness (white), -1: full darkness (black).
        """
        # code from https://www.pvladov.com/2012/09/make-color-lighter-or-darker.html
        if brightness < 0:
            brightness += 1
            return ColorSwatch((self.r * brightness, self.g * brightness, self.b * brightness, self.a))
        return ColorSwatch(((1 - self.r) * brightness + self.r, (1 - self.g) * brightness + self.g,
                            (1 - self.b) * brightness + self.b, self.a))

    def saturate(self, saturation: float = 1.1) -> ColorSwatch:
        """Returns a saturated (or desaturated) version of the color. Alpha is not changed.

        :param saturation: The amount to saturate the color. 0: completely desaturated (gray), 1: no change, 0.5: half
            saturation, 2: double saturation.
        """
        # code from https://alienryderflex.com/saturation.html
        r, g, b, a = self
        s = (0.299 * r * r + 0.587 * g * g + 0.114 * b * b) ** 0.5
        return ColorSwatch((max(0, min(s + (r - s) * saturation, 1)), max(0, min(s + (g - s) * saturation, 1)),
                            max(0, min(s + (b - s) * saturation, 1)), a))

    def with_alpha(self, alpha: float = 1) -> ColorSwatch:
        """Returns the color with the given *alpha* value."""
        return ColorSwatch(self[0], self[1], self[2], alpha)

    with_opacity = with_alpha

    @classmethod
    def material(cls, *shades: Tuple[int, int, int]) -> ColorSwatch:
        """Builds a (material) swatch from 10 color shades and another 4 optional accent shades."""
        shades = list(map(lambda x: color(*x), shades))
        swatch: ColorSwatch = cls(shades[5])
        swatch.shades[50] = shades[0]
        swatch.shades[100] = shades[1]
        swatch.shades[200] = shades[2]
        swatch.shades[300] = shades[3]
        swatch.shades[400] = shades[4]
        swatch.shades[600] = shades[6]
        swatch.shades[700] = shades[7]
        swatch.shades[800] = shades[8]
        swatch.shades[900] = shades[9]
        if len(shades) > 10:
            swatch.shades[-100] = shades[10]
            swatch.shades[-200] = shades[11]
            swatch.shades[-400] = shades[12]
            swatch.shades[-700] = shades[13]
        return swatch


ColorSwatch.RED = ColorSwatch.material((255, 235, 238), (255, 205, 210), (239, 154, 154), (229, 115, 115),
                                       (239, 83, 80), (244, 67, 54), (229, 57, 53), (211, 47, 47), (198, 40, 40),
                                       (183, 28, 28), (255, 138, 128), (255, 82, 82), (255, 23, 68), (213, 0, 0))
ColorSwatch.PINK = ColorSwatch.material((252, 228, 236), (248, 187, 208), (244, 143, 177), (240, 98, 146),
                                        (236, 64, 122), (233, 30, 99), (216, 27, 96), (194, 24, 91), (173, 20, 87),
                                        (136, 14, 79), (255, 128, 171), (255, 64, 129), (245, 0, 87), (197, 17, 98))
ColorSwatch.PURPLE = ColorSwatch.material((243, 229, 245), (225, 190, 231), (206, 147, 216), (186, 104, 200),
                                          (171, 71, 188), (156, 39, 176), (142, 36, 170), (123, 31, 162),
                                          (106, 27, 154), (74, 20, 140), (234, 128, 252), (224, 64, 251), (213, 0, 249),
                                          (170, 0, 255))
ColorSwatch.DEEP_PURPLE = ColorSwatch.material((237, 231, 246), (209, 196, 233), (179, 157, 219), (149, 117, 205),
                                               (126, 87, 194), (103, 58, 183), (94, 53, 177), (81, 45, 168),
                                               (69, 39, 160), (49, 27, 146), (179, 136, 255), (124, 77, 255),
                                               (101, 31, 255), (98, 0, 234))
ColorSwatch.INDIGO = ColorSwatch.material((232, 234, 246), (197, 202, 233), (159, 168, 218), (121, 134, 203),
                                          (92, 107, 192), (63, 81, 181), (57, 73, 171), (48, 63, 159), (40, 53, 147),
                                          (26, 35, 126), (140, 158, 255), (83, 109, 254), (61, 90, 254), (48, 79, 254))
ColorSwatch.BLUE = ColorSwatch.material((227, 242, 253), (187, 222, 251), (144, 202, 249), (100, 181, 246),
                                        (66, 165, 245), (33, 150, 243), (30, 136, 229), (25, 118, 210), (21, 101, 192),
                                        (13, 71, 161), (130, 177, 255), (68, 138, 255), (41, 121, 255), (41, 98, 255))
ColorSwatch.LIGHT_BLUE = ColorSwatch.material((225, 245, 254), (179, 229, 252), (129, 212, 250), (79, 195, 247),
                                              (41, 182, 246), (3, 169, 244), (3, 155, 229), (2, 136, 209),
                                              (2, 119, 189), (1, 87, 155), (128, 216, 255), (64, 196, 255),
                                              (0, 176, 255), (0, 145, 234))
ColorSwatch.CYAN = ColorSwatch.material((224, 247, 250), (178, 235, 242), (128, 222, 234), (77, 208, 225),
                                        (38, 198, 218), (0, 188, 212), (0, 172, 193), (0, 151, 167), (0, 131, 143),
                                        (0, 96, 100), (132, 255, 255), (24, 255, 255), (0, 229, 255), (0, 184, 212))
ColorSwatch.TEAL = ColorSwatch.material((224, 242, 241), (178, 223, 219), (128, 203, 196), (77, 182, 172),
                                        (38, 166, 154), (0, 150, 136), (0, 137, 123), (0, 121, 107), (0, 105, 92),
                                        (0, 77, 64), (167, 255, 235), (100, 255, 218), (29, 233, 182), (0, 191, 165))
ColorSwatch.GREEN = ColorSwatch.material((232, 245, 233), (200, 230, 201), (165, 214, 167), (129, 199, 132),
                                         (102, 187, 106), (76, 175, 80), (67, 160, 71), (56, 142, 60), (46, 125, 50),
                                         (27, 94, 32), (185, 246, 202), (105, 240, 174), (0, 230, 118), (0, 200, 83))
ColorSwatch.LIGHT_GREEN = ColorSwatch.material((241, 248, 233), (220, 237, 200), (197, 225, 165), (174, 213, 129),
                                               (156, 204, 101), (139, 195, 74), (124, 179, 66), (104, 159, 56),
                                               (85, 139, 47), (51, 105, 30), (204, 255, 144), (178, 255, 89),
                                               (118, 255, 3), (100, 221, 23))
ColorSwatch.LIME = ColorSwatch.material((249, 251, 231), (240, 244, 195), (230, 238, 156), (220, 231, 117),
                                        (212, 225, 87), (205, 220, 57), (192, 202, 51), (175, 180, 43), (158, 157, 36),
                                        (130, 119, 23), (244, 255, 129), (238, 255, 65), (198, 255, 0), (174, 234, 0))
ColorSwatch.YELLOW = ColorSwatch.material((255, 253, 231), (255, 249, 196), (255, 245, 157), (255, 241, 118),
                                          (255, 238, 88), (255, 235, 59), (253, 216, 53), (251, 192, 45),
                                          (249, 168, 37), (245, 127, 23), (255, 255, 141), (255, 255, 0), (255, 234, 0),
                                          (255, 214, 0))
ColorSwatch.AMBER = ColorSwatch.material((255, 248, 225), (255, 236, 179), (255, 224, 130), (255, 213, 79),
                                         (255, 202, 40), (255, 193, 7), (255, 179, 0), (255, 160, 0), (255, 143, 0),
                                         (255, 111, 0), (255, 229, 127), (255, 215, 64), (255, 196, 0), (255, 171, 0))
ColorSwatch.ORANGE = ColorSwatch.material((255, 243, 224), (255, 224, 178), (255, 204, 128), (255, 183, 77),
                                          (255, 167, 38), (255, 152, 0), (251, 140, 0), (245, 124, 0), (239, 108, 0),
                                          (230, 81, 0), (255, 209, 128), (255, 171, 64), (255, 145, 0), (255, 109, 0))
ColorSwatch.DEEP_ORANGE = ColorSwatch.material((251, 233, 231), (255, 204, 188), (255, 171, 145), (255, 138, 101),
                                               (255, 112, 67), (255, 87, 34), (244, 81, 30), (230, 74, 25),
                                               (216, 67, 21), (191, 54, 12), (255, 158, 128), (255, 110, 64),
                                               (255, 61, 0), (221, 44, 0))
# No accent for the following
ColorSwatch.BROWN = ColorSwatch.material((239, 235, 233), (215, 204, 200), (188, 170, 164), (161, 136, 127),
                                         (141, 110, 99), (121, 85, 72), (109, 76, 65), (93, 64, 55), (78, 52, 46),
                                         (62, 39, 35))
ColorSwatch.GREY = ColorSwatch.material((250, 250, 250), (245, 245, 245), (238, 238, 238), (224, 224, 224),
                                        (189, 189, 189), (158, 158, 158), (117, 117, 117), (97, 97, 97), (66, 66, 66),
                                        (33, 33, 33))
ColorSwatch.BLUE_GREY = ColorSwatch.material((236, 239, 241), (207, 216, 220), (176, 190, 197), (144, 164, 174),
                                             (120, 144, 156), (96, 125, 139), (84, 110, 122), (69, 90, 100),
                                             (55, 71, 79), (38, 50, 56))
# aliases
ColorSwatch.GRAY = ColorSwatch.GREY
ColorSwatch.BLUE_GRAY = ColorSwatch.BLUE_GREY
